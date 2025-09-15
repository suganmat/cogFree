from pydantic import BaseModel, Field
from typing import List, Optional, Any
import uuid
from datetime import datetime


class ChatMessage(BaseModel):
    """Represents a single message in a chat conversation."""
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    """Request model for generating a meal suggestion."""
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None


class MealSuggestion(BaseModel):
    """Meal suggestion model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_input: str
    session_id: Optional[str] = None


class OpenRouterCompletionResponse(BaseModel):
    """Response model for OpenRouter API completion."""
    id: str
    object: str
    created: int
    model: str
    usage: dict
    choices: List[dict]
    
    @property
    def content(self) -> str:
        """Extracts the content from the first choice."""
        if self.choices and len(self.choices) > 0:
            return self.choices[0].get("message", {}).get("content", "")
        return ""
    
    @property
    def suggestion_id(self) -> str:
        """Returns the ID of the completion."""
        return self.id
    
    @property
    def timestamp(self) -> datetime:
        """Returns the creation timestamp as a datetime object."""
        return datetime.fromtimestamp(self.created)


class StructuredMealSuggestion(BaseModel):
    """Structured meal suggestion model for JSON responses."""
    meal_name: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    prep_time: str
    cook_time: str
    servings: str
    difficulty: str
    cuisine_type: str
    dietary_tags: List[str]
    nutritional_benefits: List[str]
    calories_per_serving: int
    protein_per_serving: str
    carbs_per_serving: str
    fat_per_serving: str


class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "1.0.0"


class HealthResponse(BaseModel):
    """Health check response model."""
    success: bool
    message: str
    timestamp: datetime
    version: str
    status: str = "healthy"
