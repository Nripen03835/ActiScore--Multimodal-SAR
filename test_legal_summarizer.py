#!/usr/bin/env python3
"""
Test script for Legal Summarizer API
"""
import requests
import json

# Create a session to maintain cookies
session = requests.Session()

def test_legal_summarizer():
    # First, let's check if we can access the page
    print("Testing page access...")
    page_response = session.get('http://localhost:5000/ai/legal-summarizer')
    print(f"Page Status Code: {page_response.status_code}")
    
    if page_response.status_code == 302:
        print("Page requires authentication - redirecting to login")
        # Try to get the login page
        login_response = session.get('http://localhost:5000/auth/login')
        print(f"Login Page Status: {login_response.status_code}")
    
    # Test data
    test_text = "This is a sample legal document. The parties agree to the terms and conditions set forth in this agreement. The contract shall be binding upon both parties. All disputes shall be resolved through arbitration."
    
    # Prepare the data
    data = {
        'text_input': test_text
    }
    
    try:
        # Make the request with session (includes cookies)
        response = session.post('http://localhost:5000/ai/summarize-legal-document', data=data)
        
        print(f"\nAPI Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Success! Response: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response is not JSON. Content: {response.text[:500]}...")
        elif response.status_code == 302:
            print("API requires authentication - redirect detected")
            print(f"Redirect location: {response.headers.get('Location')}")
        else:
            print(f"Error Response: {response.text[:500]}...")
            
    except Exception as e:
        print(f"Request failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_legal_summarizer()