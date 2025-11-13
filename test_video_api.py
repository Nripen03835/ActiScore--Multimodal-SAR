#!/usr/bin/env python3
"""
Test script to debug video processing API issues
"""

import requests
import json
import sys

def test_video_processing_api():
    """Test the video processing API with different scenarios"""
    
    # Test with a sample YouTube URL
    test_cases = [
        {
            "name": "Valid YouTube URL",
            "data": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "summary_type": "educational",
                "options": {
                    "enableAudioConversion": True,
                    "audioQuality": "medium",
                    "speakerRecognition": "disabled",
                    "includeAudioTimestamps": True
                }
            }
        },
        {
            "name": "Invalid URL format",
            "data": {
                "video_url": "not-a-valid-url",
                "summary_type": "educational",
                "options": {}
            }
        },
        {
            "name": "Missing video URL",
            "data": {
                "summary_type": "educational",
                "options": {}
            }
        },
        {
            "name": "Invalid summary type",
            "data": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "summary_type": "invalid-type",
                "options": {}
            }
        }
    ]
    
    base_url = "http://localhost:5000"  # Adjust if your Flask app runs on different port
    endpoint = "/ai/summarize-video"
    
    print("Testing Video Processing API")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        print(f"Data: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                base_url + endpoint,
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response text (first 500 chars): {response.text[:500]}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SUCCESS:")
                print(f"Message: {result.get('message', 'No message')}")
                print(f"Summary title: {result.get('summary', {}).get('title', 'No title')}")
                if result.get('audio_conversion'):
                    print(f"Audio instructor: {result['audio_conversion']['speakers'][0]['name']}")
            else:
                result = response.json()
                print("❌ ERROR:")
                print(f"Error message: {result.get('error', 'Unknown error')}")
                if 'details' in result:
                    print(f"Details: {result['details']}")
                    
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR: Could not connect to Flask server")
            print("Make sure your Flask application is running on port 5000")
            return
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {str(e)}")
        
        print("-" * 30)

def test_csrf_token():
    """Test if CSRF token is required and accessible"""
    print("\n\nTesting CSRF Token Requirements")
    print("=" * 50)
    
    try:
        # First, try to access the video summarizer page to get CSRF token
        base_url = "http://localhost:5000"
        response = requests.get(base_url + "/ai/video-summarizer")
        
        if response.status_code == 200:
            print("✅ Video summarizer page accessible")
            # Look for CSRF token in the response
            if 'csrf_token' in response.text or 'csrf-token' in response.text:
                print("✅ CSRF token found in page")
            else:
                print("⚠️  CSRF token not found in page (might be in meta tag)")
        else:
            print(f"❌ Could not access video summarizer page: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server")
    except Exception as e:
        print(f"❌ Error accessing page: {str(e)}")

if __name__ == "__main__":
    print("Video Processing API Test Script")
    print("Make sure your Flask application is running!")
    print("\nTo start Flask app, run: flask run")
    print("=" * 50)
    
    input("Press Enter to start testing...")
    
    test_csrf_token()
    test_video_processing_api()
    
    print("\n" + "=" * 50)
    print("Testing completed!")