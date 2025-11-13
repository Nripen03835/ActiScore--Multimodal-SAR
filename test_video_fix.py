#!/usr/bin/env python3
"""
Simple test to verify the analyze_video_content function fix
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import the function we fixed
from app.intellilearn.routes import determine_video_category

def test_determine_video_category():
    """Test the determine_video_category function that replaced analyze_video_content"""
    
    # Test cases
    test_cases = [
        {
            'title': 'Python Programming Tutorial',
            'description': 'Learn Python basics and advanced concepts',
            'keywords': ['python', 'programming', 'tutorial'],
            'expected': 'programming'
        },
        {
            'title': 'Machine Learning Fundamentals',
            'description': 'Introduction to data science and AI',
            'keywords': ['machine learning', 'data science', 'AI'],
            'expected': 'data_science'
        },
        {
            'title': 'Business Strategy Workshop',
            'description': 'Marketing and entrepreneurship tips',
            'keywords': ['business', 'marketing', 'startup'],
            'expected': 'business'
        },
        {
            'title': 'Physics Experiment Demo',
            'description': 'Chemistry and biology concepts',
            'keywords': ['physics', 'chemistry', 'biology'],
            'expected': 'science'
        },
        {
            'title': 'Ancient Civilizations',
            'description': 'Historical events and wars',
            'keywords': ['history', 'ancient', 'civilization'],
            'expected': 'history'
        },
        {
            'title': 'Spanish Grammar Lesson',
            'description': 'Learn vocabulary and pronunciation',
            'keywords': ['language', 'grammar', 'vocabulary'],
            'expected': 'language'
        },
        {
            'title': 'General Educational Content',
            'description': 'Various topics and subjects',
            'keywords': ['education', 'learning', 'knowledge'],
            'expected': 'general_education'
        }
    ]
    
    print("Testing determine_video_category function...")
    print("=" * 50)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['title']}")
        result = determine_video_category(
            test_case['title'],
            test_case['description'],
            test_case['keywords']
        )
        
        if result == test_case['expected']:
            print(f"✅ PASS: Expected '{test_case['expected']}', got '{result}'")
        else:
            print(f"❌ FAIL: Expected '{test_case['expected']}', got '{result}'")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! The function is working correctly.")
        print("✅ The analyze_video_content function fix is successful.")
    else:
        print("❌ Some tests failed. The function needs more work.")
    
    return all_passed

if __name__ == "__main__":
    test_determine_video_category()