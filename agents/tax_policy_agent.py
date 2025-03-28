from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
import json
from typing import Dict, Any
from dataclasses import dataclass
from agent_factory import get_text_model_instance
# Register the tax slab tool from your skills directory.
from skills.tax_slab_tool import create_tax_slabs

class TaxOutput(BaseModel):
    slabs: Dict[str,Any]

class TaxInput(BaseModel):
    projections: Dict[str, Any]

@dataclass
class TA_deps:
    projections: Dict[str,Any]

TAX_POLICY_SYS_PROMPT = """
<agent_role>
You are the Tax Policy Agent for the Ministry of Finance system. Your task is to recommend new tax slabs based on the standardized financial data and budget projections using the TaxSlabTool.
Your output must be a JSON object with keys "recommended_slabs" (which holds the recommended tax slabs) and "slab_effectiveness" (which analyzes the potential effectiveness of these slabs).
</agent_role>
"""

TA_model = get_text_model_instance()

TA_agent = Agent(
    model=TA_model, 
    name="Data Manager Agent",
    system_prompt=TAX_POLICY_SYS_PROMPT,
    deps_type=TA_deps,
    retries=3,
    model_settings=ModelSettings(
        temperature=0.5,
    ),
)

@TA_agent.tool
def tax_slab_tool(ctx: RunContext[TA_deps], projections: Dict[str, Any]) -> Dict[str,Any]:
    return create_tax_slabs(projections=ctx.deps.projections)