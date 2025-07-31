# 🍽️ Food Detection API - Node.js Backend

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Jeysson16/backend-comidas&env=GEMINI_API_KEY&envDescription=API%20Key%20de%20Google%20Gemini%20requerida&envLink=https://makersuite.google.com/app/apikey)

## 📋 Descripción

API backend desarrollada en **Node.js** especializada en detección de alimentos usando **Google Gemini 1.5 Flash**. Optimizada para aplicaciones móviles Flutter con análisis nutricional automático y alta precisión en reconocimiento de imágenes.

## 🚀 Características

- **IA Avanzada**: Google Gemini 1.5 Flash para detección precisa
- **Análisis Nutricional**: Cálculo automático de calorías, proteínas, carbohidratos y grasas
- **API RESTful**: Endpoints optimizados para aplicaciones móviles
- **Soporte Multi-formato**: JPEG, PNG, GIF, WebP
- **Despliegue Fácil**: Configurado para Vercel con un clic
- **Base de Datos Nutricional**: 25+ alimentos con información detallada

## 🛠️ Tecnologías

- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **IA**: Google Generative AI (Gemini 1.5 Flash)
- **Procesamiento**: Multer para archivos
- **Despliegue**: Vercel
- **CORS**: Configurado para aplicaciones móviles

## 📦 Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/Jeysson16/backend-comidas.git
cd backend-comidas

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu GEMINI_API_KEY

# Ejecutar en desarrollo
npm run dev

# Ejecutar en producción
npm start
```

## 🔧 Variables de Entorno

```env
GEMINI_API_KEY=tu_api_key_de_gemini
PORT=8000
CORS_ORIGINS=*
ENVIRONMENT=development
```

## 🚀 Despliegue en Vercel

### Opción 1: Un Clic
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Jeysson16/backend-comidas)

### Opción 2: Manual
1. Fork este repositorio
2. Conecta tu cuenta de Vercel con GitHub
3. Importa el proyecto en Vercel
4. Configura las variables de entorno:
   - `GEMINI_API_KEY`: Tu API key de Google Gemini
   - `CORS_ORIGINS`: `*` (o dominios específicos)
5. Deploy automático

### Variables de Entorno en Vercel
```
GEMINI_API_KEY=tu_api_key_aqui
CORS_ORIGINS=*
ENVIRONMENT=production
```

## 📡 Endpoints

### Información del Sistema
```http
GET /
```

### Estado de Salud
```http
GET /health
```

### Documentación
```http
GET /docs
```

### Detección de Alimentos
```http
POST /api/v1/ai/test-detection
Content-Type: multipart/form-data

file: [imagen_de_comida]
```

**Respuesta:**
```json
{
  "success": true,
  "detection_result": {
    "dish_identification": {
      "name": "Pollo con brócoli",
      "confidence": 0.95,
      "cuisine_type": "Internacional"
    },
    "detections": [
      {
        "class": "chicken_breast",
        "confidence": 0.90,
        "estimated_weight": 150,
        "nutrition": {
          "calories": 248,
          "protein": 46.5,
          "carbs": 0,
          "fat": 5.4,
          "fiber": 0
        }
      }
    ],
    "meal_analysis": {
      "total_calories": 282,
      "total_protein": 49.3,
      "health_score": 9.0,
      "recommendations": ["Excelente balance proteico"]
    }
  }
}
```

### Alimentos Soportados
```http
GET /api/v1/ai/supported-foods
```

## 🥗 Alimentos Soportados

### Frutas
- Manzana, Plátano, Naranja, Fresa, Uvas

### Vegetales  
- Brócoli, Zanahoria, Tomate, Lechuga, Espinaca

### Proteínas
- Pechuga de pollo, Salmón, Carne de res, Huevo, Tofu

### Carbohidratos
- Arroz, Pan, Pasta, Papa, Quinoa



## 📱 Integración con Flutter

```dart
// Ejemplo de uso en Flutter
final request = http.MultipartRequest(
  'POST', 
  Uri.parse('https://backend-comidas-jeysson16.vercel.app/api/v1/ai/test-detection')
);
request.files.add(await http.MultipartFile.fromPath('file', imagePath));

final response = await request.send();
final responseData = await response.stream.bytesToString();
final result = json.decode(responseData);
```

## 🔍 Estructura del Proyecto

```
backend_comidas/
├── index.js              # Aplicación principal
├── package.json          # Dependencias Node.js
├── vercel.json           # Configuración Vercel
├── .env.example          # Variables de entorno ejemplo
├── .gitignore           # Archivos ignorados
└── README.md            # Documentación
```

## 🧪 Testing

```bash
# Probar endpoint de salud
curl https://backend-comidas-jeysson16.vercel.app/health

# Probar detección (con imagen)
curl -X POST -F "file=@imagen.jpg" https://backend-comidas-jeysson16.vercel.app/api/v1/ai/test-detection
```

## 📊 Rendimiento

- **Tiempo de respuesta**: < 3 segundos
- **Precisión**: > 90% en alimentos comunes
- **Límite de archivo**: 10MB
- **Formatos soportados**: JPEG, PNG, GIF, WebP
- **Concurrencia**: Optimizado para múltiples usuarios

## 🔒 Seguridad

- Validación de tipos de archivo
- Límites de tamaño de archivo
- CORS configurado
- Variables de entorno seguras
- Sin almacenamiento de imágenes

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

- **Documentación**: `/docs` endpoint
- **Issues**: GitHub Issues
- **Email**: tu-email@ejemplo.com

## 🔄 Changelog

### v2.0.0 (Actual)
- ✅ Migración completa a Node.js
- ✅ Optimización para Vercel
- ✅ Mejor rendimiento y estabilidad
- ✅ API más robusta

### v1.0.0 (Legacy Python)
- ✅ Versión inicial en Python/FastAPI
- ✅ Integración básica con Gemini

---

**Desarrollado con ❤️ para aplicaciones móviles Flutter**
