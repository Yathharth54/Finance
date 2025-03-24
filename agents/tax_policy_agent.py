from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json

# Register the tax slab tool from your skills directory.
from skills.tax_slab_tool import create_tax_slabs

class TaxPolicyOutput(BaseModel):
    recommended_slabs: dict

TAX_POLICY_SYS_PROMPT = """
<agent_role>
You are the Tax Policy Agent for the Ministry of Finance system. Your task is to recommend new tax slabs based on the standardized financial data and budget projections using the TaxSlabTool.
Your output must be a JSON object with keys "recommended_slabs" (which holds the recommended tax slabs) and "slab_effectiveness" (which analyzes the potential effectiveness of these slabs).
</agent_role>
"""

class TaxPolicyAgent:
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=TAX_POLICY_SYS_PROMPT,
            name="TaxPolicyAgent",
            result_type=TaxPolicyOutput,
            retries=2,
            model_settings=ModelSettings(temperature=0.2)
        )
        self.register_tools()

    def register_tools(self):
        self.agent.tool_plain(create_tax_slabs)

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

    async def run_agent(self, data: dict, budget_info: dict) -> dict:
        # Combine standardized data and budget projections as input.
        combined_input = {"data": data, "budget_info": budget_info}
        user_input = f"Based on the following input {combined_input}, recommend new tax slabs using the TaxSlabTool and provide an analysis of their effectiveness."
        plan = self.generate_plan(user_input)
        print("[TaxPolicyAgent] Generated Plan:\n", plan)
        context = RunContext(
            deps={},
            model=self.agent.model,
            usage={},
            prompt=self.agent.system_prompt
        )
        context.input = json.dumps(combined_input)
        result = await self.agent.run(context)
        print("[TaxPolicyAgent] Tax policy recommendations complete.")
        return {
            "recommended_slabs": result.recommended_slabs
        }