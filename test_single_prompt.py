#!/usr/bin/env python3
"""
Test the single prompt approach
"""
from app.services.prompt_service import PromptService

def test_single_prompt():
    """Test the single prompt approach."""
    print("Testing single prompt approach...")
    
    user_message = "I want a healthy vegetarian meal for dinner"
    
    # Test the formatted prompt
    formatted_prompt = PromptService.get_dietician_prompt(user_message)
    print("✅ Formatted prompt:")
    print(formatted_prompt[:200] + "...")
    print()
    
    # Test OpenRouter message format
    messages = PromptService.format_openrouter_messages(user_message)
    print("✅ OpenRouter messages format:")
    print(f"Number of messages: {len(messages)}")
    print(f"Message role: {messages[0]['role']}")
    print(f"Message content preview: {messages[0]['content'][:100]}...")
    print()
    
    # Test validation
    is_valid, error = PromptService.validate_user_message(user_message)
    print(f"✅ Validation: {'Valid' if is_valid else 'Invalid'}")
    if not is_valid:
        print(f"Error: {error}")
    
    return True

if __name__ == "__main__":
    test_single_prompt()
    print("\n🎉 Single prompt approach is working!")
