import os
import openai
from pydantic_ai.models.openai import OpenAIModel

def get_text_model_instance():
    # Directly use the openai module as the client
    return OpenAIModel(model_name="gpt-4o-2024-08-06", openai_client=openai)
