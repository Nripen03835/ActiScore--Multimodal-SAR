#!/usr/bin/env python3
"""
Test script to verify dynamic audio conversion functionality
generates varied content for different video types.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.intellilearn.routes import (
    determine_video_category,
    generate_programming_audio_content,
    generate_data_science_audio_content,
    generate_business_audio_content,
    generate_science_audio_content,
    generate_history_audio_content,
    generate_language_audio_content,
    generate_general_education_audio_content,
    generate_dynamic_audio_conversion
)

def test_video_categorization():
    """Test video category detection"""
    print("=== Testing Video Category Detection ===")
    
    test_videos = [
        {
            "title": "Python Programming Tutorial - Building Web Applications",
            "description": "Learn how to build web applications using Python and Flask framework",
            "keywords": ["python", "programming", "web", "flask", "tutorial"]
        },
        {
            "title": "Data Science Fundamentals - Machine Learning Basics",
            "description": "Introduction to machine learning concepts and data analysis techniques",
            "keywords": ["data", "science", "machine learning", "analysis", "statistics"]
        },
        {
            "title": "Business Strategy Workshop - Market Analysis",
            "description": "Learn strategic planning and market research methodologies",
            "keywords": ["business", "strategy", "market", "planning", "management"]
        },
        {
            "title": "Physics Lecture - Quantum Mechanics Principles",
            "description": "Understanding quantum mechanics and particle physics",
            "keywords": ["physics", "quantum", "science", "particles", "theory"]
        },
        {
            "title": "World History - Ancient Civilizations",
            "description": "Exploring ancient civilizations and their impact on modern society",
            "keywords": ["history", "ancient", "civilizations", "culture", "society"]
        }
    ]
    
    for i, video in enumerate(test_videos, 1):
        category = determine_video_category(video["title"], video["description"], video["keywords"])
        print(f"Video {i}: '{video['title']}' → Category: {category}")
    print()

def test_audio_content_generation():
    """Test audio content generation for different categories"""
    print("=== Testing Audio Content Generation ===")
    
    test_cases = [
        ("programming", "JavaScript Async Programming", ["callbacks", "promises", "async/await"]),
        ("data_science", "Statistical Analysis with Python", ["pandas", "numpy", "visualization"]),
        ("business", "Digital Marketing Strategies", ["SEO", "social media", "analytics"]),
        ("science", "Chemistry Laboratory Techniques", ["experiments", "safety", "equipment"]),
        ("history", "Renaissance Art Movement", ["Leonardo da Vinci", "Michelangelo", "innovation"]),
        ("language", "Spanish Conversation Practice", ["vocabulary", "grammar", "pronunciation"]),
        ("general_education", "Study Skills and Time Management", ["note-taking", "scheduling", "focus"])
    ]
    
    generators = {
        "programming": generate_programming_audio_content,
        "data_science": generate_data_science_audio_content,
        "business": generate_business_audio_content,
        "science": generate_science_audio_content,
        "history": generate_history_audio_content,
        "language": generate_language_audio_content,
        "general_education": generate_general_education_audio_content
    }
    
    for category, title, key_points in test_cases:
        print(f"\n--- {category.upper()} CONTENT ---")
        content = generators[category](title, key_points)
        
        print(f"Title: {title}")
        print(f"Instructor: {content['speakers'][0]['name']}")
        print(f"Audio Text (first 200 chars): {content['text'][:200]}...")
        print(f"Segments: {len(content['segments'])}")
        print(f"Duration: {content['duration']}")
        print(f"Category: {category}")
        print(f"Word Count: {content['word_count']}")
        print(f"Confidence: {content['confidence']}%")

def test_full_audio_conversion():
    """Test complete audio conversion workflow"""
    print("\n=== Testing Complete Audio Conversion Workflow ===")
    
    test_video = {
        "title": "Machine Learning with TensorFlow",
        "description": "Complete guide to building neural networks using TensorFlow and Keras",
        "keywords": ["machine learning", "tensorflow", "neural networks", "deep learning"],
        "summary": "This comprehensive tutorial covers everything from basic neural network concepts to advanced deep learning architectures..."
    }
    
    result = generate_dynamic_audio_conversion(
        video_url="https://example.com/video.mp4",
        summary_type="educational",
        video_summary=test_video,
        enable_audio_conversion=True
    )
    
    if result:
        print(f"Audio conversion successful!")
        print(f"Instructor: {result['speakers'][0]['name']}")
        print(f"Duration: {result['duration']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Segments: {len(result['segments'])}")
        print(f"Audio Quality: {result['audio_quality']}")
        print(f"Sample text: {result['text'][:150]}...")
        print(f"Word Count: {result['word_count']}")
        print(f"Speaker Count: {result['speaker_count']}")
    else:
        print("Audio conversion failed!")

if __name__ == "__main__":
    print("Starting Audio Conversion Tests...\n")
    
    try:
        test_video_categorization()
        test_audio_content_generation()
        test_full_audio_conversion()
        print("\n=== All Tests Completed Successfully! ===")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()