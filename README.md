# SIF-GPT - Sistema Inteligente de PQRS para la Secretaría de Infraestructura Física

**SIF-GPT** es un asistente virtual inteligente desarrollado para la **Secretaría de Infraestructura Física de la Alcaldía de Medellín**. El sistema combina procesamiento de lenguaje natural con inteligencia artificial para optimizar la gestión y consulta de PQRS (Peticiones, Quejas, Reclamos, Sugerencias y Denuncias).

## 🎯 Propósito del Sistema

SIF-GPT fue diseñado para automatizar y mejorar la gestión de PQRS en la Secretaría de Infraestructura Física, proporcionando:

- **Consultas inteligentes** sobre un histórico de **10,617 registros** de PQRS
- **Procesamiento automático** de solicitudes por texto y audio
- **Clasificación inteligente** de PQRS según categorías institucionales
- **Generación de respuestas** contextualizadas y personalizadas
- **Interfaz web moderna** para funcionarios y ciudadanos

## 🚀 Características Principales

### 🧠 Inteligencia Artificial Integrada
- **GPT-4** para comprensión y generación de respuestas naturales
- **Whisper** para transcripción automática de audio
- **Análisis semántico** para clasificación automática de PQRS
- **Memoria conversacional** para mantener contexto entre interacciones

### 📊 Gestión Avanzada de Datos
- Base de datos histórica de **10,617 PQRS** en formato Excel
- **5 categorías principales**: Solicitud de Interés Particular, Trámite, Solicitud de Interés General, Solicitud de Información, Tutela
- **Estados de seguimiento**: EVACUADO, SIN RESPUESTA, DEVOLUCIÓN BACK OFFICE, SOLICITUD DE PRÓRROGA
- **Análisis por barrios** y unidades especializadas de Medellín

### 🎤 Procesamiento Multimodal
- **Transcripción de audio** en múltiples formatos (MP3, WAV, MP4, etc.)
- **Procesamiento de texto** directo
- **Análisis automático** del contenido para clasificación

### 🌐 Interfaz Web Completa
- **Diseño corporativo** con identidad visual de la Alcaldía de Medellín
- **Responsive design** compatible con dispositivos móviles
- **Accesibilidad** optimizada para usuarios diversos

## 🏗️ Arquitectura del Sistema

```
SIFGPT/
├── src/                          # Código fuente principal
│   ├── controllers/              # Controladores REST
│   │   ├── historico_controller.py    # Endpoints de consulta histórica
│   │   └── pqrs_controller.py         # Endpoints de procesamiento PQRS
│   ├── services/                 # Servicios de negocio
│   │   ├── audio_service.py           # Transcripción de audio (Whisper)
│   │   ├── historico_query_service.py # Consultas inteligentes de histórico
│   │   ├── pqrs_classifier_service.py # Clasificación automática IA
│   │   ├── response_generator_service.py # Generación de respuestas GPT-4
│   │   └── pqrs_orchestrator_service.py # Orquestador principal
│   ├── models/                   # Modelos de datos tipados
│   │   └── pqrs_model.py              # PQRSData, AudioTranscription
│   ├── repositories/             # Acceso a datos
│   │   └── pqrs_repository.py         # Gestión de Excel y prompts
│   ├── utils/                    # Utilidades del sistema
│   │   └── logger.py                  # Sistema de logging
│   └── config/                   # Configuración
│       └── config.py                  # Config centralizada
├── templates/                    # Frontend web
│   └── index.html                     # Interfaz principal SIF-GPT
├── static/                       # Recursos estáticos
│   ├── css/styles.css                 # Estilos corporativos
│   ├── js/sifgpt-unified.js          # JavaScript de la aplicación
│   └── images/logo-medellin.png       # Logo oficial
├── input/                        # Datos del sistema
│   ├── audios/                        # Archivos de audio temporales
│   ├── historico/                     # Base de datos PQRS
│   │   └── historico2.xlsx            # 10,617 registros históricos
│   ├── prompts/                       # Prompts de IA especializados
│   │   ├── sys_prompt.txt             # Personalidad de SIF-GPT
│   │   ├── categorias.txt             # Categorías de PQRS
│   │   └── ...                        # Otros prompts especializados
│   └── plantillas_solucion/           # Plantillas de respuesta
├── app.py                        # Aplicación Flask principal
├── requirements.txt              # Dependencias Python
├── Dockerfile                    # Contenedor Docker
└── docker-compose.yml            # Orquestación de servicios
```

### 🔄 Flujo de Procesamiento
1. **Recepción**: El sistema recibe PQRS por texto o audio
2. **Transcripción**: Si es audio, Whisper convierte a texto
3. **Clasificación**: GPT-4 analiza y categoriza automáticamente
4. **Consulta**: Se buscan casos similares en el histórico
5. **Respuesta**: Se genera una respuesta contextualizada
6. **Seguimiento**: Se registra la interacción para análisis

## 🔧 Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- OpenAI API Key (para GPT-4 y Whisper)
- Windows/Linux/macOS

### Instalación Rápida

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/afelipfo/SIFGPT.git
   cd SIFGPT
   ```

2. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**

   ```bash
   # Crear archivo .env en la raíz del proyecto
   OPENAI_API_KEY=tu_api_key_aqui
   SECRET_KEY=tu_secret_key_aqui
   DEBUG=True
   ```

4. **Ejecutar la aplicación**

   ```bash
   python app.py
   ```

5. **Acceder al sistema**
   - Abrir navegador en: `http://localhost:5000`
   - La interfaz SIF-GPT estará disponible

## 📡 API Endpoints

### 🔍 Consultas de Histórico PQRS

- `POST /api/historico/consulta` - Consulta inteligente con IA
- `GET /api/historico/radicado/<numero>` - Consulta por número de radicado
- `POST /api/historico/buscar/texto` - Búsqueda por contenido de texto
- `POST /api/historico/buscar/nombre` - Búsqueda por nombre del solicitante
- `POST /api/historico/consulta-avanzada` - Consulta con filtros múltiples
- `POST /api/historico/sugerencias` - Sugerencias inteligentes de búsqueda
- `GET /api/historico/filtros-disponibles` - Filtros disponibles en el sistema
- `GET /api/historico/estadisticas` - Estadísticas del histórico PQRS
- `GET /api/historico/resumen` - Resumen ejecutivo del histórico

### 📝 Procesamiento de PQRS

- `POST /api/pqrs/procesar-audio` - Procesar PQRS desde archivo de audio
- `POST /api/pqrs/procesar-texto` - Procesar PQRS desde texto directo
- `GET /api/pqrs/health` - Estado del servicio de procesamiento

### 🏥 Sistema y Monitoreo

- `GET /` - Interfaz web principal de SIF-GPT
- `GET /api/health` - Estado general del sistema
- `GET /test/historico` - Pruebas del servicio de histórico
- `GET /test/advanced-historico` - Pruebas avanzadas del sistema

## 🧪 Verificación del Sistema

Para verificar que SIF-GPT está funcionando correctamente:

```bash
# Verificar estado general
curl http://localhost:5000/api/health

# Probar consulta de ejemplo
curl -X POST http://localhost:5000/api/historico/consulta \
  -H "Content-Type: application/json" \
  -d '{"query": "problemas con vías en El Poblado"}'
```

## 🚀 Despliegue

### Docker

```bash
# Construir imagen
docker build -t sifgpt .

# Ejecutar contenedor
docker run -p 5000:5000 --env-file .env sifgpt
```

### Docker Compose

```bash
docker-compose up -d
```

## 📊 Funcionalidades Principales

### 1. Consultas Inteligentes

- **Búsqueda Semántica**: Utiliza IA para entender el contexto y la intención
- **Búsqueda por Radicado**: Consulta directa por número de radicado específico
- **Búsqueda por Nombre**: Localización por nombre del solicitante
- **Búsqueda por Texto**: Análisis de contenido en descripciones de PQRS

### 2. Consultas Avanzadas

- **Filtros Múltiples**: Combinación de criterios (fecha, estado, barrio, etc.)
- **Ordenamiento Inteligente**: Resultados priorizados por relevancia
- **Paginación Optimizada**: Control eficiente de resultados grandes
- **Filtros Temporales**: Búsquedas por rangos de fechas específicos

### 3. Análisis de Datos

- **Estadísticas en Tiempo Real**: Resúmenes cuantitativos actualizados
- **Análisis por Barrios**: Distribución geográfica de PQRS en Medellín
- **Análisis por Estados**: Seguimiento de EVACUADO, SIN RESPUESTA, etc.
- **Tendencias Temporales**: Patrones de solicitudes a lo largo del tiempo

### 4. Procesamiento de Audio

- **Transcripción Automática**: Conversión de voz a texto con Whisper
- **Clasificación Inteligente**: Análisis automático del tipo de PQRS
- **Múltiples Formatos**: Soporte para MP3, WAV, MP4, M4A, FLAC, OGG
- **Respuesta Contextualizada**: Generación automática de respuestas relevantes

### 5. Asistente Virtual SIF-GPT

- **Personalidad Especializada**: Entrenado específicamente para infraestructura física
- **Memoria Conversacional**: Mantiene contexto durante toda la sesión
- **Respuestas Personalizadas**: Basadas en el histórico y contexto específico
- **Seguimiento Inteligente**: Preguntas de clarificación cuando es necesario

## 🔒 Seguridad y Privacidad

- **Validación de Entrada**: Todos los endpoints validan datos de entrada
- **Manejo Seguro de Archivos**: Procesamiento temporal de audio sin almacenamiento
- **Logging Completo**: Registro de todas las operaciones para auditoría
- **Variables de Entorno**: Configuración segura de API keys

## � Monitoreo y Logging

El sistema incluye logging centralizado que registra:

- **Operaciones de Usuario**: Consultas, búsquedas y procesamientos
- **Errores del Sistema**: Fallos y excepciones para debugging
- **Métricas de Rendimiento**: Tiempos de respuesta y uso de recursos
- **Acceso a Datos**: Consultas al histórico PQRS para auditoría

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Implementar cambios y pruebas
4. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Crear Pull Request

## 📄 Licencia

Este proyecto es propiedad de la **Alcaldía de Medellín - Secretaría de Infraestructura Física**.
Desarrollado para uso interno de la administración municipal.

## 🆘 Soporte Técnico

Para soporte técnico o consultas sobre SIF-GPT:

- **Documentación**: Revisar este README y comentarios en el código
- **Contacto**: Equipo de desarrollo de la Secretaría de Infraestructura Física

## 📊 Estadísticas del Proyecto

- **Base de Datos**: 10,617 registros históricos de PQRS
- **Categorías**: 5 tipos principales de PQRS
- **Estados**: 4+ estados de seguimiento diferentes
- **Barrios**: Cobertura completa de Medellín
- **Tecnología**: Flask + OpenAI GPT-4 + Whisper
- **Idioma**: Español (Colombia)

## 🔄 Historial de Versiones

### v1.0.0 (2024-09-10) - Primera Versión Estable

**🎉 Características Principales Implementadas:**

- ✅ **Sistema SIF-GPT Completo**: Asistente virtual especializado para PQRS
- ✅ **Procesamiento de Audio**: Transcripción automática con Whisper
- ✅ **Consultas Inteligentes**: Sistema RAG con GPT-4 para búsquedas semánticas
- ✅ **Base de Datos Histórica**: 10,617 registros de PQRS integrados
- ✅ **Clasificación Automática**: IA para categorizar PQRS automáticamente
- ✅ **Interfaz Web Completa**: Frontend corporativo responsive
- ✅ **API REST Completa**: 15+ endpoints para todas las funcionalidades
- ✅ **Sistema de Logging**: Monitoreo y auditoría completa
- ✅ **Configuración Docker**: Despliegue containerizado listo para producción

**🏗️ Arquitectura Implementada:**

- **Orquestador Principal**: PQRSOrchestratorService coordina todos los servicios
- **Servicios Especializados**: Audio, Clasificación, Generación de Respuestas, Consultas
- **Controladores REST**: Endpoints organizados por funcionalidad
- **Repositorios de Datos**: Acceso optimizado a Excel y prompts de IA
- **Configuración Centralizada**: Gestión unificada de configuración

**📈 Capacidades del Sistema:**

- Procesamiento de 7+ formatos de audio diferentes
- Consultas en lenguaje natural sobre 10,617 PQRS históricas
- Clasificación automática en 5 categorías institucionales
- Análisis por barrios, estados y unidades de Medellín
- Respuestas contextualizadas y personalizadas
- Interfaz bilingüe optimizada para funcionarios públicos

---

**SIF-GPT v1.0.0** - Transformando la gestión de PQRS con Inteligencia Artificial  
*Secretaría de Infraestructura Física - Alcaldía de Medellín*
