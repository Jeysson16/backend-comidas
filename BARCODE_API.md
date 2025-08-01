# API de Análisis de Códigos de Barras

## Descripción General

La API ahora incluye capacidades avanzadas de análisis de códigos de barras, específicamente optimizada para productos disponibles en Perú. Utiliza una estrategia en cascada que combina múltiples fuentes de datos con análisis de IA.

## Nuevos Endpoints

### 1. POST `/api/v1/ai/barcode-scan`

Analiza un producto a partir de una imagen que contiene un código de barras.

**Parámetros:**
- `file`: Imagen que contiene el código de barras (JPG, PNG, etc.)

**Respuesta de ejemplo:**
```json
{
  "success": true,
  "product_analysis": {
    "barcode": "7751271001234",
    "product_info": {
      "name": "Leche Gloria Entera",
      "brand": "Gloria",
      "category": "Lácteos",
      "country": "Perú",
      "source": "openfoodfacts"
    },
    "nutritional_analysis": {
      "calories_per_100g": 65,
      "macronutrients": {
        "protein": 3.2,
        "carbs": 4.8,
        "fat": 3.5,
        "fiber": 0
      },
      "micronutrients": {
        "calcium": 120,
        "vitamin_d": 1.2,
        "sodium": 50
      }
    },
    "health_analysis": {
      "processing_level": "Procesado",
      "health_score": 7.5,
      "recommendations": [
        "Buena fuente de calcio y proteínas",
        "Moderado en grasas saturadas",
        "Ideal para el desayuno"
      ]
    },
    "sustainability": {
      "eco_score": "B",
      "carbon_footprint": "Medio",
      "packaging": "Reciclable"
    }
  },
  "filename": "codigo_barras.jpg",
  "message": "Análisis de código de barras completado exitosamente"
}
```

### 2. POST `/api/v1/ai/barcode-manual`

Analiza un producto a partir de un código de barras ingresado manualmente.

**Parámetros:**
- `barcode`: Código de barras (8, 12, 13 o 14 dígitos)

**Ejemplo de uso:**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/barcode-manual" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "barcode=7751271001234"
```

### 3. GET `/api/v1/ai/barcode-info`

Obtiene información sobre las capacidades de análisis de códigos de barras.

**Respuesta:**
```json
{
  "success": true,
  "barcode_capabilities": {
    "supported_formats": [
      "EAN-13 (más común en Perú y el mundo)",
      "EAN-8 (productos pequeños)",
      "UPC-A (productos de Estados Unidos)",
      "UPC-E (versión compacta de UPC-A)"
    ],
    "peru_specific": {
      "country_code": "775",
      "description": "Los productos fabricados en Perú tienen códigos que empiezan con 775",
      "coverage": "Buena cobertura en OpenFoodFacts para productos peruanos"
    },
    "data_sources": [
      {
        "name": "OpenFoodFacts",
        "description": "Base de datos colaborativa mundial de productos alimentarios",
        "coverage": "Excelente para productos internacionales y peruanos conocidos",
        "priority": 1
      },
      {
        "name": "UPC Database",
        "description": "Base de datos comercial de códigos UPC/EAN",
        "coverage": "Buena para productos que no están en OpenFoodFacts",
        "priority": 2
      }
    ]
  }
}
```

## Estrategia de Análisis

### 1. Detección de Código de Barras
- Utiliza OpenCV y pyzbar para detectar códigos de barras en imágenes
- Soporta múltiples formatos (EAN-13, EAN-8, UPC-A, UPC-E)
- Optimizado para códigos peruanos (775) e internacionales

### 2. Búsqueda de Información del Producto
**Fuente principal:**
1. **OpenFoodFacts** (Siempre disponible - Gratuito)
   - Base de datos colaborativa mundial
   - Excelente para productos peruanos conocidos
   - Información nutricional detallada
   - No requiere API key ni registro

**Fuente opcional:**
2. **UPC Database** (Solo si se configura - Requiere tarjeta)
   - Base de datos comercial
   - Respaldo para productos no encontrados en OpenFoodFacts
   - **No recomendado** por requerir registro con tarjeta de crédito

### 3. Análisis con IA (Gemini)
- Análisis nutricional detallado
- Evaluación de nivel de procesamiento
- Recomendaciones de salud personalizadas
- Análisis de sostenibilidad
- Comparación con alternativas

## Códigos de Barras en Perú

### Productos Peruanos
- **Código de país:** 775
- **Ejemplo:** 7751271001234 (Gloria)
- **Cobertura:** Buena en OpenFoodFacts

### Productos Importados
- Mantienen su código original del país de origen
- **Estados Unidos:** 0-1 (UPC)
- **Europa:** 30-37, 40-44, etc.
- **Brasil:** 789
- **Chile:** 780

## Variables de Entorno Requeridas

```env
# Gemini AI (REQUERIDO para análisis nutricional)
GEMINI_API_KEY=tu_api_key_de_gemini

# UPC Database (COMPLETAMENTE OPCIONAL - no recomendado por requerir tarjeta)
# UPC_DATABASE_API_KEY=tu_api_key_opcional
```

**Nota importante:** La API funciona perfectamente solo con OpenFoodFacts (gratuito) y Gemini. UPC Database es opcional y requiere registro con tarjeta de crédito.

## Casos de Uso

### 1. Aplicación Móvil
- Escaneo directo con cámara del teléfono
- Análisis nutricional instantáneo
- Recomendaciones personalizadas

### 2. Gestión de Inventario
- Registro rápido de productos
- Información nutricional automática
- Categorización inteligente

### 3. Educación Nutricional
- Comparación de productos
- Análisis de ingredientes
- Recomendaciones saludables

## Limitaciones y Consideraciones

### Cobertura de Productos
- **Productos internacionales:** Excelente cobertura
- **Productos peruanos grandes:** Buena cobertura
- **Productos locales pequeños:** Cobertura variable

### Fallback Strategy
Si no se encuentra información del código de barras:
1. Se puede usar el endpoint `/test-detection` con imagen del producto
2. Gemini analizará la imagen directamente
3. Proporcionará información nutricional estimada

### Rendimiento
- **Tiempo de respuesta:** 2-5 segundos promedio
- **Precisión:** Alta para productos conocidos
- **Disponibilidad:** 99.9% (dependiente de APIs externas)