import requests
import boto3
from typing import Optional, Dict
from app.core.config import (
    PLAYHT_API_KEY, ELEVENLABS_API_KEY, AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY, AWS_REGION, VOICE_OPTIONS, TTS_PROVIDERS, DEFAULT_VOICE
)


class SimpleTTSService:
    """Simple TTS service that calls existing providers with fallback."""
    
    def __init__(self):
        self.polly_client = None
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            self.polly_client = boto3.client(
                'polly',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
    
    def get_voice_options(self) -> Dict:
        """Get available voice options."""
        return VOICE_OPTIONS
    
    def synthesize_with_playht(self, text: str, voice_id: str) -> Optional[str]:
        """Synthesize audio using Play.ht API."""
        try:
            headers = {
                "Authorization": f"Bearer {PLAYHT_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "voice": voice_id,
                "content": text,
                "title": "Readio Audiobook"
            }
            response = requests.post(
                "https://api.play.ht/api/v2/tts",
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("url")
        except Exception as e:
            print(f"Play.ht synthesis failed: {e}")
        return None
    
    def synthesize_with_elevenlabs(self, text: str, voice_id: str) -> Optional[str]:
        """Synthesize audio using ElevenLabs API."""
        try:
            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                # For ElevenLabs, we'd typically save the audio file
                # For now, return a placeholder URL
                return f"elevenlabs_audio_{voice_id}.mp3"
        except Exception as e:
            print(f"ElevenLabs synthesis failed: {e}")
        return None
    
    def synthesize_with_polly(self, text: str, voice_id: str) -> Optional[str]:
        """Synthesize audio using Amazon Polly."""
        if not self.polly_client:
            return None
        
        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id
            )
            
            # Save the audio file and return the URL
            audio_filename = f"polly_audio_{voice_id}.mp3"
            with open(audio_filename, 'wb') as file:
                file.write(response['AudioStream'].read())
            
            return audio_filename
        except Exception as e:
            print(f"Polly synthesis failed: {e}")
        return None
    
    def synthesize(self, text: str, voice_style: Optional[str] = None) -> Optional[Dict]:
        """Synthesize audio with provider fallback mechanism."""
        if not voice_style or voice_style not in VOICE_OPTIONS:
            voice_style = DEFAULT_VOICE
        
        voice_config = VOICE_OPTIONS[voice_style]
        
        # Try each provider in order until one succeeds
        for provider in TTS_PROVIDERS:
            voice_id = voice_config.get(f"{provider}_voice")
            if not voice_id:
                continue
            
            audio_url = None
            
            if provider == "playht":
                audio_url = self.synthesize_with_playht(text, voice_id)
            elif provider == "elevenlabs":
                audio_url = self.synthesize_with_elevenlabs(text, voice_id)
            elif provider == "polly":
                audio_url = self.synthesize_with_polly(text, voice_id)
            
            if audio_url:
                return {
                    "audio_url": audio_url,
                    "provider": provider,
                    "voice_style": voice_style,
                    "voice_id": voice_id
                }
        
        return None


# Backward compatibility function
def synthesize(text: str, voice_id: str) -> str:
    """Legacy function for backward compatibility."""
    service = SimpleTTSService()
    result = service.synthesize(text, "professional")
    return result["audio_url"] if result else "" 