# Food Detection API con Google Gemini

## Descripción
Backend especializado en detección de alimentos usando Google Gemini 1.5 Flash que permite:
- Detección avanzada de alimentos con IA
- Análisis nutricional automático
- Alta precisión en reconocimiento
- API optimizada solo para IA

## Tecnologías
- **FastAPI**: Framework web moderno y rápido
- **Google Gemini 1.5 Flash**: Modelo de IA para detección de alimentos
- **Vercel**: Plataforma de despliegue

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno (crear .env):
```
GEMINI_API_KEY=tu_api_key_de_gemini
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:5173
```

4. Iniciar servidor:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Despliegue en Vercel

1. Clona este repositorio
2. Instala la CLI de Vercel: `npm i -g vercel`
3. Ejecuta `vercel login` y sigue las instrucciones
4. Ejecuta `vercel` en la raíz del proyecto
5. Configura las variables de entorno en Vercel:
   - `GEMINI_API_KEY`: Tu API key de Google Gemini
   - `CORS_ORIGINS`: Lista de dominios permitidos separados por comas

## Estructura del Proyecto
```
/app
  /ai              # Módulos de IA para detección de alimentos
  /api             # Endpoints de la API
  /core            # Configuración y utilidades
  /models          # Modelos de datos
  /schemas         # Esquemas de validación
  /services        # Servicios de la aplicación
  main.py          # Punto de entrada de la aplicación
```

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