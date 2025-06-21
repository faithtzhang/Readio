#!/usr/bin/env python3
"""
Test script to verify routes are working correctly.
"""

import requests
import json
import os

# Test configuration
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_recommend():
    """Test the recommend endpoint."""
    print("\nTesting recommend endpoint...")
    try:
        payload = {"labels": ["fiction", "adventure"]}
        response = requests.post(f"{BASE_URL}/recommend/", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommend passed: {len(data.get('recommendations', []))} recommendations")
            return True
        else:
            print(f"❌ Recommend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Recommend error: {e}")
        return False

def test_summarize():
    """Test the summarize endpoint."""
    print("\nTesting summarize endpoint...")
    try:
        payload = {
            "summary": "This is a sample book summary for testing purposes.",
            "voice_style": "professional"
        }
        response = requests.post(f"{BASE_URL}/summarize/", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Summarize passed: {len(data.get('script', ''))} characters")
            return True
        else:
            print(f"❌ Summarize failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Summarize error: {e}")
        return False

def test_tts():
    """Test the TTS endpoint."""
    print("\nTesting TTS endpoint...")
    try:
        payload = {
            "script": "This is a test script for text-to-speech conversion.",
            "voice_id": "professional"
        }
        response = requests.post(f"{BASE_URL}/tts/", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS passed: {data.get('audio_url', 'No URL')}")
            return True
        else:
            print(f"❌ TTS failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def test_video_perspectives():
    """Test the video perspectives endpoint."""
    print("\nTesting video perspectives endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/video/perspectives")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Video perspectives passed: {len(data.get('perspectives', {}))} perspectives")
            return True
        else:
            print(f"❌ Video perspectives failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Video perspectives error: {e}")
        return False

def test_video_voices():
    """Test the video voices endpoint."""
    print("\nTesting video voices endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/video/voices")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Video voices passed: {data.get('total_count', 0)} voices available")
            return True
        else:
            print(f"❌ Video voices failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Video voices error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Readio API Routes")
    print("=" * 50)
    
    # Check if server is running
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server first:")
        print("   source venv/bin/activate")
        print("   python -m uvicorn app.main:app --reload")
        return
    
    # Run tests
    tests = [
        test_recommend,
        test_summarize,
        test_tts,
        test_video_perspectives,
        test_video_voices
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The routes are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main() 