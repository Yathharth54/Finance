import os
from openai import AsyncOpenAI  # Updated import
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel

def get_text_model_instance():
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=api_key)
    
    model_name = os.getenv("MODEL", "gpt-4o-2024-08-06")  # Added default model
    
    try:
        return OpenAIModel(
            model_name=model_name,
            openai_client=client
        )
    except Exception as e:
        raise Exception(f"Failed to initialize OpenAI model: {str(e)}")