import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings

# Import and register the tools used by this agent
from skills.budget_projection_tool import project_budget
from skills.risk_identification_tool import risk_identification

# Load environment variables from .env file
load_dotenv()

class BudgetOutput(BaseModel):
    projections: dict
    risk_ranking: str

BUDGET_AGENT_SYS_PROMPT = """
<agent_role>
You are the Budget Agent for the Ministry of Finance system. Your task is to generate budget projections using the BudgetProjectionTool and then evaluate the financial risk using the RiskIdentificationTool.
Your output must be a JSON object with two keys: "projections" that holds the projected financial data and "risk_ranking" that holds the risk level (e.g., "low", "medium", "high").
</agent_role>
"""

class BudgetAgent:
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=BUDGET_AGENT_SYS_PROMPT,
            name="BudgetAgent",
            result_type=BudgetOutput,
            retries=2,
            model_settings=ModelSettings(temperature=0.2)
        )
        self.register_tools()

    def register_tools(self):
        self.agent.tool_plain(project_budget)
        self.agent.tool_plain(risk_identification)

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

    async def run_agent(self, input_data: dict = None) -> dict:
        # If no input data is provided, load input_data.json from the outer directory.
        if input_data is None:
            input_file = "input_data.json"
            if os.path.isfile(input_file):
                with open(input_file, 'r') as f:
                    input_data = json.load(f)
                print(f"[BudgetAgent] Loaded input data from {input_file}.")
            else:
                raise FileNotFoundError(f"{input_file} not found in the directory.")

        user_input = f"Process the following input data to generate budget projections and risk ranking: {input_data}"
        plan = self.generate_plan(user_input)
        print("[BudgetAgent] Generated Plan:\n", plan)
        context = RunContext(
            deps={},
            model=self.agent.model,
            usage={},
            prompt=self.agent.system_prompt
        )
        context.input = json.dumps(input_data)
        result = await self.agent.run(context)
        print("[BudgetAgent] Final budget projections and risk ranking obtained.")
        return {
            "projections": result.projections,
            "risk_ranking": result.risk_ranking
        }