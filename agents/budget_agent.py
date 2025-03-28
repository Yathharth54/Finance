import os
import json
from dotenv import load_dotenv
from typing import Dict, Any
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from agent_factory import get_text_model_instance
# Import and register the tools used by this agent
from skills.budget_projection_tool import project_budget
from skills.risk_identification_tool import risk_identification

# Load environment variables from .env file
load_dotenv()

class BudgetOutput(BaseModel):
    projections: Dict[str, Any]
    risk_ranking: str

class BudgetInput(BaseModel):
    financial_data: Dict[str, Any]

@dataclass
class BA_deps:
    json_file_path: str

BUDGET_AGENT_SYS_PROMPT = """
<agent_role>
1.You are the Budget Agent for the Ministry of Finance system. Your task is to generate budget projections using the BudgetProjectionTool and then evaluate the financial risk using the RiskIdentificationTool.
2.BudgetProjectionTool will take input the input_data.json file and generate projected financial data.
3.RiskIdentificationTool will take the projected financial data from BudgetProjectionTool output and evaluate the overall risk ranking.
4.Your output must be a JSON object with two keys: "projections" that holds the projected financial data and "risk_ranking" that holds the risk level (e.g., "low", "medium", "high").
</agent_role>
"""

BA_model = get_text_model_instance()

BA_agent = Agent(
    model=BA_model, 
    name="Data Manager Agent",
    system_prompt=BUDGET_AGENT_SYS_PROMPT,
    deps_type=BA_deps,
    retries=3,
    model_settings=ModelSettings(
        temperature=0.5,
    ),
)

@BA_agent.tool
def project_budget_tool(ctx: RunContext[BA_deps], input_data: json) -> json:
    return project_budget(file_path=ctx.deps.json_file_path)

@BA_agent.tool_plain
def risk_identification_tool(projections: json) -> json:
    return risk_identification()
