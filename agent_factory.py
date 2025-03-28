import os
import openai
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel

def get_text_model_instance():
    # Load environment variables from .env file
    load_dotenv()
    
    # Set OpenAI API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    openai.api_key = api_key
    
    # Use the model specified in the environment or fallback to default
    model_name = os.getenv("MODEL")
    
    try:
        # Return the configured model instance
        return OpenAIModel(
            model_name=model_name,
            openai_client=openai,
            temperature=0.7,  # Add reasonable defaults
            max_tokens=2000
        )
    except Exception as e:
        raise Exception(f"Failed to initialize OpenAI model: {str(e)}")
