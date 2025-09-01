# TUNRAG - Sistema de PQRS con Inteligencia Artificial

## 🏗️ Arquitectura del Sistema

TUNRAG es un sistema moderno de procesamiento de PQRS (Peticiones, Quejas, Reclamos, Sugerencias y Denuncias) que utiliza inteligencia artificial para clasificar y responder automáticamente a las solicitudes de los ciudadanos.

### **Arquitectura Refactorizada (v2.0.0)**

El sistema ha sido completamente refactorizado siguiendo principios de arquitectura de software modernos:

```
src/
├── config/          # Configuración centralizada
├── models/          # Modelos de datos
├── services/        # Servicios de negocio
├── repositories/    # Acceso a datos
├── controllers/     # Controladores de API
└── utils/           # Utilidades comunes
```

### **Patrones Arquitectónicos Implementados**

- **Repository Pattern**: Para acceso a datos
- **Strategy Pattern**: Para diferentes estrategias de transcripción de audio
- **Factory Pattern**: Para creación de servicios
- **MVC Pattern**: Para separación de responsabilidades
- **Dependency Injection**: Para inyección de dependencias

## 🚀 Instalación y Ejecución

### **Requisitos Previos**

- Python 3.12+
- Conda o Miniconda
- OpenAI API Key

### **Instalación**

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd TUNRAG
```

2. **Crear entorno conda**
```bash
conda env create -f environment.yml
conda activate poc_dd
```

3. **Configurar variables de entorno**
```bash
# Crear archivo .env
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
```

4. **Ejecutar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🔧 Configuración

### **Variables de Entorno**

- `OPENAI_API_KEY`: Clave API de OpenAI (requerida)
- `OPENAI_BASE_URL`: URL base de OpenAI (opcional)
- `OPENAI_MODEL`: Modelo de OpenAI a usar (default: gpt-4o)
- `WHISPER_MODEL`: Modelo de Whisper a usar (default: whisper-1)
- `DEBUG`: Modo debug (default: True)
- `LOG_LEVEL`: Nivel de logging (default: INFO)

### **Estructura de Directorios**

```
input/
├── audios/              # Archivos de audio
├── historico/           # Base de datos histórica
├── prompts/             # Prompts del sistema
└── plantillas_solucion/ # Plantillas de respuesta

logs/                    # Archivos de log
static/                  # Archivos estáticos
templates/               # Plantillas HTML
```

## 📡 API Endpoints

### **Endpoints Principales**

- `GET /` - Página principal
- `POST /get_response` - Procesar PQRS desde texto
- `POST /process_audio` - Procesar PQRS desde audio
- `POST /transcribe_audio` - Solo transcribir audio

### **Endpoints del Sistema**

- `GET /health` - Verificación básica de salud
- `GET /health/detailed` - Verificación detallada de salud
- `GET /system/status` - Estado del sistema
- `POST /system/refresh` - Refrescar cachés
- `GET /system/validate` - Validar sistema

## 🎯 Funcionalidades

### **Procesamiento de PQRS**

1. **Clasificación Automática**: Identifica tipo de PQRS usando IA
2. **Extracción de Información**: Extrae datos relevantes del texto
3. **Generación de Respuestas**: Genera respuestas contextuales
4. **Manejo de FAQs**: Responde preguntas frecuentes automáticamente
5. **Consulta de Histórico**: Verifica estado de PQRS existentes

### **Transcripción de Audio**

- Soporte para múltiples formatos de audio
- Estrategias configurables (OpenAI Whisper, Faster Whisper)
- Validación de formatos
- Procesamiento en tiempo real

### **Gestión de Datos**

- Caché inteligente de prompts y plantillas
- Repositorio de datos histórico
- Estadísticas del sistema
- Validación de integridad

## 🔍 Monitoreo y Logging

### **Sistema de Logging**

- Logging centralizado y configurable
- Diferentes niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Logs en consola y archivo
- Rotación automática de logs

### **Monitoreo del Sistema**

- Endpoints de salud
- Estado de servicios
- Métricas de caché
- Validación de configuración

## 🧪 Testing

### **Modo de Prueba**

```python
# En el código
result = orchestrator.process_text_pqrs("texto de prueba", test=True)
```

### **Validación del Sistema**

```bash
curl http://localhost:5000/system/validate
```

## 📊 Métricas y Rendimiento

### **Indicadores Clave**

- Tiempo de respuesta promedio
- Tasa de éxito en clasificación
- Uso de caché
- Estado de servicios externos

### **Optimizaciones**

- Caché de prompts y plantillas
- Lazy loading de datos
- Estrategias configurables de transcripción
- Manejo eficiente de errores

## 🔒 Seguridad

### **Medidas Implementadas**

- Validación de entrada
- Manejo seguro de archivos
- Logging de auditoría
- Manejo de errores sin exposición de información sensible

## 🚀 Roadmap

### **Próximas Funcionalidades**

- [ ] Implementación de RAG (Retrieval Augmented Generation)
- [ ] Integración con LangChain
- [ ] Dashboard de administración
- [ ] API de webhooks
- [ ] Sistema de notificaciones
- [ ] Análisis avanzado de sentimientos

## 🤝 Contribución

### **Estándares de Código**

- Seguir principios SOLID
- Documentación completa
- Tests unitarios
- Logging consistente
- Manejo de errores robusto

### **Proceso de Desarrollo**

1. Crear feature branch
2. Implementar funcionalidad
3. Agregar tests
4. Actualizar documentación
5. Crear pull request

## 📝 Licencia

Este proyecto está bajo la licencia [LICENCIA]. Ver el archivo LICENSE para más detalles.

## 📞 Contacto

Para soporte técnico o consultas:
- Email: [email]
- Documentación: [docs-url]
- Issues: [github-issues]

---

**TUNRAG v2.0.0** - Sistema de PQRS con Inteligencia Artificial
