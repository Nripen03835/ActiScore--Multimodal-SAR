#!/usr/bin/env python3
"""
Simple test to check the API response
"""
import requests

# Test with a simple session
session = requests.Session()

# First, let's try to access the page to see what happens
print("=== Testing Page Access ===")
response = session.get('http://localhost:5000/ai/legal-summarizer')
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")
print(f"Headers: {dict(response.headers)}")

# Now test the API
print("\n=== Testing API ===")
data = {'text_input': 'This is a test legal document.'}
response = session.post('http://localhost:5000/ai/summarize-legal-document', data=data)
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")
print(f"Headers: {dict(response.headers)}")
print(f"Content Type: {response.headers.get('content-type', 'unknown')}")

if response.status_code == 200:
    if 'application/json' in response.headers.get('content-type', ''):
        print(f"JSON Response: {response.json()}")
    else:
        print(f"HTML Response: {response.text[:200]}...")
elif response.status_code == 302:
    print(f"Redirected to: {response.headers.get('Location')}")
else:
    print(f"Response: {response.text[:200]}...")