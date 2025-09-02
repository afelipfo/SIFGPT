# TUNRAG - Sistema RAG para Consulta de PQRS

Sistema de Recuperación Aumentada de Información (RAG) especializado en la consulta y gestión de PQRS (Peticiones, Quejas, Reclamos, Sugerencias y Denuncias) almacenadas en el histórico de la Alcaldía de Medellín.

## 🚀 Características Principales

- **Sistema RAG Unificado**: Consultas inteligentes sobre histórico de PQRS
- **Procesamiento de Audio**: Transcripción y análisis de PQRS por voz
- **Clasificación Automática**: Categorización inteligente de PQRS usando IA
- **API REST Completa**: Endpoints unificados para todas las funcionalidades
- **Interfaz Web Moderna**: Frontend responsive y fácil de usar
- **Logging Centralizado**: Sistema de logs robusto para monitoreo

## 🏗️ Arquitectura del Sistema

```
TUNRAG/
├── src/                          # Código fuente principal
│   ├── controllers/              # Controladores de API unificados
│   │   ├── historico_controller.py    # Controlador unificado de histórico
│   │   └── pqrs_controller.py         # Controlador de PQRS
│   ├── services/                 # Servicios de negocio
│   │   ├── historico_query_service.py # Servicio unificado de histórico
│   │   ├── pqrs_orchestrator_service.py # Orquestador principal
│   │   ├── audio_service.py      # Servicio de audio
│   │   ├── pqrs_classifier_service.py # Clasificación de PQRS
│   │   └── response_generator_service.py # Generación de respuestas
│   ├── models/                   # Modelos de datos
│   ├── repositories/             # Acceso a datos
│   ├── utils/                    # Utilidades (logger, etc.)
│   └── config/                   # Configuración del sistema
├── templates/                    # Plantillas HTML
├── static/                       # Archivos estáticos (CSS, JS, imágenes)
├── input/                        # Datos de entrada
│   ├── historico/               # Archivos de histórico de PQRS
│   ├── prompts/                 # Prompts para IA
│   └── plantillas_solucion/     # Plantillas de respuestas
├── logs/                        # Archivos de log
├── app.py                       # Aplicación principal Flask

└── requirements.txt              # Dependencias de Python
```

## 🔧 Instalación y Configuración

### Requisitos Previos
- Python 3.11+
- OpenAI API Key
- Dependencias del sistema (ver requirements.txt)

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd TUNRAG
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   # Editar .env con tu OpenAI API Key
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

## 📡 API Endpoints

### Histórico de PQRS (Unificado)

- `POST /api/historico/consulta` - Consulta inteligente
- `GET /api/historico/radicado/<numero>` - Consulta por radicado
- `POST /api/historico/buscar/texto` - Búsqueda por texto
- `POST /api/historico/buscar/nombre` - Búsqueda por nombre
- `POST /api/historico/consulta-avanzada` - Consulta con filtros múltiples
- `POST /api/historico/sugerencias` - Sugerencias de búsqueda
- `GET /api/historico/filtros-disponibles` - Filtros disponibles
- `GET /api/historico/estadisticas` - Estadísticas del histórico
- `GET /api/historico/ayuda` - Ayuda del sistema
- `GET /api/historico/resumen` - Resumen del histórico

### PQRS

- `POST /api/pqrs/procesar-audio` - Procesar PQRS desde audio
- `POST /api/pqrs/procesar-texto` - Procesar PQRS desde texto
- `GET /api/pqrs/health` - Estado del servicio

### Sistema

- `GET /` - Interfaz web principal
- `GET /api/health` - Estado general del sistema
- `GET /test/historico` - Pruebas del servicio histórico
- `GET /test/advanced-historico` - Pruebas de funcionalidades avanzadas

## 🧪 Pruebas

Verificar el estado del sistema:

```bash
curl http://localhost:5000/api/health
```

Este comando verifica que todos los servicios estén funcionando correctamente.

## 🚀 Despliegue

### Docker

```bash
# Construir imagen
docker build -t tunrag .

# Ejecutar contenedor
docker run -p 5000:5000 --env-file .env tunrag
```

### Docker Compose

```bash
docker-compose up -d
```

## 📊 Funcionalidades del Sistema RAG

### 1. Consultas Inteligentes
- **Búsqueda por Texto**: Búsqueda semántica en descripciones de PQRS
- **Búsqueda por Radicado**: Consulta directa por número de radicado
- **Búsqueda por Nombre**: Localización por nombre del solicitante

### 2. Consultas Avanzadas
- **Filtros Múltiples**: Combinación de criterios de búsqueda
- **Ordenamiento**: Resultados ordenados por diferentes campos
- **Paginación**: Control del número de resultados
- **Filtros de Fecha**: Búsquedas por rangos temporales

### 3. Análisis de Datos
- **Estadísticas**: Resúmenes cuantitativos del histórico
- **Tendencias**: Análisis temporal de PQRS
- **Clasificación**: Distribución por tipos y estados
- **Geolocalización**: Análisis por barrios y unidades

### 4. Procesamiento de Audio
- **Transcripción**: Conversión de voz a texto
- **Clasificación**: Análisis automático del tipo de PQRS
- **Respuesta Automática**: Generación de respuestas contextuales

## 🔒 Seguridad

- Validación de entrada en todos los endpoints
- Manejo seguro de archivos de audio
- Logging de todas las operaciones
- Configuración de variables de entorno

## 📝 Logging

El sistema utiliza un logger centralizado que registra:
- Operaciones del usuario
- Errores del sistema
- Métricas de rendimiento
- Acceso a datos

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Ejecutar pruebas
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

## 🆘 Soporte

Para soporte técnico o consultas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar la documentación de la API

## 🔄 Historial de Versiones

### v2.0.0 (Actual)
- **Unificación completa** de servicios de histórico
- **Eliminación** de archivos duplicados
- **Consolidación** de controladores
- **Sistema de pruebas unificado**
- **Limpieza** de dependencias no utilizadas

### v1.0.0
- Versión inicial del sistema
- Funcionalidades básicas de PQRS
- Servicios separados de histórico

---

**TUNRAG** - Transformando la gestión de PQRS con Inteligencia Artificial
