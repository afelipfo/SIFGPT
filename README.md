# 🚀 SIFGPT - Sistema de PQRS Inteligente Unificado

**Sistema automatizado para procesamiento de PQRS (Peticiones, Quejas, Reclamos y Sugerencias) usando Inteligencia Artificial - TODO EN UNA SOLA INTERFAZ.**

## ✨ **CARACTERÍSTICAS PRINCIPALES**

### 🤖 **Procesamiento Inteligente**
- **Clasificación automática** de PQRS usando IA
- **Generación de respuestas** contextuales e inteligentes
- **Procesamiento de audio** con transcripción automática
- **Análisis semántico** de consultas

### 📊 **Sistema de Histórico**
- **Consultas inteligentes** al histórico de PQRS
- **Búsqueda avanzada** con múltiples filtros
- **Estadísticas** y análisis de datos
- **Dashboard avanzado** para consultas complejas

### 🎯 **Funcionalidades Core**
- **INTERFAZ UNIFICADA** - Todo en un solo localhost:5000
- **API REST completa** con endpoints documentados
- **Interfaz web moderna** y responsive con pestañas
- **Grabación de audio** integrada
- **Sistema de logging** robusto
- **Arquitectura modular** y escalable

## 🏗️ **ARQUITECTURA UNIFICADA**

```
SIFGPT/
├── 📁 src/                    # Código fuente del backend
│   ├── 🎮 controllers/        # Controladores de la API
│   ├── 🏗️ models/            # Modelos de datos
│   ├── 🔧 services/           # Lógica de negocio
│   ├── 💾 repositories/       # Acceso a datos
│   ├── ⚙️ config/            # Configuración del sistema
│   └── 🛠️ utils/             # Utilidades y logging
├── 🌐 templates/              # Plantilla HTML unificada
├── 🎨 static/                 # CSS, JS e imágenes
│   └── js/
│       └── sifgpt-unified.js  # JavaScript unificado
├── 📁 input/                  # Datos y archivos de entrada
├── 📊 notebooks/              # Jupyter notebooks de análisis
└── 🐳 Docker/                 # Configuración de contenedores
```

## 🚀 **INSTALACIÓN Y CONFIGURACIÓN**

### **Requisitos Previos**
- Python 3.11+
- pip o conda
- OpenAI API Key (opcional para desarrollo)

### **1. Clonar el repositorio**
```bash
git clone <repository-url>
cd SIFGPT
```

### **2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **3. Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tu configuración
```

### **4. Ejecutar la aplicación**
```bash
python app.py
```

## 🔧 **CONFIGURACIÓN**

### **Variables de Entorno (.env)**
```env
# Configuración de la aplicación
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
LOG_LEVEL=INFO

# Configuración de OpenAI
OPENAI_API_KEY=tu-api-key-de-openai
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
WHISPER_MODEL=whisper-1
```

## 🌐 **INTERFAZ UNIFICADA**

### **Una sola URL: http://localhost:5000**

Tu aplicación ahora tiene **TODO en un solo lugar** con pestañas de navegación:

#### **1. 🗨️ PQRS Chat** (Pestaña principal)
- **Chat inteligente** para procesar PQRS
- **Grabación de audio** integrada
- **Transcripción automática** con IA
- **Respuestas contextuales** del sistema

#### **2. 📚 Histórico**
- **Búsqueda por radicado**
- **Búsqueda por texto**
- **Búsqueda por nombre**
- **Resultados en tiempo real**

#### **3. 📊 Dashboard Avanzado**
- **Métricas en tiempo real**
- **Búsquedas avanzadas** con filtros
- **Estadísticas** del sistema
- **Visualización** de datos

#### **4. ⚙️ Sistema**
- **Estado de servicios**
- **Mantenimiento** del sistema
- **Logs** y monitoreo
- **Validación** del sistema

## 📡 **API ENDPOINTS**

### **PQRS**
- `POST /api/pqrs/process-text` - Procesar PQRS desde texto
- `POST /api/pqrs/process-audio` - Procesar PQRS desde audio
- `POST /api/pqrs/transcribe-audio` - Transcribir solo audio
- `GET /api/pqrs/status` - Estado del sistema

### **Histórico**
- `POST /api/historico/consulta` - Consulta inteligente
- `GET /api/historico/radicado/<numero>` - Por número de radicado
- `POST /api/historico/buscar/texto` - Búsqueda por texto
- `POST /api/historico/buscar/nombre` - Búsqueda por nombre

### **Histórico Avanzado**
- `POST /api/advanced-historico/consulta-avanzada` - Consultas complejas
- `GET /api/advanced-historico/sugerencias` - Sugerencias de búsqueda

### **Sistema**
- `GET /api/health` - Verificación de salud
- `GET /test/historico` - Pruebas del histórico
- `GET /test/advanced-historico` - Pruebas avanzadas

## 🎮 **USO DE LA INTERFAZ UNIFICADA**

### **Acceso Principal**
1. **Abrir** `http://localhost:5000`
2. **Navegar** entre pestañas usando el menú superior
3. **Usar todas las funcionalidades** sin cambiar de página

### **Flujo de Trabajo Recomendado**
1. **PQRS Chat**: Procesar nuevas solicitudes
2. **Histórico**: Consultar casos existentes
3. **Dashboard**: Analizar métricas y tendencias
4. **Sistema**: Monitorear estado y mantenimiento

## 🧪 **PRUEBAS Y VERIFICACIÓN**

### **Ejecutar Pruebas Completas**
```bash
python test_complete_functionality.py
```

### **Verificar Estado del Sistema**
```bash
curl http://localhost:5000/api/health
```

### **Acceso a la Interfaz**
- **Frontend**: http://localhost:5000
- **Backend**: http://localhost:5000/api
- **Tests**: http://localhost:5000/test

## 🐳 **DOCKER**

### **Construir imagen**
```bash
docker build -t sifgpt .
```

### **Ejecutar contenedor**
```bash
docker run -p 5000:5000 sifgpt
```

### **Usar docker-compose**
```bash
docker-compose up -d
```

## 📊 **ESTADO DEL PROYECTO**

### ✅ **COMPONENTES FUNCIONALES**
- **Configuración**: 100% funcional
- **Servicios**: 100% funcional
- **Controladores**: 100% funcional
- **Modelos**: 100% funcional
- **Repositorios**: 100% funcional
- **API REST**: 100% funcional
- **Interfaz Unificada**: 100% funcional
- **Sistema de Audio**: 100% funcional
- **Sistema de Logging**: 100% funcional

### 🎯 **VEREDICTO FINAL**
**SIFGPT está 100% FUNCIONAL con INTERFAZ UNIFICADA.**

### 🆕 **NOVEDADES DE LA VERSIÓN UNIFICADA**
- ✅ **Una sola interfaz** para todas las funcionalidades
- ✅ **Navegación por pestañas** intuitiva
- ✅ **Frontend consolidado** en un solo archivo
- ✅ **JavaScript unificado** para toda la funcionalidad
- ✅ **Sin duplicación** de código o interfaces
- ✅ **Experiencia de usuario** mejorada y consistente

## 🔍 **TROUBLESHOOTING**

### **Problemas Comunes**

1. **Error de OpenAI API Key**
   - Verificar que la variable `OPENAI_API_KEY` esté configurada
   - Usar clave de prueba para desarrollo

2. **Error de directorios**
   - Verificar que existan los directorios `input/`, `logs/`
   - Ejecutar `python -c "from src.config.config import config; config.validate_config()"`

3. **Error de dependencias**
   - Actualizar pip: `pip install --upgrade pip`
   - Reinstalar dependencias: `pip install -r requirements.txt`

4. **La interfaz no carga**
   - Verificar que `app.py` esté ejecutándose
   - Revisar consola del navegador para errores JavaScript

## 📝 **LOGS Y MONITOREO**

### **Archivos de Log**
- **Principal**: `logs/sifgpt.log`
- **Nivel**: Configurable via `LOG_LEVEL`
- **Formato**: Timestamp + Nivel + Mensaje

### **Monitoreo en Tiempo Real**
```bash
tail -f logs/sifgpt.log
```

## 🤝 **CONTRIBUCIÓN**

### **Estructura de Desarrollo**
1. **Fork** del repositorio
2. **Crear rama** para nueva funcionalidad
3. **Implementar** cambios
4. **Ejecutar pruebas** completas
5. **Crear Pull Request**

### **Estándares de Código**
- **Python**: PEP 8
- **JavaScript**: ES6+ con funciones modernas
- **HTML/CSS**: Bootstrap 5 + CSS personalizado
- **Documentación**: Docstrings completos
- **Logging**: Usar logger centralizado
- **Manejo de errores**: Try-catch con logging

## 📄 **LICENCIA**

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 **CONTACTO**

- **Desarrollador**: Felipe
- **Proyecto**: SIFGPT - Sistema de PQRS Unificado
- **Versión**: 2.0.0 UNIFICADA
- **Estado**: ✅ 100% FUNCIONAL + INTERFAZ UNIFICADA

---

## 🎉 **¡SIFGPT UNIFICADO ESTÁ LISTO!**

**Ahora tienes TODO en un solo lugar:**
- 🎯 **Un solo localhost:5000** para el frontend
- 🔌 **Un solo localhost:5000/api** para el backend
- 🧪 **Un solo localhost:5000/test** para las pruebas
- 📱 **Una sola interfaz** con todas las funcionalidades
- 🚀 **Sin pérdida de funcionalidad** - todo está ahí

**¡Tu sistema de PQRS inteligente unificado está listo para revolucionar la atención al ciudadano!** 🚀✨
