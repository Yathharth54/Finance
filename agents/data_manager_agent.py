from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json

class DataManagerOutput(BaseModel):
    standardized_data: dict

DATA_MANAGER_SYS_PROMPT = """
<agent_role>
You are the Data Manager Agent for the Ministry of Finance system. Your task is to validate the input financial data using the DataValidationTool and then standardize it using the DatasetStandardizationTool.
Your output must be a JSON object with the key "standardized_data" that holds the processed data.
</agent_role>
"""

class DataManagerAgent:
    def __init__(self, model):
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
        from skills.data_validation_tool import validate_input_structure
        from skills.dataset_standardization_tool import standardize_dataset
        self.agent.tool_plain(validate_input_structure)
        self.agent.tool_plain(standardize_dataset)

    def generate_plan(self, user_input: str) -> str:
        prompt = f"{self.agent.system_prompt}\nUser Input: {user_input}\nPlan:"
        response = self.agent.model.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": self.agent.system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    async def run_agent(self, input_data: dict) -> dict:
        user_input = f"Process the following input data: {input_data}"
        plan = self.generate_plan(user_input)
        print("[DataManagerAgent] Generated Plan:\n", plan)
        context = RunContext(
            deps={},
            model=self.agent.model,
            usage={},
            prompt=self.agent.system_prompt
        )
        context.input = json.dumps(input_data)
        result = await self.agent.run(context)
        print("[DataManagerAgent] Final standardized data obtained.")
        return result.standardized_data
