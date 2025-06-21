import os

class Settings:
    LLAMA4_API_KEY = os.getenv("LLAMA4_API_KEY")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = "us-west-2"  # Adjust as needed
    BEDROCK_MODEL_ID = "luma.ray-v2:0"

settings = Settings()
