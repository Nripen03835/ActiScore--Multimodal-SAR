#!/usr/bin/env python3
"""
Simple test script to verify the ActiScore application is working
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_main_pages():
    """Test main application pages"""
    pages = [
        ('/', 'Home page'),
        ('/auth/login', 'Login page'),
        ('/auth/register', 'Register page')
    ]
    
    all_working = True
    
    for url, name in pages:
        try:
            response = requests.get(f'http://localhost:5000{url}')
            if response.status_code == 200:
                print(f"✅ {name} working")
            else:
                print(f"❌ {name} failed: {response.status_code}")
                all_working = False
        except Exception as e:
            print(f"❌ {name} error: {e}")
            all_working = False
    
    return all_working

def test_model_files():
    """Test that model files exist"""
    model_files = [
        ('models/fer_model.pkl', 'FER model'),
        ('models/ser_model.pkl', 'SER model'),
        ('models/fusion_model.pkl', 'Fusion model'),
        ('models/feature_scaler_efficient.pkl', 'Feature scaler'),
        ('models/model_metadata.json', 'Model metadata')
    ]
    
    all_exist = True
    
    for file_path, name in model_files:
        if os.path.exists(file_path):
            print(f"✅ {name} exists")
        else:
            print(f"❌ {name} missing: {file_path}")
            all_exist = False
    
    return all_exist

def main():
    """Main test function"""
    print("🚀 Testing ActiScore Application")
    print("=" * 50)
    
    # Test health endpoint
    health_working = test_health_endpoint()
    
    if not health_working:
        print("\n❌ Application is not running. Please start it first:")
        print("python run.py")
        return
    
    print("\n📄 Testing main pages...")
    pages_working = test_main_pages()
    
    print("\n🧠 Testing model files...")
    models_exist = test_model_files()
    
    print("\n" + "=" * 50)
    
    if health_working and pages_working and models_exist:
        print("✅ All tests passed! Application is ready.")
        print("\n🌐 Application URLs:")
        print("   Main: http://localhost:5000")
        print("   Login: http://localhost:5000/auth/login")
        print("   Register: http://localhost:5000/auth/register")
        print("\n👤 Default credentials:")
        print("   Admin: admin@example.com / admin123")
        print("   Demo: john@example.com / password123")
    else:
        print("❌ Some tests failed. Please check the output above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure the application is running")
        print("   2. Check that all dependencies are installed")
        print("   3. Verify model files are created")
        print("   4. Check application logs for errors")

if __name__ == '__main__':
    import os
    main()