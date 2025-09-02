# TUNRAG - Sistema RAG para Consulta de PQRS

Sistema de Recuperación Aumentada de Información (RAG) especializado en la consulta y gestión de PQRS (Peticiones, Quejas, Reclamos, Sugerencias y Denuncias) almacenadas en el histórico de la Alcaldía de Medellín.

## 🚀 Características Principales

- **Sistema RAG Unificado**: Consultas inteligentes sobre histórico de PQRS
- **Procesamiento de Audio**: Transcripción y análisis de PQRS por voz
- **Clasificación Automática**: Categorización inteligente de PQRS usando IA
- **API REST Completa**: Endpoints unificados para todas las funcionalidades
- **Interfaz Web Moderna**: Frontend responsive y fácil de usar
- **Logging Centralizado**: Sistema de logs robusto para monitoreo

## 🏗️ Arquitectura del Sistema Optimizada

### Separación entre Arquitectura y Orquestación

#### **Capa de Arquitectura (Estructura Base)**
```
SIFGPT/
├── src/                          # Código fuente principal (100% funcional)
│   ├── controllers/              # Controladores REST por dominio
│   │   ├── historico_controller.py    # Endpoints de consulta histórica
│   │   └── pqrs_controller.py         # Endpoints de procesamiento PQRS
│   ├── services/                 # Servicios de negocio especializados
│   │   ├── audio_service.py           # Transcripción de audio
│   │   ├── historico_query_service.py # Consultas inteligentes de histórico
│   │   ├── pqrs_classifier_service.py # Clasificación automática de PQRS
│   │   ├── response_generator_service.py # Generación de respuestas contextuales
│   │   └── pqrs_orchestrator_service.py # ⭐ ORQUESTADOR PRINCIPAL
│   ├── models/                   # Modelos de datos tipados
│   │   └── pqrs_model.py              # PQRSData, PQRSHistorico, AudioTranscription
│   ├── repositories/             # Acceso y gestión de datos
│   │   └── pqrs_repository.py         # PQRSRepository, PromptRepository
│   ├── utils/                    # Utilidades del sistema
│   │   └── logger.py                  # Sistema de logging centralizado
│   └── config/                   # Configuración centralizada
│       └── config.py                  # Configuración unificada del sistema
├── templates/                    # Frontend optimizado
│   └── index.html                     # Interfaz web unificada
├── static/                       # Archivos estáticos optimizados
│   ├── css/styles.css                 # Estilos unificados y responsivos
│   ├── js/sifgpt-unified.js          # JavaScript unificado (sin duplicados)
│   └── images/logo-medellin.png       # Logo oficial
├── input/                        # Datos de entrada (solo utilizados)
│   ├── audios/                        # Directorio para procesamiento temporal de audio
│   │   └── .gitkeep                   # Mantiene la carpeta en el repositorio
│   ├── historico/                     # Archivos de histórico activos
│   │   └── historico2.xlsx            # Histórico principal en formato Excel
│   ├── prompts/                       # Prompts de IA (solo utilizados)
│   │   ├── categorias.txt, entidades.txt, estructura_json.txt
│   │   ├── faqs.txt, respuestas_faqs.txt
│   │   └── sys_prompt.txt, sys_prompt_faqs.txt, sys_prompt_solucion.txt
│   └── plantillas_solucion/           # Plantillas de respuesta
│       └── plantilla.txt              # Plantilla base de respuestas
├── logs/                         # Sistema de logging
│   └── tunrag.log                     # Logs de la aplicación
├── app.py                        # Aplicación principal Flask
├── requirements.txt              # Dependencias optimizadas
├── Dockerfile                    # Configuración Docker
└── docker-compose.yml            # Orquestación de contenedores
```

#### **Capa de Orquestación (Flujo de Datos)**
- **PQRSOrchestratorService**: Coordina todos los servicios especializados
- **Controllers**: Enrutan requests HTTP a servicios apropiados
- **Blueprints**: Organizan endpoints por funcionalidad (PQRS vs Histórico)

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
