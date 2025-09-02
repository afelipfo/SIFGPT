# Integración del Archivo Excel Histórico

## Descripción

Se ha integrado exitosamente el archivo `historico2.xlsx` como fuente principal de consulta histórica para el bot de PQRS. El sistema ahora puede manejar tanto archivos CSV como Excel, priorizando el Excel cuando esté disponible.

## Características Principales

### 🔄 Carga Inteligente de Datos
- **Prioridad Excel**: El sistema intenta cargar primero `historico2.xlsx`
- **Fallback CSV**: Si no hay Excel, usa `historico.csv` como respaldo
- **Normalización automática**: Mapea nombres de columnas para compatibilidad

### 🧠 Consultas Inteligentes
- **Detección automática**: Analiza el texto del usuario para determinar el tipo de consulta
- **Múltiples criterios**: Búsqueda por radicado, texto, nombre, fechas, etc.
- **Respuestas contextuales**: Proporciona información relevante según la consulta

### 📊 Estadísticas Avanzadas
- **Resumen general**: Total de registros, fuente de datos, columnas disponibles
- **Análisis por categorías**: Clasificación, estado, fechas
- **Información del sistema**: Estado de cachés y servicios

## API Endpoints Disponibles

### Consulta General
```http
POST /api/historico/consulta
Content-Type: application/json

{
  "consulta": "texto de búsqueda",
  "tipo_consulta": "inteligente"
}
```

### Consulta por Radicado
```http
GET /api/historico/radicado/{numero_radicado}
```

### Búsqueda por Texto
```http
POST /api/historico/buscar/texto
Content-Type: application/json

{
  "texto": "palabras a buscar"
}
```

### Búsqueda por Nombre
```http
POST /api/historico/buscar/nombre
Content-Type: application/json

{
  "nombre": "nombre del solicitante"
}
```

### Consulta por Fechas
```http
POST /api/historico/fechas
Content-Type: application/json

{
  "fecha_inicio": "01/01/2024",
  "fecha_fin": "31/12/2024"
}
```

### Estadísticas
```http
GET /api/historico/estadisticas
```

### Ayuda
```http
GET /api/historico/ayuda
```

### Resumen
```http
GET /api/historico/resumen
```

## Tipos de Consulta Disponibles

### 1. **Por Radicado**
- Busca una PQRS específica por número de radicado
- Ejemplo: "Consulta el radicado 2024-001"

### 2. **Por Texto**
- Busca PQRS que contengan ciertas palabras en su descripción
- Ejemplo: "Busca PQRS sobre educación"

### 3. **Por Nombre**
- Busca PQRS por nombre del solicitante
- Ejemplo: "Busca PQRS de Juan Pérez"

### 4. **Por Fechas**
- Consulta PQRS en un rango de fechas específico
- Ejemplo: "PQRS entre 01/01/2024 y 31/12/2024"

### 5. **Estadísticas**
- Obtiene estadísticas generales del histórico
- Ejemplo: "Muestra estadísticas del histórico"

### 6. **Inteligente**
- Análisis automático del tipo de consulta basado en el texto
- Detecta automáticamente qué tipo de búsqueda realizar

## Uso desde el Bot

### Consulta Simple
```
Usuario: "Consulta el radicado 2024-001"
Bot: [Busca y muestra información de la PQRS]
```

### Búsqueda por Tema
```
Usuario: "Busca PQRS sobre educación"
Bot: [Muestra todas las PQRS relacionadas con educación]
```

### Estadísticas
```
Usuario: "¿Cuántas PQRS hay en el sistema?"
Bot: [Muestra estadísticas generales del histórico]
```

### Consulta por Fechas
```
Usuario: "PQRS del mes de enero 2024"
Bot: [Muestra PQRS del período especificado]
```

## Estructura de Respuestas

### Respuesta Exitosa
```json
{
  "success": true,
  "tipo_consulta": "por_radicado",
  "datos": {
    "numero_radicado": "2024-001",
    "nombre": "Juan Pérez",
    "fecha_radicacion": "15/01/2024",
    "texto_pqrs": "Solicito información sobre...",
    "clasificacion": "Petición",
    "estado_pqrs": "En proceso"
  },
  "mensaje": "Se encontró la PQRS con radicado 2024-001"
}
```

### Respuesta con Error
```json
{
  "success": false,
  "tipo_consulta": "por_radicado",
  "error": "Descripción del error",
  "mensaje": "Error al realizar la consulta"
}
```

## Configuración

### Variables de Entorno
```bash
# El sistema detecta automáticamente los archivos en:
INPUT_DIR/historico/historico2.xlsx  # Prioridad alta
INPUT_DIR/historico/historico.csv     # Prioridad baja
```

### Dependencias
```bash
pip install openpyxl pandas
```

## Pruebas

### Script de Prueba
```bash
python test_historico_integration.py
```

### Verificación Manual
1. Asegúrate de que `historico2.xlsx` esté en `input/historico/`
2. Ejecuta el script de prueba
3. Verifica que las APIs respondan correctamente
4. Prueba consultas desde el bot

## Logs y Monitoreo

### Logs del Sistema
- Carga de archivos históricos
- Normalización de columnas
- Consultas realizadas
- Errores y advertencias

### Métricas Disponibles
- Total de registros cargados
- Fuente de datos utilizada
- Columnas disponibles
- Estado de cachés

## Solución de Problemas

### Error: "No se encontró archivo histórico"
- Verifica que `historico2.xlsx` esté en `input/historico/`
- Asegúrate de que el archivo no esté corrupto
- Verifica permisos de lectura

### Error: "Columnas faltantes"
- El sistema normaliza automáticamente nombres de columnas
- Revisa los logs para ver qué columnas están disponibles
- Ajusta el mapeo en `_normalize_columns()` si es necesario

### Error: "Error al procesar fechas"
- Verifica el formato de fechas en el Excel
- El sistema acepta formatos DD/MM/YYYY, DD-MM-YYYY, etc.
- Revisa que las fechas sean válidas

## Mejoras Futuras

### Funcionalidades Planificadas
- [ ] Búsqueda por entidad o dependencia
- [ ] Filtros combinados (fecha + clasificación + estado)
- [ ] Exportación de resultados a Excel/PDF
- [ ] Dashboard de estadísticas en tiempo real
- [ ] Notificaciones de nuevas PQRS

### Optimizaciones Técnicas
- [ ] Caché inteligente con TTL
- [ ] Indexación de texto para búsquedas más rápidas
- [ ] Paginación de resultados grandes
- [ ] Compresión de datos históricos

## Soporte

Para soporte técnico o reportar problemas:
1. Revisa los logs del sistema
2. Ejecuta el script de prueba
3. Verifica la configuración
4. Consulta la documentación de la API

---

**Nota**: Esta integración mantiene compatibilidad total con el sistema existente y mejora significativamente las capacidades de consulta histórica del bot.
