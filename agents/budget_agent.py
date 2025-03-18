from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json

class BudgetAgentOutput(BaseModel):
    projected_budget: dict
    risk_analysis: dict
    resource_allocation: dict

BUDGET_AGENT_SYS_PROMPT = """
<agent_role>
You are the Budget Agent for the Ministry of Finance system. Your task is to generate budget projections using historical data and economic indicators, identify risks, and suggest optimal resource allocation.
Your available tools are:
- BudgetProjectionTool
- RiskIdentificationTool
- ResourceAllocationTool
Output a JSON with keys "projected_budget", "risk_analysis", and "resource_allocation".
</agent_role>
"""

class BudgetAgent:
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=BUDGET_AGENT_SYS_PROMPT,
            name="BudgetAgent",
            result_type=BudgetAgentOutput,
            retries=2,
            model_settings=ModelSettings(temperature=0.2)
        )
        self.register_tools()

    def register_tools(self):
        from skills.budget_projection_tool import generate_budget_forecast
        from skills.risk_identification_tool import identify_budget_risks
        from skills.resource_allocation_tool import suggest_resource_allocation

        # Register tools with the agent (using the framework’s decorator pattern)
        self.agent.tool_plain(generate_budget_forecast)
        self.agent.tool_plain(identify_budget_risks)
        self.agent.tool_plain(suggest_resource_allocation)

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

    async def run_agent(self, data: dict) -> dict:
        plan = self.generate_plan(f"Use the standardized data: {data} to project budget and analyze risks.")
        print("[BudgetAgent] Generated Plan:\n", plan)
        context = RunContext(
            deps={},
            model=self.agent.model,
            usage={},
            prompt=self.agent.system_prompt
        )
        context.input = json.dumps(data)
        result = await self.agent.run(context)
        print("[BudgetAgent] Budget projection and risk analysis complete.")
        return {
            "projected_budget": result.projected_budget,
            "risk_analysis": result.risk_analysis,
            "resource_allocation": result.resource_allocation
        }