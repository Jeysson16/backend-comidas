"""
Endpoints de la API para información de modelos de IA.
Enfocado exclusivamente en Google Gemini.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, List
import logging

from app.ai.food_detection import food_detector

router = APIRouter()
logger = logging.getLogger(__name__)

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