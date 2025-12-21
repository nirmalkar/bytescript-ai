#!/usr/bin/env python3
"""
Test script for the chat API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_health_endpoint():
    """Test the health endpoint (requires auth)"""
    print("Testing health endpoint...")
    
    # This will fail without proper Firebase token
    headers = {
        "Authorization": "Bearer mock_token",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    print(f"Health endpoint status: {response.status_code}")
    print(f"Health endpoint response: {response.text}")
    print()

def test_chat_endpoint():
    """Test the chat completion endpoint"""
    print("Testing chat completion endpoint...")
    
    # Mock request payload
    payload = {
        "messages": [
            {"role": "user", "content": "Write a simple Python function that adds two numbers"}
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    # This will fail without proper Firebase token
    headers = {
        "Authorization": "Bearer mock_token",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/chat/completions", 
                           json=payload, 
                           headers=headers)
    
    print(f"Chat endpoint status: {response.status_code}")
    print(f"Chat endpoint response: {response.text}")
    print()

def test_ollama_direct():
    """Test Ollama directly"""
    print("Testing Ollama directly...")
    
    payload = {
        "model": "deepseek-coder:1.3b",
        "prompt": "Write a simple Python function that adds two numbers",
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", 
                               json=payload, 
                               timeout=30)
        
        print(f"Ollama status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Ollama response: {data.get('response', 'No response')[:200]}...")
        else:
            print(f"Ollama error: {response.text}")
    except Exception as e:
        print(f"Ollama connection error: {e}")
    
    print()

if __name__ == "__main__":
    print("=== API Test Script ===")
    print()
    
    # Test Ollama first
    test_ollama_direct()
    
    # Test API endpoints (will fail without proper auth)
    test_health_endpoint()
    test_chat_endpoint()
    
    print("=== Test Complete ===")
    print("\nNote: The API endpoints require Firebase authentication.")
    print("To test with real authentication:")
    print("1. Set up Firebase project")
    print("2. Configure FIREBASE_CREDENTIALS_PATH")
    print("3. Get a Firebase ID token")
    print("4. Replace 'mock_token' with the real token")
