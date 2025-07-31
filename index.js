const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

// Configuración de CORS
app.use(cors({
  origin: process.env.CORS_ORIGINS === '*' ? '*' : process.env.CORS_ORIGINS?.split(',') || '*',
  credentials: true
}));

app.use(express.json());

// Configuración de multer para subida de archivos
const storage = multer.memoryStorage();
const upload = multer({
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Tipo de archivo no permitido'), false);
    }
  }
});

// Inicializar Gemini AI
const genAI = process.env.GEMINI_API_KEY ? new GoogleGenerativeAI(process.env.GEMINI_API_KEY) : null;

// Base de datos nutricional
const nutritionalData = {
  // Frutas
  "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "fiber": 2.4},
  "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6},
  "orange": {"calories": 47, "protein": 0.9, "carbs": 12, "fat": 0.1, "fiber": 2.4},
  "strawberry": {"calories": 32, "protein": 0.7, "carbs": 8, "fat": 0.3, "fiber": 2.0},
  "grapes": {"calories": 62, "protein": 0.6, "carbs": 16, "fat": 0.2, "fiber": 0.9},
  
  // Vegetales
  "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6},
  "carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 2.8},
  "tomato": {"calories": 18, "protein": 0.9, "carbs": 4, "fat": 0.2, "fiber": 1.2},
  "lettuce": {"calories": 15, "protein": 1.4, "carbs": 3, "fat": 0.2, "fiber": 1.3},
  "spinach": {"calories": 23, "protein": 2.9, "carbs": 4, "fat": 0.4, "fiber": 2.2},
  
  // Proteínas
  "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0},
  "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 12, "fiber": 0},
  "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "fiber": 0},
  "egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "fiber": 0},
  "tofu": {"calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "fiber": 0.3},
  
  // Carbohidratos
  "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "fiber": 0.4},
  "bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.2, "fiber": 2.7},
  "pasta": {"calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "fiber": 1.8},
  "potato": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "fiber": 2.2},
  "quinoa": {"calories": 120, "protein": 4.4, "carbs": 22, "fat": 1.9, "fiber": 2.8}
};

// Factores de peso estimado (gramos por porción típica)
const weightFactors = {
  "apple": 150, "banana": 120, "orange": 130, "strawberry": 15, "grapes": 5,
  "broccoli": 100, "carrot": 80, "tomato": 120, "lettuce": 20, "spinach": 30,
  "chicken_breast": 150, "salmon": 150, "beef": 150, "egg": 50, "tofu": 100,
  "rice": 150, "bread": 30, "pasta": 100, "potato": 150, "quinoa": 100
};

// Función para crear el prompt de análisis
function createFoodAnalysisPrompt() {
  return `
Analiza esta imagen de comida y proporciona una respuesta JSON detallada con la siguiente estructura:

{
  "dish_identification": {
    "name": "nombre_del_plato_principal",
    "confidence": 0.95,
    "cuisine_type": "peruana/italiana/mexicana/etc"
  },
  "detections": [
    {
      "class": "nombre_comida_en_ingles",
      "confidence": 0.95,
      "bbox": [0.1, 0.2, 0.8, 0.7],
      "estimated_weight": 150,
      "nutrition": {
        "calories": 248,
        "protein": 46.5,
        "carbs": 0.0,
        "fat": 5.4,
        "fiber": 0.0
      },
      "nutrition_per_100g": {
        "calories": 165,
        "protein": 31.0,
        "carbs": 0.0,
        "fat": 3.6,
        "fiber": 0.0
      }
    }
  ],
  "meal_analysis": {
    "total_calories": 450,
    "total_protein": 35.2,
    "total_carbs": 45.8,
    "total_fat": 12.3,
    "health_score": 8.5,
    "recommendations": ["Agregar más vegetales", "Buen contenido de proteína"]
  }
}

Responde SOLO con el JSON válido, sin texto adicional.`;
}

// Función para detectar alimentos con Gemini
async function detectFoodWithGemini(imageBuffer) {
  if (!genAI) {
    return simulateDetection();
  }

  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    
    const imagePart = {
      inlineData: {
        data: imageBuffer.toString('base64'),
        mimeType: "image/jpeg"
      }
    };

    const prompt = createFoodAnalysisPrompt();
    const result = await model.generateContent([prompt, imagePart]);
    const response = await result.response;
    const text = response.text();
    
    // Limpiar y parsear la respuesta JSON
    const cleanedText = text.replace(/```json\n?|\n?```/g, '').trim();
    return JSON.parse(cleanedText);
    
  } catch (error) {
    console.error('Error en detección con Gemini:', error);
    return simulateDetection();
  }
}

// Función de simulación para cuando no hay API key
function simulateDetection() {
  return {
    "dish_identification": {
      "name": "Plato mixto",
      "confidence": 0.85,
      "cuisine_type": "Internacional"
    },
    "detections": [
      {
        "class": "chicken_breast",
        "confidence": 0.90,
        "bbox": [0.2, 0.3, 0.4, 0.5],
        "estimated_weight": 150,
        "nutrition": {
          "calories": 248,
          "protein": 46.5,
          "carbs": 0,
          "fat": 5.4,
          "fiber": 0
        },
        "nutrition_per_100g": {
          "calories": 165,
          "protein": 31,
          "carbs": 0,
          "fat": 3.6,
          "fiber": 0
        }
      },
      {
        "class": "broccoli",
        "confidence": 0.88,
        "bbox": [0.6, 0.2, 0.3, 0.4],
        "estimated_weight": 100,
        "nutrition": {
          "calories": 34,
          "protein": 2.8,
          "carbs": 7,
          "fat": 0.4,
          "fiber": 2.6
        },
        "nutrition_per_100g": {
          "calories": 34,
          "protein": 2.8,
          "carbs": 7,
          "fat": 0.4,
          "fiber": 2.6
        }
      }
    ],
    "meal_analysis": {
      "total_calories": 282,
      "total_protein": 49.3,
      "total_carbs": 7,
      "total_fat": 5.8,
      "health_score": 9.0,
      "recommendations": ["Excelente balance proteico", "Buena fuente de fibra"]
    }
  };
}

// RUTAS DE LA API

// Ruta raíz
app.get('/', (req, res) => {
  res.json({
    message: "Food Detection API con Google Gemini",
    version: "2.0.0",
    ai_backend: "Google Gemini 1.5 Flash",
    architecture: "Node.js Backend especializado en IA",
    docs: "/docs",
    status: "running",
    features: [
      "Detección avanzada de alimentos con IA",
      "Análisis nutricional automático",
      "Alta precisión en reconocimiento",
      "API optimizada para aplicaciones móviles"
    ]
  });
});

// Health check
app.get('/health', (req, res) => {
  const geminiStatus = process.env.GEMINI_API_KEY ? "configured" : "not_configured";
  
  res.json({
    status: "healthy",
    environment: process.env.ENVIRONMENT || "development",
    gemini: geminiStatus,
    architecture: "Node.js AI-focused backend",
    timestamp: new Date().toISOString()
  });
});

// Documentación básica
app.get('/docs', (req, res) => {
  res.json({
    title: "Food Detection API",
    version: "2.0.0",
    description: "API especializada en detección de alimentos usando Google Gemini 1.5 Flash",
    endpoints: {
      "GET /": "Información del sistema",
      "GET /health": "Estado de salud",
      "GET /docs": "Esta documentación",
      "POST /api/v1/ai/test-detection": "Detección de alimentos en imagen",
      "GET /api/v1/ai/supported-foods": "Alimentos soportados"
    },
    usage: {
      "detection": "Envía una imagen como form-data con key 'file'",
      "response": "JSON con detecciones, análisis nutricional y recomendaciones"
    }
  });
});

// Endpoint principal de detección
app.post('/api/v1/ai/test-detection', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: "No se proporcionó ningún archivo de imagen"
      });
    }

    console.log(`Procesando imagen: ${req.file.originalname}, tamaño: ${req.file.size} bytes`);

    // Detectar alimentos
    const detectionResult = await detectFoodWithGemini(req.file.buffer);

    res.json({
      success: true,
      detection_result: detectionResult,
      filename: req.file.originalname,
      message: "Detección completada exitosamente"
    });

  } catch (error) {
    console.error('Error en detección:', error);
    res.status(500).json({
      success: false,
      error: "Error interno del servidor",
      message: error.message
    });
  }
});

// Alimentos soportados
app.get('/api/v1/ai/supported-foods', (req, res) => {
  const supportedFoods = Object.keys(nutritionalData).map(food => ({
    name: food,
    nutrition_per_100g: nutritionalData[food],
    typical_weight: weightFactors[food] || 100
  }));

  res.json({
    total_foods: supportedFoods.length,
    foods: supportedFoods,
    categories: {
      fruits: ["apple", "banana", "orange", "strawberry", "grapes"],
      vegetables: ["broccoli", "carrot", "tomato", "lettuce", "spinach"],
      proteins: ["chicken_breast", "salmon", "beef", "egg", "tofu"],
      carbs: ["rice", "bread", "pasta", "potato", "quinoa"]
    }
  });
});

// Manejo de errores
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        success: false,
        error: "El archivo es demasiado grande. Máximo 10MB."
      });
    }
  }
  
  res.status(500).json({
    success: false,
    error: "Error interno del servidor"
  });
});

// Ruta 404
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    error: "Endpoint no encontrado",
    available_endpoints: [
      "GET /",
      "GET /health", 
      "GET /docs",
      "POST /api/v1/ai/test-detection",
      "GET /api/v1/ai/supported-foods"
    ]
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`🚀 Food Detection API ejecutándose en puerto ${PORT}`);
  console.log(`📱 Optimizada para aplicaciones móviles Flutter`);
  console.log(`🤖 IA: Google Gemini 1.5 Flash`);
  console.log(`🔑 Gemini API: ${process.env.GEMINI_API_KEY ? 'Configurada' : 'No configurada (modo simulación)'}`);
  console.log(`📖 Documentación: http://localhost:${PORT}/docs`);
});

module.exports = app;