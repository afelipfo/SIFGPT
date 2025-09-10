from abc import ABC, abstractmethod
from typing import Optional, List
from pathlib import Path
import os
from openai import OpenAI
from faster_whisper import WhisperModel
from src.utils.logger import logger
from src.config.config import config
from src.models.pqrs_model import AudioTranscription

class TranscriptionStrategy(ABC):
    """Estrategia abstracta para transcripción de audio"""
    
    @abstractmethod
    def transcribe(self, audio_file) -> str:
        """Transcribe un archivo de audio"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Retorna los formatos de audio soportados"""
        pass

class OpenAIWhisperStrategy(TranscriptionStrategy):
    """Estrategia de transcripción usando OpenAI Whisper"""
    
    def __init__(self, api_key: str, model: str = 'whisper-1'):
        """Inicializa la estrategia OpenAI Whisper"""
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Reducir logging
        pass  # logger.info(f"Estrategia OpenAI Whisper inicializada con modelo: {model}")
    
    def transcribe(self, audio_file) -> str:
        """Transcribe usando OpenAI Whisper"""
        try:
            logger.info("Iniciando transcripción con OpenAI Whisper")
            
            # Convertir FileStorage de Flask a bytes para OpenAI
            if hasattr(audio_file, 'read'):
                # Si es un FileStorage de Flask, leer los bytes
                logger.info(f"Procesando FileStorage - filename: {getattr(audio_file, 'filename', 'unknown')}")
                
                # Resetear posición del archivo por si ya fue leído
                if hasattr(audio_file, 'seek'):
                    audio_file.seek(0)
                
                audio_bytes = audio_file.read()
                logger.info(f"Audio leído: {len(audio_bytes)} bytes")
                
                if len(audio_bytes) == 0:
                    raise ValueError("El archivo de audio está vacío")
                
                # Crear un objeto BytesIO para OpenAI
                from io import BytesIO
                audio_io = BytesIO(audio_bytes)
                
                # OpenAI necesita el nombre del archivo para determinar el formato
                if hasattr(audio_file, 'filename') and audio_file.filename:
                    audio_io.name = audio_file.filename
                else:
                    # Asumir formato WAV por defecto si no hay nombre
                    audio_io.name = 'recording.wav'
                
                logger.info(f"Preparando para transcripción con nombre: {audio_io.name}")
            else:
                audio_io = audio_file
                logger.info("Usando archivo directo para transcripción")
            
            # Realizar transcripción
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_io,
                language='es',
                response_format="text",
                prompt="Esta es una consulta ciudadana sobre PQRS, radicados, solicitudes o servicios municipales en Medellín."
            )
            
            if not transcription or not transcription.strip():
                raise ValueError("La transcripción resultó vacía")
            
            logger.info(f"Transcripción OpenAI Whisper completada exitosamente: {len(transcription)} caracteres")
            return transcription.strip()
            
        except Exception as e:
            logger.exception(f"Error en transcripción OpenAI Whisper: {str(e)}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Formatos soportados por OpenAI Whisper"""
        return ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "ogg", "flac", "aac"]

class FasterWhisperStrategy(TranscriptionStrategy):
    """Estrategia de transcripción usando Faster Whisper (local)"""
    
    def __init__(self, model: str = 'large-v3', compute_type: str = "int8"):
        """Inicializa la estrategia Faster Whisper"""
        self.model = WhisperModel(model, compute_type=compute_type)
        logger.info(f"Estrategia Faster Whisper inicializada con modelo: {model}")
    
    def transcribe(self, audio_file) -> str:
        """Transcribe usando Faster Whisper"""
        try:
            if hasattr(audio_file, 'name'):
                file_path = audio_file.name
            else:
                file_path = str(audio_file)
            
            segments, info = self.model.transcribe(
                file_path, 
                beam_size=2, 
                language="es"
            )
            
            transcription = " ".join([segment.text for segment in segments])
            logger.info("Transcripción Faster Whisper completada exitosamente")
            return transcription
        except Exception as e:
            logger.error(f"Error en transcripción Faster Whisper: {e}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Formatos soportados por Faster Whisper"""
        return ["wav", "mp3", "flac", "ogg", "m4a", "aac"]

class AudioService:
    """Servicio principal para manejo de audio"""
    
    def __init__(self, strategy: TranscriptionStrategy):
        """Inicializa el servicio de audio con una estrategia"""
        self.strategy = strategy
        self.audio_extensions = config.AUDIO_EXTENSIONS
        # logger.info("Servicio de audio inicializado")
    
    def get_audio_files(self, folder_path: str) -> List[str]:
        """Obtiene lista de archivos de audio en un directorio"""
        try:
            from glob import glob
            audio_files = []
            for ext in self.audio_extensions:
                audio_files.extend(glob(os.path.join(folder_path, ext)))
            
            logger.info(f"Encontrados {len(audio_files)} archivos de audio en {folder_path}")
            return audio_files
        except Exception as e:
            logger.error(f"Error al obtener archivos de audio: {e}")
            return []
    
    def transcribe_audio(self, audio_file) -> AudioTranscription:
        """Transcribe un archivo de audio"""
        try:
            logger.info("Iniciando transcripción de audio")
            
            # Obtener nombre del archivo
            if hasattr(audio_file, 'filename'):
                filename = audio_file.filename
            elif hasattr(audio_file, 'name'):
                filename = os.path.basename(audio_file.name)
            else:
                filename = "recording.wav"  # Nombre por defecto
            
            logger.info(f"Procesando archivo: {filename}")
            
            # Validar formato antes de transcribir (pero no fallar si no es válido)
            if not self.validate_audio_format(filename):
                logger.warning(f"Formato posiblemente no soportado, pero continuando: {filename}")
            
            # Realizar transcripción
            logger.info("Iniciando proceso de transcripción...")
            transcription_text = self.strategy.transcribe(audio_file)
            
            # Validar que la transcripción no esté vacía
            if not transcription_text or not transcription_text.strip():
                raise ValueError("La transcripción resultó vacía - el audio podría no contener habla reconocible")
            
            # Validar y limpiar la transcripción antes de procesarla
            cleaned_transcription = self.validate_and_clean_transcription(transcription_text.strip())
            
            # Mejorar el texto transcrito para una mejor interpretación de radicados
            improved_transcription = self.improve_transcription_for_radicados(cleaned_transcription)
            
            # Crear objeto de transcripción
            audio_transcription = AudioTranscription(
                audio_file=filename,
                transcription=improved_transcription
            )
            
            logger.info(f"Transcripción completada exitosamente para: {filename} - {len(improved_transcription)} caracteres")
            logger.info(f"Texto transcrito original: {transcription_text[:100]}...")
            if transcription_text != cleaned_transcription:
                logger.info(f"Texto transcrito limpio: {cleaned_transcription[:100]}...")
            if cleaned_transcription != improved_transcription:
                logger.info(f"Texto transcrito mejorado: {improved_transcription[:100]}...")
            
            return audio_transcription
            
        except Exception as e:
            logger.exception(f"Error en transcripción de audio: {str(e)}")
            raise
    
    def validate_and_clean_transcription(self, transcription: str) -> str:
        """Valida y limpia la transcripción eliminando contenido irrelevante o ruido"""
        import re
        
        try:
            # Lista de patrones que indican contenido irrelevante o ruido de transcripción
            noise_patterns = [
                # Patrones de subtítulos automáticos
                r'subtítulos?\s+realizados?\s+por\s+.*?amara\.org',
                r'subtitles?\s+(provided|created|made)\s+by\s+.*?amara\.org',
                r'subtítulos?\s+de\s+.*?comunidad',
                
                # Patrones de música o ruido de fondo
                r'\[música\]',
                r'\[music\]',
                r'\[ruido\]',
                r'\[noise\]',
                r'\[sonido\]',
                r'\[sound\]',
                r'♪.*?♪',
                
                # Patrones de indicadores de audio no útiles
                r'\[inaudible\]',
                r'\[unclear\]',
                r'\[incomprensible\]',
                r'\(inaudible\)',
                r'\(unclear\)',
                r'\(incomprensible\)',
                
                # Patrones de timestamping o marcadores técnicos
                r'\d{1,2}:\d{2}:\d{2}',  # timestamps
                r'>> .*?',  # marcadores de speaker
                r'<.*?>',   # tags HTML/XML
                
                # Palabras sueltas muy cortas que pueden ser ruido
                r'\b[a-zA-Z]\b',  # letras sueltas
                
                # Patrones de repetición excesiva (ruido)
                r'(.{1,3})\1{5,}',  # repetición de caracteres/palabras
            ]
            
            # Limpiar el texto
            cleaned_text = transcription.strip()
            
            # Aplicar filtros de ruido
            for pattern in noise_patterns:
                cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
            
            # Normalizar espacios
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            # Log para debugging
            logger.info(f"Transcripción original: '{transcription[:100]}'")
            logger.info(f"Transcripción limpia: '{cleaned_text[:100]}'")
            
            # Validar que quede contenido útil después de la limpieza
            # Primero verificar si hay contenido significativo antes de validar longitud
            has_meaningful_content = self._contains_meaningful_content(cleaned_text)
            
            if len(cleaned_text) < 3 and not has_meaningful_content:  # Muy corto Y sin contenido relevante
                logger.warning("Transcripción muy corta después de limpieza, posible ruido")
                raise ValueError("La transcripción contiene principalmente ruido o contenido irrelevante. Por favor, graba nuevamente en un ambiente más silencioso y habla claramente.")
            
            # Validar que contenga palabras en español o números (contexto PQRS)
            if not has_meaningful_content:
                logger.warning("Transcripción no contiene contenido relevante para PQRS")
                raise ValueError("No se detectó contenido relevante para consultas PQRS. Por favor, menciona tu consulta sobre radicados, solicitudes o servicios municipales.")
            
            logger.info(f"Transcripción validada y limpiada: '{transcription[:50]}...' -> '{cleaned_text[:50]}...'")
            return cleaned_text
            
        except ValueError:
            # Re-lanzar errores de validación
            raise
        except Exception as e:
            logger.warning(f"Error limpiando transcripción: {e}")
            return transcription  # Devolver transcripción original en caso de error de limpieza
    
    def _contains_meaningful_content(self, text: str) -> bool:
        """Verifica si el texto contiene contenido significativo para PQRS"""
        import re
        
        # Palabras clave relevantes para PQRS
        pqrs_keywords = [
            'radicado', 'número', 'consulta', 'solicitud', 'queja', 'reclamo', 'sugerencia',
            'petición', 'información', 'ayuda', 'problema', 'inconveniente', 'servicio',
            'infraestructura', 'vía', 'calle', 'barrio', 'sector', 'daño', 'reparación',
            'mantenimiento', 'construcción', 'obra', 'proyecto', 'solicitar', 'reportar',
            'estado', 'seguimiento', 'respuesta', 'trámite', 'gestión', 'municipio',
            'secretaría', 'alcaldía', 'ciudadano', 'vecino', 'comunidad', 'hola', 'buenos',
            'días', 'tardes', 'noches', 'gracias', 'favor', 'necesito', 'quiero', 'deseo',
            # Agregar números que podrían ser dictados
            'veinte', 'veinticinco', 'diez', 'cero', 'uno', 'dos', 'tres', 'cuatro',
            'cinco', 'seis', 'siete', 'ocho', 'nueve'
        ]
        
        # Palabras que indican idioma no español
        english_words = [
            'hello', 'this', 'that', 'the', 'and', 'for', 'you', 'are', 'not', 'can',
            'have', 'will', 'would', 'could', 'should', 'english', 'error', 'transcription'
        ]
        
        text_lower = text.lower()
        logger.info(f"Validando contenido: '{text_lower}'")
        
        # Verificar si contiene demasiadas palabras en inglés
        english_count = sum(1 for word in english_words if word in text_lower)
        total_words = len(text_lower.split())
        
        if english_count > 2 and total_words > 3:  # Más de 2 palabras en inglés en un texto corto
            logger.info(f"Rechazado por contenido en inglés: {english_count}/{total_words}")
            return False
        
        # Verificar si contiene palabras clave de PQRS
        for keyword in pqrs_keywords:
            if keyword in text_lower:
                logger.info(f"Contenido válido encontrado por palabra clave: '{keyword}'")
                return True
        
        # Verificar si contiene números que podrían ser radicados
        if re.search(r'\d{4,}', text):  # Al menos 4 dígitos seguidos (más permisivo)
            logger.info("Contenido válido encontrado por secuencia numérica")
            return True
        
        # Verificar si contiene estructura de pregunta o solicitud en español
        question_patterns = [
            r'\b(qué|cuál|cuándo|cómo|dónde|por qué|quién)\b',
            r'\b(necesito|quiero|deseo|solicito|requiero)\b',
            r'\?',  # signos de pregunta
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, text_lower):
                logger.info(f"Contenido válido encontrado por patrón de pregunta: {pattern}")
                return True
        
        # Verificar longitud mínima y estructura básica del español
        words = text_lower.split()
        if len(words) >= 1:  # Más permisivo: al menos una palabra
            # Verificar que no sea solo números o caracteres especiales
            meaningful_words = [w for w in words if re.match(r'[a-záéíóúñü]+', w)]
            if len(meaningful_words) >= 1:
                # Si es una sola palabra, verificar que sea significativa
                if len(words) == 1:
                    # Palabras de una sola letra o muy cortas (menos de 3 caracteres) son sospechosas
                    if len(text_lower.strip()) >= 3:
                        logger.info("Contenido válido encontrado por palabra única significativa")
                        return True
                else:
                    logger.info("Contenido válido encontrado por múltiples palabras en español")
                    return True
        
        logger.info("No se encontró contenido significativo")
        return False
    
    def improve_transcription_for_radicados(self, transcription: str) -> str:
        """Mejora la transcripción para una mejor interpretación de números de radicado"""
        import re
        
        try:
            improved_text = transcription
            
            # 1. Normalizar espacios múltiples
            improved_text = re.sub(r'\s+', ' ', improved_text).strip()
            
            # 2. Detectar patrones de números dictados por separado que pueden ser radicados
            # Buscar contextos que indiquen que se está dictando un radicado
            radicado_patterns = [
                (r'(radicado)\s+(.+?)(?=\.|$|,|!|\?)', self._join_spoken_radicado),
                (r'(número)\s+(.+?)(?=\.|$|,|!|\?)', self._join_spoken_radicado),
                (r'(rad)\s+(.+?)(?=\.|$|,|!|\?)', self._join_spoken_radicado),
            ]
            
            for pattern, processor in radicado_patterns:
                matches = list(re.finditer(pattern, improved_text, re.IGNORECASE))
                # Procesar matches en orden inverso para mantener posiciones
                for match in reversed(matches):
                    full_match = match.group(0)
                    indicator = match.group(1)
                    number_text = match.group(2)
                    
                    processed_number = processor(number_text)
                    if processed_number:
                        replacement = f"{indicator} {processed_number}"
                        improved_text = improved_text[:match.start()] + replacement + improved_text[match.end():]
                        logger.info(f"Mejorado radicado dictado: '{full_match}' -> '{replacement}'")
            
            # 3. También buscar secuencias largas de números separados por espacios que podrían ser radicados
            # sin contexto específico (solo si no hay otros números largos en el texto)
            number_sequences = re.findall(r'\b(?:\d{1,2}\s+){5,}\d{1,2}\b', improved_text)
            for sequence in number_sequences:
                joined = self._join_spoken_radicado(sequence)
                if joined and len(joined) == 12 and joined.startswith('2025'):
                    improved_text = improved_text.replace(sequence, joined)
                    logger.info(f"Mejorada secuencia de números: '{sequence}' -> '{joined}'")
            
            return improved_text
            
        except Exception as e:
            logger.warning(f"Error mejorando transcripción: {e}")
            return transcription  # Devolver transcripción original en caso de error
    
    def _join_spoken_radicado(self, number_text: str) -> str:
        """Une números dictados por separado en una secuencia continua de radicado"""
        import re
        
        # Limpiar el texto
        text = number_text.lower().strip()
        
        # Reemplazar palabras numéricas por dígitos
        number_words = {
            'cero': '0', 'uno': '1', 'dos': '2', 'tres': '3', 'cuatro': '4',
            'cinco': '5', 'seis': '6', 'siete': '7', 'ocho': '8', 'nueve': '9',
            'diez': '10', 'once': '11', 'doce': '12', 'trece': '13', 'catorce': '14',
            'quince': '15', 'dieciséis': '16', 'diecisiete': '17', 'dieciocho': '18',
            'diecinueve': '19', 'veinte': '20', 'veintiuno': '21', 'veintidós': '22',
            'veintitrés': '23', 'veinticuatro': '24', 'veinticinco': '25', 'veintiséis': '26',
            'veintisiete': '27', 'veintiocho': '28', 'veintinueve': '29', 'treinta': '30'
        }
        
        # Reemplazar palabras por números
        for word, number in number_words.items():
            text = re.sub(r'\b' + word + r'\b', number, text)
        
        # Extraer todos los números del texto
        numbers = re.findall(r'\d+', text)
        
        if not numbers:
            return None
        
        # Unir todos los números encontrados
        combined_number = ''.join(numbers)
        
        # Verificar que la longitud sea apropiada para un radicado (12 dígitos)
        if len(combined_number) == 12 and combined_number.startswith('2025'):
            return combined_number
        
        # Si la longitud es menor pero tenemos una estructura apropiada, intentar formatear
        if len(combined_number) < 12 and len(combined_number) >= 8:
            # Rellenar con ceros al final para completar 12 dígitos
            padded = combined_number.ljust(12, '0')
            if padded.startswith('2025'):
                return padded
        
        return None
    
    def validate_audio_format(self, filename: str) -> bool:
        """Valida si el formato de audio es soportado"""
        if not filename:
            logger.warning("Nombre de archivo vacío, asumiendo formato válido")
            return True  # Permitir archivos sin nombre específico (como recording.wav)
        
        extension = Path(filename).suffix.lower().lstrip('.')
        if not extension:
            logger.warning("Sin extensión, asumiendo formato válido")
            return True  # Permitir archivos sin extensión específica
        
        supported_formats = self.strategy.get_supported_formats()
        is_valid = extension in supported_formats
        
        if not is_valid:
            logger.warning(f"Formato de audio no soportado: {extension}. Formatos soportados: {supported_formats}")
        else:
            logger.info(f"Formato de audio válido: {extension}")
        
        return is_valid
    
    def change_strategy(self, strategy: TranscriptionStrategy):
        """Cambia la estrategia de transcripción"""
        self.strategy = strategy
        logger.info("Estrategia de transcripción cambiada")
    
    def get_supported_formats(self) -> List[str]:
        """Obtiene formatos soportados por la estrategia actual"""
        return self.strategy.get_supported_formats()

class AudioServiceFactory:
    """Factory para crear servicios de audio"""
    
    @staticmethod
    def create_openai_service(api_key: str, model: str = 'whisper-1') -> AudioService:
        """Crea un servicio de audio con estrategia OpenAI"""
        strategy = OpenAIWhisperStrategy(api_key, model)
        return AudioService(strategy)
    
    @staticmethod
    def create_faster_whisper_service(model: str = 'large-v3', compute_type: str = "int8") -> AudioService:
        """Crea un servicio de audio con estrategia Faster Whisper"""
        strategy = FasterWhisperStrategy(model, compute_type)
        return AudioService(strategy)
