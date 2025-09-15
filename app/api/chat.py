from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, APIResponse, HealthResponse, StructuredMealSuggestion
from app.services.openrouter_service import OpenRouterService
from app.services.prompt_service import PromptService
from app.services.json_parser import JSONParser
from app.core.config import settings
from loguru import logger
import uuid
import time
import json

router = APIRouter()

# Initialize OpenRouter service
openrouter_service = OpenRouterService()


@router.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint with structured response."""
    try:
        start_time = time.time()
        
        # Test OpenRouter connection
        openrouter_status = "connected"
        try:
            # Quick test to see if we can reach OpenRouter
            import httpx
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get("https://openrouter.ai")
                if response.status_code != 200:
                    openrouter_status = "unreachable"
        except:
            openrouter_status = "unreachable"
        
        uptime = time.time() - start_time
        
        health_data = {
            "status": "healthy",
            "version": settings.app_version,
            "uptime_seconds": round(uptime, 2),
            "openrouter_status": openrouter_status,
            "model": settings.openrouter_model,
            "timestamp": time.time(),
            "features": {
                "json_responses": True,
                "structured_parsing": True,
                "session_management": True
            }
        }
        
        return APIResponse(
            success=True,
            message="Meal Suggestor Backend is healthy",
            data=health_data
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return APIResponse(
            success=False,
            message="Health check failed",
            error={"type": "health_check_error", "details": str(e)}
        )


@router.post("/suggest", response_model=APIResponse)
async def generate_meal_suggestion(request: ChatRequest):
    """Generate a meal suggestion based on user input."""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        # Validate the user message
        is_valid, error_message = PromptService.validate_user_message(request.message)
        if not is_valid:
            return APIResponse(
                success=False,
                message="Validation failed",
                error={"type": "validation_error", "details": error_message},
                request_id=request_id
            )
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        logger.info(f"Processing meal suggestion request {request_id} for session: {session_id}")
        
        # Generate meal suggestion
        suggestion = await openrouter_service.generate_meal_suggestion(
            user_message=request.message,
            session_id=session_id
        )
        
        # Parse the structured response
        structured_suggestion = JSONParser.parse_meal_suggestion(suggestion.content)
        
        if structured_suggestion:
            # Return structured JSON response
            response_data = {
                "message": request.message,
                "suggestion": structured_suggestion.dict(),
                "session_id": session_id,
                "timestamp": suggestion.timestamp.isoformat() if hasattr(suggestion.timestamp, 'isoformat') else str(suggestion.timestamp),
                "suggestion_id": suggestion.suggestion_id
            }
            
            logger.info(f"Successfully processed structured meal suggestion {suggestion.suggestion_id} for session: {session_id}")
            
            return APIResponse(
                success=True,
                message="Structured meal suggestion generated successfully",
                data=response_data,
                request_id=request_id
            )
        else:
            # Fallback to raw response if JSON parsing fails
            logger.warning(f"JSON parsing failed for suggestion {suggestion.suggestion_id}, using fallback")
            
            fallback_suggestion = JSONParser.create_fallback_response(request.message)
            
            response_data = {
                "message": request.message,
                "suggestion": fallback_suggestion.dict(),
                "raw_response": suggestion.content,  # Include raw response for debugging
                "session_id": session_id,
                "timestamp": suggestion.timestamp.isoformat() if hasattr(suggestion.timestamp, 'isoformat') else str(suggestion.timestamp),
                "suggestion_id": suggestion.suggestion_id
            }
            
            return APIResponse(
                success=True,
                message="Meal suggestion generated (fallback format)",
                data=response_data,
                request_id=request_id
            )
            
    except HTTPException as http_exc:
        logger.error(f"HTTP Exception in meal suggestion: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error generating meal suggestion: {str(e)}")
        return APIResponse(
            success=False,
            message="Failed to generate meal suggestion",
            error={"type": "generation_error", "details": str(e)},
            request_id=request_id
        )


@router.get("/config", response_model=APIResponse)
async def get_config():
    """Retrieve current application configuration."""
    try:
        config_data = {
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "debug_mode": settings.debug,
            "openrouter_model": settings.openrouter_model,
            "openrouter_base_url": settings.openrouter_base_url,
            "allowed_origins": settings.allowed_origins,
            "log_level": settings.log_level
        }
        return APIResponse(
            success=True,
            message="Configuration retrieved successfully",
            data=config_data
        )
    except Exception as e:
        logger.error(f"Error retrieving configuration: {str(e)}")
        return APIResponse(
            success=False,
            message="Failed to retrieve configuration",
            error={"type": "config_error", "details": str(e)}
        )


@router.get("/stats", response_model=APIResponse)
async def get_stats():
    """Retrieve application statistics."""
    try:
        stats_data = {
            "total_requests": 0,  # Placeholder
            "successful_requests": 0,  # Placeholder
            "failed_requests": 0,  # Placeholder
            "average_response_time_ms": 0,  # Placeholder
            "last_updated": time.time()
        }
        return APIResponse(
            success=True,
            message="Application statistics retrieved successfully",
            data=stats_data
        )
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        return APIResponse(
            success=False,
            message="Failed to retrieve statistics",
            error={"type": "stats_error", "details": str(e)}
        )
