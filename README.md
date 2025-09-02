# TUNRAG - Sistema de PQRS con Inteligencia Artificial

## 🎯 Descripción

TUNRAG es un sistema moderno y completamente funcional de procesamiento de PQRS (Peticiones, Quejas, Reclamos, Sugerencias y Denuncias) que utiliza inteligencia artificial para clasificar y responder automáticamente a las solicitudes de los ciudadanos de Medellín.

## ✨ Características Principales

- **🤖 Clasificación Automática de PQRS** usando GPT-4
- **🎤 Transcripción de Audio** con OpenAI Whisper
- **💬 Generación Inteligente de Respuestas** contextuales
- **📊 Consulta de Histórico** de PQRS existentes
- **🔍 Manejo de FAQs** automático
- **📱 Interfaz Web Moderna** y responsive
- **📝 Logging Completo** del sistema
- **⚡ Arquitectura Escalable** siguiendo principios SOLID

## 🚀 Instalación Rápida

### **1. Clonar el Repositorio**
```bash
git clone <repository-url>
cd TUNRAG
```

### **2. Configuración Automática (Recomendado)**
```bash
python setup.py
```

### **3. Configuración Manual (Alternativa)**

#### **Crear Entorno Virtual**
```bash
# Con conda
conda env create -f environment.yml
conda activate poc_dd

# O con venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

#### **Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env y configurar tu API key
OPENAI_API_KEY=tu_api_key_de_openai_aqui
```

### **4. Ejecutar la Aplicación**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🔧 Configuración

### **Variables de Entorno Requeridas**

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `OPENAI_API_KEY` | **REQUERIDA** - Clave API de OpenAI | `sk-...` |
| `OPENAI_MODEL` | Modelo de OpenAI a usar | `gpt-4o` |
| `WHISPER_MODEL` | Modelo de Whisper para audio | `whisper-1` |
| `DEBUG` | Modo debug | `True` |
| `SECRET_KEY` | Clave secreta de Flask | `mi-clave-secreta` |

### **Estructura de Directorios**
```
TUNRAG/
├── src/                    # Código fuente
│   ├── config/            # Configuración
│   ├── controllers/       # Controladores de API
│   ├── models/            # Modelos de datos
│   ├── repositories/      # Acceso a datos
│   ├── services/          # Lógica de negocio
│   └── utils/             # Utilidades
├── input/                 # Datos de entrada
│   ├── audios/            # Archivos de audio
│   ├── historico/         # Base de datos histórica
│   ├── prompts/           # Prompts del sistema
│   └── plantillas_solucion/ # Plantillas de respuesta
├── static/                # Archivos estáticos
├── templates/             # Plantillas HTML
└── logs/                  # Archivos de log
```

## 📡 API Endpoints

### **Endpoints Principales**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página principal |
| `/get_response` | POST | Procesar PQRS desde texto |
| `/process_audio` | POST | Procesar PQRS desde audio |
| `/transcribe_audio` | POST | Solo transcribir audio |

### **Endpoints del Sistema**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Verificación básica de salud |
| `/health/detailed` | GET | Verificación detallada de salud |
| `/system/status` | GET | Estado del sistema |
| `/system/refresh` | POST | Refrescar cachés |
| `/system/validate` | GET | Validar sistema |

## 🎯 Uso del Sistema

### **1. Interfaz Web**
- Abre `http://localhost:5000` en tu navegador
- Escribe tu PQRS en el campo de texto
- O usa el botón de micrófono para grabar audio
- El sistema clasificará y responderá automáticamente

### **2. API REST**
```bash
# Procesar texto
curl -X POST http://localhost:5000/get_response \
  -H "Content-Type: application/json" \
  -d '{"message": "Solicito información sobre el estado de la calle 45"}'

# Procesar audio
curl -X POST http://localhost:5000/process_audio \
  -F "audio=@mi_audio.wav"

# Verificar salud del sistema
curl http://localhost:5000/health
```

### **3. Ejemplos de PQRS**

#### **Petición**
```
"Solicito información sobre cuándo se arreglará el semáforo de la avenida principal"
```

#### **Queja**
```
"Me quejo del mal estado de las aceras en mi barrio"
```

#### **Reclamo**
```
"Reclamo por el retraso en la obra de la calle 5"
```

#### **Sugerencia**
```
"Sugiero instalar más bancas en el parque del centro"
```

#### **Denuncia**
```
"Denuncio un hueco peligroso en la avenida principal"
```

## 🔍 Monitoreo y Logs

### **Ver Logs en Tiempo Real**
```bash
tail -f logs/tunrag.log
```

### **Verificar Estado del Sistema**
```bash
curl http://localhost:5000/system/status
```

### **Validar Sistema**
```bash
curl http://localhost:5000/system/validate
```

## 🧪 Testing

### **Modo de Prueba**
```python
# En el código
result = orchestrator.process_text_pqrs("texto de prueba", test=True)
```

### **Tests Automáticos**
```bash
python setup.py  # Ejecuta tests básicos
```

## 🚨 Solución de Problemas

### **Problemas Comunes**

#### **1. Error: "OPENAI_API_KEY no está configurada"**
```bash
# Verificar que el archivo .env existe y tiene la API key
cat .env | grep OPENAI_API_KEY
```

#### **2. Error: "Formato de audio no soportado"**
- Formatos soportados: `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, `webm`
- Tamaño máximo: 16MB

#### **3. Error: "Error interno del servidor"**
```bash
# Ver logs para más detalles
tail -f logs/tunrag.log
```

#### **4. La aplicación no inicia**
```bash
# Verificar dependencias
python setup.py

# Verificar puerto disponible
netstat -an | grep 5000
```

### **Logs de Debug**
```bash
# Cambiar nivel de log en .env
LOG_LEVEL=DEBUG

# Reiniciar aplicación
python app.py
```

## 🔒 Seguridad

### **Medidas Implementadas**
- ✅ Validación de entrada
- ✅ Manejo seguro de archivos
- ✅ Logging de auditoría
- ✅ Manejo de errores sin exposición de información sensible
- ✅ Límite de tamaño de archivos
- ✅ CORS configurado

### **Recomendaciones de Producción**
- Cambiar `SECRET_KEY` por defecto
- Configurar `DEBUG=False`
- Usar HTTPS en producción
- Implementar autenticación si es necesario
- Configurar firewall apropiado

## 📊 Métricas y Rendimiento

### **Indicadores Clave**
- Tiempo de respuesta promedio
- Tasa de éxito en clasificación
- Uso de caché
- Estado de servicios externos

### **Optimizaciones Implementadas**
- Caché de prompts y plantillas
- Lazy loading de datos
- Estrategias configurables de transcripción
- Manejo eficiente de errores

## 🚀 Roadmap

### **Próximas Funcionalidades**
- [ ] Implementación de RAG (Retrieval Augmented Generation)
- [ ] Integración con LangChain
- [ ] Dashboard de administración
- [ ] API de webhooks
- [ ] Sistema de notificaciones
- [ ] Análisis avanzado de sentimientos
- [ ] Integración con bases de datos
- [ ] Sistema de usuarios y roles

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

## 📞 Soporte

### **Para Soporte Técnico**
- Email: [email]
- Documentación: [docs-url]
- Issues: [github-issues]

### **Comunidad**
- Discord: [discord-invite]
- Telegram: [telegram-group]

---

## 🎉 ¡TUNRAG está Listo para tu Negocio!

**TUNRAG v2.0.0** - Sistema de PQRS con Inteligencia Artificial

**Características Destacadas:**
- ✅ **100% Funcional** - Listo para producción
- ✅ **Arquitectura Sólida** - Principios SOLID implementados
- ✅ **Manejo de Errores Robusto** - Sistema estable y confiable
- ✅ **Interfaz Intuitiva** - Fácil de usar para ciudadanos
- ✅ **Escalable** - Preparado para crecimiento
- ✅ **Documentado** - Fácil de mantener y extender

**¡Tu sistema de PQRS inteligente está listo para revolucionar la atención al ciudadano!** 🚀
