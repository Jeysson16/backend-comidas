"""
Endpoints de la API para información de modelos de IA.
Enfocado exclusivamente en Google Gemini.
Incluye detección de alimentos por imagen y análisis de productos por código de barras.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, List, Optional
import logging

from app.ai.food_detection import food_detector
from app.services.product_service import ProductAnalysisService

router = APIRouter()
logger = logging.getLogger(__name__)

# Instancia del servicio de análisis de productos
product_service = ProductAnalysisService()

@router.get("/model-info", response_model=Dict)
async def get_model_info():
    """
    Obtiene información detallada sobre el modelo Gemini.
    """
    try:
        info = food_detector.get_model_info()
        return {
            "success": True,
            "model_info": info,
            "message": "Información del modelo obtenida exitosamente"
        }
    except Exception as e:
        logger.error(f"Error obteniendo información del modelo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-foods", response_model=Dict)
async def get_supported_foods():
    """
    Obtiene información sobre las capacidades de detección de alimentos de Gemini.
    """
    try:
        foods_info = food_detector.get_supported_foods()
        return {
            "success": True,
            "food_detection_info": foods_info,
            "message": "Información de capacidades de detección obtenida exitosamente"
        }
    except Exception as e:
        logger.error(f"Error obteniendo información de alimentos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-detection", response_model=Dict)
async def test_detection(file: UploadFile = File(...)):
    """
    Prueba la detección de alimentos con una imagen usando Gemini.
    """
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="El archivo debe ser una imagen"
            )
        
        # Leer datos de la imagen
        image_data = await file.read()
        
        # Realizar detección
        result = food_detector.detect_objects(image_data)
        
        return {
            "success": True,
            "detection_result": result,
            "filename": file.filename,
            "message": "Detección completada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en detección de prueba: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nutrition-database", response_model=Dict)
async def get_nutrition_database():
    """
    Obtiene información sobre la base de datos nutricional de Gemini.
    """
    try:
        # Información sobre las capacidades nutricionales de Gemini
        nutrition_info = {
            "database_type": "AI-powered nutritional analysis",
            "provider": "Google Gemini 1.5 Flash",
            "capabilities": [
                "Cálculo automático de calorías",
                "Análisis de macronutrientes (proteínas, carbohidratos, grasas)",
                "Estimación de micronutrientes",
                "Análisis de fibra y azúcares",
                "Evaluación nutricional completa",
                "Recomendaciones personalizadas"
            ],
            "accuracy": "Alta precisión basada en análisis visual y base de datos USDA",
            "supported_nutrients": [
                "calories", "protein", "carbs", "fat", "fiber", 
                "sugar", "sodium", "calcium", "iron", "vitamin_c"
            ],
            "portion_estimation": "Estimación automática basada en análisis visual",
            "meal_analysis": "Análisis completo de comidas y balance nutricional",
            "total_foods": len(food_detector.get_supported_foods()),
            "update_frequency": "Tiempo real con cada análisis"
        }
        
        return {
            "success": True,
            "nutrition_database": nutrition_info,
            "message": "Información de base de datos nutricional obtenida exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo información nutricional: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gemini-status", response_model=Dict)
async def get_gemini_status():
    """
    Obtiene el estado actual de la integración con Gemini.
    """
    try:
        model_info = food_detector.get_model_info()
        
        status_info = {
            "gemini_configured": model_info["api_configured"],
            "status": model_info["status"],
            "model_name": model_info["model_name"],
            "provider": model_info["provider"],
            "capabilities": model_info["capabilities"],
            "features": model_info["features"],
            "supported_foods_count": model_info["supported_foods_count"],
            "confidence_threshold": model_info["confidence_threshold"],
            "ready_for_production": model_info["api_configured"] and model_info["status"] == "active"
        }
        
        return {
            "success": True,
            "gemini_status": status_info,
            "message": "Estado de Gemini obtenido exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado de Gemini: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimization-info", response_model=Dict)
async def get_optimization_info():
    """
    Obtiene información sobre la estrategia de optimización de tokens implementada.
    """
    try:
        # Verificar si el detector está disponible
        if food_detector.detector:
            optimization_info = food_detector.detector.get_optimization_info()
        else:
            # Información de optimización para modo simulación
            optimization_info = {
                "strategy": "simulation_mode",
                "description": "Modo simulación - API key de Gemini no configurada",
                "features": {
                    "single_api_call": False,
                    "gemini_nutrition": False,
                    "local_fallback": True,
                    "enhanced_analysis": False,
                    "health_scoring": True,
                    "recommendations": True
                },
                "benefits": [
                    "Permite desarrollo sin API key",
                    "Respuestas consistentes para testing",
                    "Datos nutricionales básicos incluidos"
                ],
                "token_optimization": {
                    "current_status": "Simulación activa",
                    "note": "Para optimización real, configura GEMINI_API_KEY",
                    "potential_savings": "30-40% con API key real"
                }
            }
        
        return {
            "success": True,
            "optimization": optimization_info,
            "message": "Información de optimización obtenida exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo información de optimización: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system-health", response_model=Dict)
async def get_system_health():
    """
    Obtiene información sobre la salud general del sistema de IA.
    """
    try:
        model_info = food_detector.get_model_info()
        
        health_info = {
            "overall_status": "healthy" if model_info["api_configured"] else "needs_configuration",
            "ai_backend": "Google Gemini",
            "api_status": "configured" if model_info["api_configured"] else "not_configured",
            "detection_ready": model_info["status"] == "active",
            "last_check": "real_time",
            "recommendations": []
        }
        
        # Agregar recomendaciones basadas en el estado
        if not model_info["api_configured"]:
            health_info["recommendations"].append(
                "Configura GEMINI_API_KEY en las variables de entorno"
            )
        else:
            health_info["recommendations"].append(
                "Sistema listo para detección de alimentos"
            )
        
        return {
            "success": True,
            "system_health": health_info,
            "message": "Información de salud del sistema obtenida exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo salud del sistema: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/barcode-scan", response_model=Dict)
async def scan_barcode(file: UploadFile = File(...)):
    """
    Analiza un producto a partir de una imagen de código de barras.
    Detecta el código de barras, obtiene información del producto y realiza análisis nutricional.
    """
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="El archivo debe ser una imagen"
            )
        
        # Leer datos de la imagen
        image_data = await file.read()
        
        # Analizar producto por código de barras
        result = await product_service.analyze_product_by_barcode(image_data)
        
        return {
            "success": True,
            "product_analysis": result,
            "filename": file.filename,
            "message": "Análisis de código de barras completado exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis de código de barras: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/barcode-manual", response_model=Dict)
async def analyze_barcode_manual(barcode: str = Form(...)):
    """
    Analiza un producto a partir de un código de barras ingresado manualmente.
    Obtiene información del producto y realiza análisis nutricional.
    """
    try:
        # Validar formato del código de barras
        if not barcode.isdigit() or len(barcode) not in [8, 12, 13, 14]:
            raise HTTPException(
                status_code=400,
                detail="El código de barras debe contener solo números y tener 8, 12, 13 o 14 dígitos"
            )
        
        # Analizar producto por código de barras manual
        result = await product_service.analyze_product_by_manual_barcode(barcode)
        
        return {
            "success": True,
            "product_analysis": result,
            "barcode": barcode,
            "message": "Análisis de código de barras manual completado exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis de código de barras manual: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/barcode-info", response_model=Dict)
async def get_barcode_info():
    """
    Obtiene información sobre las capacidades de análisis de códigos de barras.
    """
    try:
        barcode_info = {
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
                    "cost": "Completamente gratuito",
                    "api_key_required": False,
                    "priority": 1,
                    "status": "Siempre disponible"
                },
                {
                    "name": "UPC Database",
                    "description": "Base de datos comercial de códigos UPC/EAN",
                    "coverage": "Buena para productos que no están en OpenFoodFacts",
                    "cost": "Requiere suscripción y tarjeta de crédito",
                    "api_key_required": True,
                    "priority": 2,
                    "status": "Opcional - No recomendado"
                }
            ],
            "ai_analysis": {
                "provider": "Google Gemini 1.5 Flash",
                "capabilities": [
                    "Análisis nutricional detallado",
                    "Evaluación de nivel de procesamiento",
                    "Recomendaciones de salud",
                    "Análisis de sostenibilidad",
                    "Comparación con alternativas saludables"
                ]
            },
            "fallback_strategy": "Si no se encuentra el código, se puede usar detección de imagen del producto",
            "response_time": "2-5 segundos promedio"
        }
        
        return {
            "success": True,
            "barcode_capabilities": barcode_info,
            "message": "Información de capacidades de códigos de barras obtenida exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo información de códigos de barras: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))