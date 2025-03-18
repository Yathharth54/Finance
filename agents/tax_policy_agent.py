from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json

class TaxPolicyOutput(BaseModel):
    recommended_slabs: dict
    slab_effectiveness: dict

TAX_POLICY_SYS_PROMPT = """
<agent_role>
You are the Tax Policy Agent for the Ministry of Finance system. Your task is to recommend new tax slabs based on revenue targets and economic conditions, and analyze the effectiveness of current tax policies.
Your available tools are:
- TaxSlabRecommender
- TaxSlabEffectivenessAnalyzer
Output a JSON with keys "recommended_slabs" and "slab_effectiveness".
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
        from skills.tax_slab_recommender import recommend_slabs
        from skills.tax_slab_effectiveness_analyzer import analyze_slabs
        self.agent.tool_plain(recommend_slabs)
        self.agent.tool_plain(analyze_slabs)

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
        combined_input = {"data": data, "budget_info": budget_info}
        plan = self.generate_plan(f"Based on the standardized data and budget info: {combined_input}, recommend tax slabs and analyze their effectiveness.")
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
            "recommended_slabs": result.recommended_slabs,
            "slab_effectiveness": result.slab_effectiveness
        }
