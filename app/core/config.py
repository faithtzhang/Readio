import os
from typing import Dict, List

# API Keys
LLAMA4_API_BASE = os.getenv("LLAMA4_API_BASE")
LLAMA4_API_KEY = os.getenv("LLAMA4_API_KEY")
PLAYHT_API_KEY = os.getenv("PLAYHT_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Redis Configuration
REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL", "redis://localhost:6379/0")

# Voice Options for TTS
VOICE_OPTIONS = {
    "playful_child": {
        "name": "Playful Child Voice",
        "description": "Energetic and engaging voice for children's books",
        "playht_voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
        "elevenlabs_voice": "21m00Tcm4TlvDq8ikWAM",
        "polly_voice": "Joanna"
    },
    "calm_senior": {
        "name": "Calm Senior Voice", 
        "description": "Gentle and soothing voice for relaxation",
        "playht_voice": "s3://voice-cloning-zero-shot/8b0d7b0a-5c1a-4b1a-8c1a-5c1a4b1a8c1a/male-cs/manifest.json",
        "elevenlabs_voice": "EXAVITQu4vr4xnSDxMaL",
        "polly_voice": "Matthew"
    },
    "professional": {
        "name": "Professional Voice",
        "description": "Clear and confident voice for business content",
        "playht_voice": "s3://voice-cloning-zero-shot/9c0d8c1b-6d2b-5c2b-9d2b-6d2b5c2b9d2b/female-cs/manifest.json",
        "elevenlabs_voice": "21m00Tcm4TlvDq8ikWAM",
        "polly_voice": "Salli"
    }
}

# Default voice style
DEFAULT_VOICE = "professional"

# TTS provider priority (fallback order)
TTS_PROVIDERS = ["playht", "elevenlabs", "polly"] 