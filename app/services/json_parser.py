import json
import re
from typing import Dict, Any, Optional
from app.models.chat import StructuredMealSuggestion
from loguru import logger


class JSONParser:
    """Service for parsing JSON responses from LLM."""
    
    @staticmethod
    def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON object from text that may contain other content.
        
        Args:
            text (str): The text containing JSON
            
        Returns:
            Optional[Dict[str, Any]]: Parsed JSON object or None if extraction fails
        """
        try:
            # First, try to parse the entire text as JSON
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass
        
        # If that fails, try to extract JSON from the text
        # Look for JSON object patterns
        json_patterns = [
            r'\{.*\}',  # Basic object pattern
            r'```json\s*(\{.*?\})\s*```',  # JSON in code blocks
            r'```\s*(\{.*?\})\s*```',  # JSON in generic code blocks
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match.strip())
                except json.JSONDecodeError:
                    continue
        
        # If no JSON found, try to find the first complete JSON object
        start_idx = text.find('{')
        if start_idx != -1:
            brace_count = 0
            end_idx = start_idx
            
            for i, char in enumerate(text[start_idx:], start_idx):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i
                        break
            
            if brace_count == 0:  # Found complete JSON object
                try:
                    json_str = text[start_idx:end_idx + 1]
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
        
        logger.warning("Could not extract valid JSON from LLM response")
        return None
    
    @staticmethod
    def parse_meal_suggestion(llm_response: str) -> Optional[StructuredMealSuggestion]:
        """
        Parse LLM response into structured meal suggestion.
        
        Args:
            llm_response (str): Raw response from LLM
            
        Returns:
            Optional[StructuredMealSuggestion]: Parsed structured data or None if parsing fails
        """
        try:
            # Extract JSON from the response
            json_data = JSONParser.extract_json_from_text(llm_response)
            if not json_data:
                logger.error("No valid JSON found in LLM response")
                return None
            
            # Validate and create structured meal suggestion
            meal_suggestion = StructuredMealSuggestion(**json_data)
            logger.info(f"Successfully parsed structured meal suggestion: {meal_suggestion.meal_name}")
            return meal_suggestion
            
        except Exception as e:
            logger.error(f"Error parsing meal suggestion: {str(e)}")
            return None
    
    @staticmethod
    def create_fallback_response(user_message: str) -> StructuredMealSuggestion:
        """
        Create a fallback structured response when JSON parsing fails.
        
        Args:
            user_message (str): Original user message
            
        Returns:
            StructuredMealSuggestion: Fallback structured data
        """
        return StructuredMealSuggestion(
            meal_name="Healthy Meal Suggestion",
            description=f"Based on your request: {user_message}",
            ingredients=["Please check the full response for detailed ingredients"],
            instructions=["Please check the full response for detailed instructions"],
            prep_time="Varies",
            cook_time="Varies", 
            servings="2-4",
            difficulty="Medium",
            cuisine_type="International",
            dietary_tags=["healthy"],
            nutritional_benefits=["Nutritious and balanced"],
            calories_per_serving=300,
            protein_per_serving="15g",
            carbs_per_serving="30g",
            fat_per_serving="10g"
        )
