#!/usr/bin/env python3
"""
Simple test script for the Meal Suggestor Backend API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/api/chat/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_meal_suggestion(message):
    """Test meal suggestion endpoint."""
    print(f"Testing meal suggestion with: '{message}'")
    response = requests.post(
        f"{BASE_URL}/api/chat/suggest",
        json={"message": message}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    if data.get("success"):
        print(f"Suggestion: {data['data']['suggestion'][:200]}...")
        print(f"Session ID: {data['data']['session_id']}")
    else:
        print(f"Error: {data.get('error')}")
    print()

def main():
    """Run all tests."""
    print("Meal Suggestor Backend API Test")
    print("=" * 40)
    
    # Test health check
    test_health()
    
    # Test meal suggestions
    test_messages = [
        "I want a healthy vegetarian meal for dinner",
        "I need a quick lunch for work",
        "I'm looking for a high-protein breakfast",
        "I want something light and refreshing for lunch"
    ]
    
    for message in test_messages:
        test_meal_suggestion(message)
        time.sleep(1)  # Small delay between requests

if __name__ == "__main__":
    main()
