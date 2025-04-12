print("0 run")  # This is the only print statement that runs

# import os
# import json
import asyncio
import logfire
# from typing import Dict, Any
from dotenv import load_dotenv
# from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from agent_factory import get_text_model_instance

# Import and register the tools used by this agent.
from skills.budget_projection_tool import project_budget
from skills.risk_identification_tool import risk_identification

# Load environment variables from .env file
load_dotenv()

class BudgetInput(BaseModel):
    file_path: str

class BA_deps(BaseModel):
    projections: dict

async def main():
    print("1 run")
    BUDGET_AGENT_SYS_PROMPT = """
    <agent_role>
    1.You are the Budget Agent for the Ministry of Finance system. Your task is to generate budget projections using the BudgetProjectionTool and then evaluate the financial risk using the RiskIdentificationTool.
    2.BudgetProjectionTool will take input the input_data.json file and generate projected financial data.
    3.RiskIdentificationTool will take the projected financial data from BudgetProjectionTool output and evaluate the overall risk ranking.
    4.Your output must be a JSON object with two keys: "projections" that holds the projected financial data and "risk_ranking" that holds the risk level (e.g., "low", "medium", "high").
    </agent_role>
    """
    
    BA_model = get_text_model_instance()
    print("2 run")
    
    BA_agent = Agent(
        model=BA_model,
        name="Budget Agent",
        system_prompt=BUDGET_AGENT_SYS_PROMPT,
        deps_type=BA_deps,
        retries=3,
        model_settings=ModelSettings(
            temperature=0.5,
            max_tokens=2000
        ),
    )
    print("3 run")
    
    prompt = "Create budget projections and evaluate financial risk."
    
    @BA_agent.tool_plain
    def project_tool() -> dict:
        return project_budget(file_path="input_data.json") # Use file_path argument

    @BA_agent.tool_plain
    def risk_tool(ctx: RunContext[BA_deps]) -> str:
        return risk_identification(projections=ctx.deps)
    
    print("4 run")
    logfire.configure(send_to_logfire='if-token-present')
    result = await BA_agent.run(user_prompt=prompt)
    print(result.data)

if __name__ == "__main__":  # Fixed syntax here
    asyncio.run(main())
    print("5 run")
