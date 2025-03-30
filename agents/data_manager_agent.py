# import os
# import json
# from typing import Dict, Any
# from dotenv import load_dotenv
# from dataclasses import dataclass
# from pydantic import BaseModel
# from pydantic_ai import Agent, RunContext
# from pydantic_ai.settings import ModelSettings
# from agent_factory import get_text_model_instance
# # Import and register the tools used by this agent.
# from skills.data_validation_tool import validate_data
# from skills.dataset_standardization_tool import standardize_data
# from skills.visualization_tool import create_visual_plots

# # Load environment variables from .env file
# load_dotenv()

# class DataManagerInput(BaseModel):
#     financial_data: Dict[str, Any]

# class DataManagerOutput(BaseModel):
#     standardized_data: Dict[str, Any]
#     visual_plots: list  # List of filenames or identifiers for the generated visual plots

# @dataclass
# class DMA_deps:
#     json_file_path: str

# DATA_MANAGER_SYS_PROMPT = """
# <agent_role>
# You are the Data Manager Agent for the Ministry of Finance system. Your task is to validate the input financial data using the DataValidationTool, then standardize it using the DatasetStandardizationTool, and finally generate visual plots using the VisualisationTool.
# Your output must be a JSON object with two keys: "standardized_data" that holds the processed data and "visual_plots" that holds a list of the generated visual plot filenames.
# </agent_role>
# """

# DMA_model = get_text_model_instance()

# DMA_agent = Agent(
#     model=DMA_model, 
#     name="Data Manager Agent",
#     system_prompt=DATA_MANAGER_SYS_PROMPT,
#     deps_type=DMA_deps,
#     retries=3,
#     model_settings=ModelSettings(
#         temperature=0.5,
#     ),
# )

# @DMA_agent.tool
# def validate_data_tool(ctx: RunContext[DMA_deps], input_data: json) -> json:
#     return validate_data(file_path=ctx.deps.json_file_path)

# @DMA_agent.tool
# def standardize_data_tool(ctx: RunContext[DMA_deps], input_data: json) -> json:
#     return standardize_data(file_path=ctx.deps.json_file_path)

# @DMA_agent.tool
# def create_visual_plots_tool(ctx: RunContext[DMA_deps], input_data: dict) -> json:
#     return create_visual_plots(data=ctx.deps.json_file_path)

