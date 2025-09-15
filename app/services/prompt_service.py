from typing import Tuple
from loguru import logger


class PromptService:
    """Service for managing prompt templates."""
    
    # Dietician prompt template with JSON output request
    DIETICIAN_SYSTEM_PROMPT = (
        "You are an expert dietician with extensive knowledge of nutrition, "
        "meal planning, and dietary requirements. Provide helpful, accurate, "
        "and personalized meal suggestions based on user preferences, dietary "
        "restrictions, and nutritional needs. Be specific about ingredients, "
        "cooking methods, and nutritional benefits.\n\n"
        "IMPORTANT: You must respond with a valid JSON object in the following format:\n"
        '{{\n'
        '  "meal_name": "string",\n'
        '  "description": "string",\n'
        '  "ingredients": ["list of ingredients"],\n'
        '  "instructions": ["list of cooking steps"],\n'
        '  "prep_time": "string (e.g., 15 minutes)",\n'
        '  "cook_time": "string (e.g., 30 minutes)",\n'
        '  "servings": "string (e.g., 2-3 servings)",\n'
        '  "difficulty": "string (Easy/Medium/Hard)",\n'
        '  "cuisine_type": "string (e.g., Mediterranean, Asian, etc.)",\n'
        '  "dietary_tags": ["list of dietary tags like vegetarian, gluten-free, etc."],\n'
        '  "nutritional_benefits": ["list of key nutritional benefits"],\n'
        '  "calories_per_serving": "number",\n'
        '  "protein_per_serving": "string (e.g., 25g)",\n'
        '  "carbs_per_serving": "string (e.g., 45g)",\n'
        '  "fat_per_serving": "string (e.g., 12g)"\n'
        '}}\n\n'
        "User's request: {user_message}"
    )
    
    @classmethod
    def get_dietician_prompt(cls, user_message: str) -> str:
        """Get the formatted dietician prompt with user message."""
        return cls.DIETICIAN_SYSTEM_PROMPT.format(user_message=user_message)
    
    @classmethod
    def validate_user_message(cls, message: str) -> Tuple[bool, str]:
        """Validate user message input."""
        if not message or not message.strip():
            return False, "Message cannot be empty"
        
        if len(message) > 1000:
            return False, "Message too long (max 1000 characters)"
        
        return True, ""
    
    @classmethod
    def format_openrouter_messages(cls, user_message: str) -> list[dict]:
        """Format messages for OpenRouter API using single system prompt approach."""
        return [
            {
                "role": "system",
                "content": cls.get_dietician_prompt(user_message)
            },
            {
                "role": "user", 
                "content": user_message
            }
        ]
