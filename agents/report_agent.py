from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json

class ReportOutput(BaseModel):
    report_path: str

REPORT_SYS_PROMPT = """
<agent_role>
You are the Report Agent for the Ministry of Finance system. Your task is to compile the data from previous agents into a final report.
Your available tools are:
- ReportCompilerTool (to compile text sections)
- VisualizationGeneratorTool (to generate charts and graphs)
Your output must be a PDF report saved in the designated output folder, and return a JSON with key "report_path" indicating where the file is saved.
</agent_role>
"""

class ReportAgent:
    def __init__(self, model):
        self.agent = Agent(
            model=model,
            system_prompt=REPORT_SYS_PROMPT,
            name="ReportAgent",
            result_type=ReportOutput,
            retries=2,
            model_settings=ModelSettings(temperature=0.2)
        )
        self.register_tools()

    def register_tools(self):
        from skills.report_compiler_tool import compile_report_content
        from skills.visualization_generator_tool import create_visualizations
        self.agent.tool_plain(compile_report_content)
        self.agent.tool_plain(create_visualizations)

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

    async def run_agent(self, data: dict, budget_info: dict, tax_info: dict) -> str:
        combined_input = {"data": data, "budget_info": budget_info, "tax_info": tax_info}
        plan = self.generate_plan(f"Compile a final report from: {combined_input}")
        print("[ReportAgent] Generated Plan:\n", plan)
        context = RunContext(
            deps={},
            model=self.agent.model,
            usage={},
            prompt=self.agent.system_prompt
        )
        context.input = json.dumps(combined_input)
        result = await self.agent.run(context)
        print("[ReportAgent] Final report generated.")
        return result.report_path
