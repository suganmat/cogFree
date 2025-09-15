#!/usr/bin/env python3
"""
Simple client example for the Meal Suggestor Backend API
"""
import requests
import json

class MealSuggestorClient:
    """Simple client for the Meal Suggestor API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def health_check(self):
        """Check if the API is healthy."""
        response = requests.get(f"{self.base_url}/api/chat/health")
        return response.json()
    
    def suggest_meal(self, message, session_id=None):
        """Get a meal suggestion."""
        payload = {"message": message}
        if session_id:
            payload["session_id"] = session_id
        
        response = requests.post(
            f"{self.base_url}/api/chat/suggest",
            json=payload
        )
        return response.json()
    
    def chat(self):
        """Interactive chat interface."""
        print("Welcome to Meal Suggestor!")
        print("Type your meal preferences or requirements.")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("Thinking...")
            response = self.suggest_meal(user_input, self.session_id)
            
            if response.get("success"):
                suggestion = response["data"]["suggestion"]
                self.session_id = response["data"]["session_id"]
                print(f"\nDietician: {suggestion}\n")
            else:
                print(f"Error: {response.get('error', 'Unknown error')}\n")

if __name__ == "__main__":
    client = MealSuggestorClient()
    
    # Test health check
    health = client.health_check()
    print(f"API Status: {health.get('status', 'unknown')}")
    
    # Start interactive chat
    client.chat()
