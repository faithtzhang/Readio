from celery import Celery
from app.core.config import REDIS_BROKER_URL

celery_app = Celery("worker", broker=REDIS_BROKER_URL)

@celery_app.task
def generate_audio_script(book_summary: str, voice_style: str, voice_id: str):
    from app.services.llama4_service import generate_summary
    from app.services.tts_service import synthesize
    script = generate_summary(book_summary, voice_style)
    return synthesize(script, voice_id)