from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json
from typing import Dict, Any
from dataclasses import dataclass
from agent_factory import get_text_model_instance
from skills.report_compiler_tool import compile_report

class ReportOutput(BaseModel):
    output_pdf: str

class ReportInput(BaseModel):
    projections: Dict[str,Any]
    risk_ranking: str
    slabs: Dict[str,Any] 
    visual_plots_dir: str

@dataclass
class RA_deps:
    projections: Dict[str,Any]
    risk_ranking: str
    slabs: Dict[str,Any]
    visual_plots_dir: str

REPORT_SYS_PROMPT = """
<agent_role>
You are the Report Agent for the Ministry of Finance system. Your task is to compile the data from previous agents into a final report.
Your available tool is:
- ReportCompilerTool (which compiles text sections from budget projections, risk analysis, tax policy recommendations, and visual plots into one PDF report)
Your output must be a PDF report saved in the designated output folder, and return a JSON object with key "report_path" indicating where the file is saved.
</agent_role>
"""

RA_model = get_text_model_instance()

RA_agent = Agent(
    model=RA_model, 
    name="Data Manager Agent",
    system_prompt=REPORT_SYS_PROMPT,
    deps_type=RA_deps,
    retries=3,
    model_settings=ModelSettings(
        temperature=0.5,
    ),
)

@RA_agent.tool
def compile_report_tool(ctx: RunContext[RA_deps]):
    return compile_report(projections=ctx.deps.projections, risk_level=ctx.deps.risk_level, tax_slabs=ctx.deps.tax_slabs, visual_plots_dir=ctx.deps.visual_plots_dir)