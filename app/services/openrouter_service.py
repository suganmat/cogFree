import httpx
from typing import Dict, Any
from app.core.config import settings
from app.models.chat import OpenRouterCompletionResponse
from app.services.prompt_service import PromptService
from loguru import logger


class OpenRouterService:
    """Service for interacting with OpenRouter API."""
    
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.base_url = settings.openrouter_base_url
        self.timeout = settings.openrouter_timeout
    
    async def generate_meal_suggestion(self, user_message: str, session_id: str = None) -> OpenRouterCompletionResponse:
        """Generate a meal suggestion using OpenRouter API with single prompt approach."""
        try:
            logger.info(f"Generating meal suggestion for user message: {user_message[:100]}...")
            
            # Prepare the request payload using single prompt approach
            payload = {
                "model": self.model,
                "messages": PromptService.format_openrouter_messages(user_message),
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Meal Suggestor Backend"
            }
            
            # Make the API request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )
                
                response.raise_for_status()
                data = response.json()
            
            # Create and return the OpenRouter completion response
            completion_response = OpenRouterCompletionResponse(**data)
            
            logger.info(f"Successfully generated meal suggestion: {completion_response.suggestion_id}")
            return completion_response
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenRouter API: {e.response.status_code} - {e.response.text}")
            raise Exception(f"OpenRouter API error: {e.response.status_code}")
            
        except httpx.TimeoutException:
            logger.error("Timeout error from OpenRouter API")
            raise Exception("Request timeout - OpenRouter API took too long to respond")
            
        except httpx.RequestError as e:
            logger.error(f"Request error to OpenRouter API: {str(e)}")
            raise Exception("Unable to connect to OpenRouter API")
            
        except Exception as e:
            logger.error(f"Unexpected error generating meal suggestion: {str(e)}")
            raise Exception("Failed to generate meal suggestion. Please try again.")
    
    def update_config(self, **kwargs) -> None:
        """Update service configuration."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.info(f"Updated {key} to {value}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current service configuration."""
        return {
            "model": self.model,
            "base_url": self.base_url,
            "timeout": self.timeout
        }
