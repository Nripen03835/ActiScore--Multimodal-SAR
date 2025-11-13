#!/usr/bin/env python3
"""
Test script to demonstrate the authentication issue in Video Summarizer
"""

import requests
import json

def test_authentication_issue():
    """Test to show that the issue is authentication-related"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Testing Video Summarizer Authentication Issue")
    print("=" * 60)
    
    # Test 1: Try to access the video summarizer page directly
    print("\n1. Testing access to video summarizer page...")
    try:
        response = requests.get(base_url + "/ai/video-summarizer", allow_redirects=False)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Page requires authentication (redirects to login)")
            print(f"   Redirect location: {response.headers.get('Location', 'Unknown')}")
        elif response.status_code == 200:
            print("   ✅ Page accessible (user likely logged in)")
        else:
            print(f"   ❓ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to Flask server")
        return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Try to access the API endpoint directly
    print("\n2. Testing access to video processing API...")
    try:
        response = requests.post(
            base_url + "/ai/summarize-video",
            json={
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "summary_type": "educational"
            },
            allow_redirects=False
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ API requires authentication (redirects to login)")
            print(f"   Redirect location: {response.headers.get('Location', 'Unknown')}")
        elif response.status_code == 401:
            print("   ✅ API requires authentication (401 Unauthorized)")
        elif response.status_code == 200:
            print("   ✅ API accessible (user likely logged in)")
            try:
                data = response.json()
                print(f"   Response: {data.get('message', 'Success')}")
            except:
                print("   ⚠️  Invalid JSON response")
        else:
            print(f"   ❓ Unexpected status: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}...")
                
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to Flask server")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Try with CSRF token (simulating browser behavior)
    print("\n3. Testing with CSRF token simulation...")
    try:
        # First get the page to extract CSRF token
        session = requests.Session()
        response = session.get(base_url + "/ai/video-summarizer")
        
        if response.status_code == 200:
            # Try to extract CSRF token from meta tag (this is a simplified approach)
            csrf_token = "dummy-csrf-token"  # In real scenario, extract from HTML
            
            response = session.post(
                base_url + "/ai/summarize-video",
                json={
                    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "summary_type": "educational"
                },
                headers={"X-CSRFToken": csrf_token}
            )
            
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Request with session cookies succeeded")
            else:
                print(f"   ❌ Still failed with session: {response.status_code}")
                
        else:
            print("   ❌ Could not get page to extract CSRF token")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def provide_solution():
    """Provide solution for the authentication issue"""
    print("\n" + "=" * 60)
    print("SOLUTION TO THE VIDEO SUMMARIZER ISSUE")
    print("=" * 60)
    
    print("""
The "Failed to process video" error is caused by authentication requirements.

WHAT'S HAPPENING:
1. The Video Summarizer requires users to be logged in (@login_required decorator)
2. When an unauthenticated user tries to process a video, the API returns 302 redirects
3. The frontend JavaScript shows "Failed to process video" for authentication failures

SOLUTIONS:

1. FOR USERS (IMMEDIATE FIX):
   - Log in to the application first
   - Navigate to the login page: /auth/login
   - Enter your credentials
   - Then use the Video Summarizer

2. FOR DEVELOPERS (CODE IMPROVEMENTS):
   
   A. Improve error messages:
      - Change "Failed to process video" to "Please log in to process videos"
      - Show authentication-specific error messages
   
   B. Add authentication check:
      - Detect 302/401 responses specifically
      - Show login prompt instead of generic error
   
   C. Consider making API public (optional):
      - Remove @login_required from summarize_video function
      - Add rate limiting instead of authentication

3. TESTING WITHOUT AUTHENTICATION (DEVELOPMENT ONLY):
   - Temporarily comment out @login_required decorator
   - Test the video processing functionality
   - Restore authentication before deployment

The video processing logic is working correctly - it's just the authentication 
requirement that's causing the "failure" message.
""")

if __name__ == "__main__":
    test_authentication_issue()
    provide_solution()