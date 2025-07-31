# Food Detection API 🍽️

API especializada en detección de alimentos usando Google Gemini 1.5 Flash, optimizada para aplicaciones móviles Flutter.

## 🚀 Despliegue rápido en Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Jeysson16/backend-comidas&env=GEMINI_API_KEY&envDescription=API%20Key%20de%20Google%20Gemini%20requerida&envLink=https://makersuite.google.com/app/apikey)

## 📱 Características

- ✅ **Detección avanzada de alimentos** con IA
- ✅ **Análisis nutricional automático**
- ✅ **Estimación de porciones** por peso
- ✅ **API optimizada** para aplicaciones móviles
- ✅ **CORS configurado** para Flutter
- ✅ **Respuestas estructuradas** en JSON
- ✅ **Documentación interactiva** con Swagger

## 🛠️ Tecnologías

- **Backend**: FastAPI + Python 3.11
- **IA**: Google Gemini 1.5 Flash
- **Despliegue**: Vercel
- **Documentación**: Swagger UI automática

## 📋 Requisitos

- Python 3.11+
- API Key de Google Gemini ([Obtener aquí](https://makersuite.google.com/app/apikey))

## 🚀 Instalación local

```bash
# Clonar repositorio
git clone https://github.com/Jeysson16/backend-comidas.git
cd backend-comidas

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY

# Ejecutar servidor
python run.py
```

La API estará disponible en: `http://localhost:8000`

## 🌐 Despliegue en Vercel desde GitHub

### Opción 1: Un click (Recomendado)
1. Haz fork de este repositorio
2. Click en el botón "Deploy with Vercel" arriba
3. Conecta tu cuenta de GitHub
4. Agrega tu `GEMINI_API_KEY`
5. ¡Listo! 🎉

### Opción 2: Manual
1. Sube tu código a GitHub
2. Ve a [vercel.com](https://vercel.com)
3. Importa tu repositorio
4. Configura las variables de entorno
5. Despliega automáticamente

## 🔑 Variables de entorno requeridas

```bash
GEMINI_API_KEY=tu_api_key_aqui
CORS_ORIGINS=*  # Para aplicaciones móviles
ENVIRONMENT=production
DEBUG=false
```

## 📊 Estructura de respuesta

### Endpoint principal: `POST /api/v1/ai/test-detection`

## Estructura de la respuesta del endpoint de detección

Al enviar una imagen al endpoint `/api/v1/ai/test-detection`, la respuesta tendrá la siguiente estructura:

```json
{
  "success": true,
  "detection_result": {
    "dish_identification": {
      "dish_name": "Nombre del plato",
      "dish_type": "Tipo de plato",
      "cuisine_type": "Tipo de cocina",
      "description": "Descripción del plato"
    },
    "detections": [
      {
        "class": "Nombre del alimento",
        "confidence": 0.95,
        "bbox": [x, y, ancho, alto],
        "estimated_weight": 150,
        "nutrition": {
          "calories": 248,
          "protein": 46.5,
          "carbs": 0,
          "fat": 5.4,
          "fiber": 0,
          "sodium": 120
        },
        "nutrition_per_100g": {
          "calories": 165,
          "protein": 31,
          "carbs": 0,
          "fat": 3.6,
          "fiber": 0,
          "sodium": 80
        },
        "portion_size": "mediana"
      }
    ],
    "meal_analysis": {
      "meal_type": "Tipo de comida",
      "total_calories": 431,
      "total_protein_grams": 51.9,
      "total_carbs_grams": 39.2,
      "total_fat_grams": 6.1,
      "total_fiber_grams": 2.6,
      "nutritional_balance": "Balance nutricional",
      "health_score": 8.5,
      "macronutrient_units": "Todos los macronutrientes (proteína, carbohidratos, grasa, fibra) están expresados en gramos (g). Sodio en miligramos (mg). Calorías en kilocalorías (kcal).",
      "recommendations": ["Recomendación 1", "Recomendación 2"]
    },
    "total_items": 3,
    "confidence_avg": 0.88,
    "nutrition_source": "gemini_enhanced"
  },
  "filename": "nombre_archivo.jpg",
  "message": "Detección completada exitosamente"
}
```

### Notas sobre la respuesta

- **bbox**: Coordenadas normalizadas [x, y, ancho, alto] que representan la ubicación del alimento en la imagen (valores entre 0 y 1)
- **estimated_weight**: Peso estimado en gramos
- **nutrition**: Valores nutricionales para la porción detectada
- **nutrition_per_100g**: Valores nutricionales por 100g del alimento
- **macronutrient_units**: Unidades de medida para los valores nutricionales
  - Proteína, carbohidratos, grasa, fibra: gramos (g)
  - Sodio: miligramos (mg)
  - Calorías: kilocalorías (kcal)

## Endpoints disponibles

- `GET /`: Información general del sistema
- `GET /health`: Verificación de salud del sistema
- `GET /system-info`: Información detallada del sistema
- `GET /api/v1/ai/model-info`: Información del modelo Gemini
- `GET /api/v1/ai/supported-foods`: Alimentos soportados
- `GET /api/v1/ai/nutrition-database`: Base de datos nutricional
- `GET /api/v1/ai/gemini-status`: Estado de Gemini
- `GET /api/v1/ai/system-health`: Salud del sistema de IA
- `POST /api/v1/ai/test-detection`: Detección de alimentos en una imagen
backend_comidas/
├── app/
│   ├── api/              # Endpoints de la API
│   ├── core/             # Configuración y seguridad
│   ├── models/           # Modelos de base de datos
│   ├── schemas/          # Esquemas Pydantic
│   ├── services/         # Lógica de negocio
│   ├── ai/               # Módulos de IA
│   └── main.py           # Aplicación principal
├── alembic/              # Migraciones de BD
├── tests/                # Pruebas
└── requirements.txt      # Dependencias
```

## Funcionalidades Principales

### 1. Análisis de Imágenes con IA
- Detección automática de alimentos en fotos
- Estimación de porciones y macronutrientes
- Sugerencias inteligentes

### 2. Sistema de Aprendizaje Adaptativo
- Cálculo automático de TDEE
- Ajuste dinámico de objetivos
- Aprendizaje basado en adherencia

### 3. API Endpoints
- `/auth/` - Autenticación y usuarios
- `/meals/` - Registro y gestión de comidas
- `/analysis/` - Análisis de imágenes
- `/progress/` - Tracking y estadísticas
- `/sync/` - Sincronización offline

## Uso de la API
La documentación interactiva estará disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`