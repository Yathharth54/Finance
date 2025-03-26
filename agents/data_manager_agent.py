import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings

# Import and register the tools used by this agent.
from skills.data_validation_tool import validate_data
from skills.dataset_standardization_tool import standardize_data
from skills.visualization_tool import create_visual_plots

# Load environment variables from .env file
load_dotenv()

class DataManagerOutput(BaseModel):
    standardized_data: dict
    visual_plots: list  # List of filenames or identifiers for the generated visual plots

DATA_MANAGER_SYS_PROMPT = """
<agent_role>
You are the Data Manager Agent for the Ministry of Finance system. Your task is to validate the input financial data using the DataValidationTool, then standardize it using the DatasetStandardizationTool, and finally generate visual plots using the VisualisationTool.
Your output must be a JSON object with two keys: "standardized_data" that holds the processed data and "visual_plots" that holds a list of the generated visual plot filenames.
</agent_role>
"""

class DataManagerAgent:
    def __init__(self, model, standardization_tool, validation_tool, visualization_tool):
        self.model = model
        self.standardization_tool = standardization_tool
        self.validation_tool = validation_tool
        self.visualization_tool = visualization_tool
        self.agent = Agent(
            model=model,
            system_prompt=DATA_MANAGER_SYS_PROMPT,
            name="DataManagerAgent",
            result_type=DataManagerOutput,
            retries=2,
            model_settings=ModelSettings(temperature=0.2)
        )
        self.register_tools()

    def register_tools(self):
        self.agent.tool_plain(validate_data)
        self.agent.tool_plain(standardize_data)
        self.agent.tool_plain(create_visual_plots)

    def generate_plan(self, user_input: str) -> str:
        prompt = f"{self.agent.system_prompt}\nUser Input: {user_input}\nPlan:"
        response = self.agent.model.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-2024-08-06"),
            messages=[
                {"role": "system", "content": self.agent.system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    async def run_agent(self, data):
        # Implementation here
        pass