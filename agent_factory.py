import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel

def get_text_model_instance():
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    model_name = os.getenv("MODEL", "gpt-4o-2024-08-06")
    
    try:
        # Initialize the model with just the model name and let it handle the API client
        return OpenAIModel(
            model_name=model_name,
            # No client or openai_client parameter
        )
    except Exception as e:
        raise Exception(f"Failed to initialize OpenAI model: {str(e)}")