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
from skills.tax_slab_tool import create_tax_slabs

# Load environment variables from .env file
load_dotenv()

class TA_deps(BaseModel):
    projections: dict

async def main():
    print("1 run")
    TAX_POLICY_SYS_PROMPT = """
    <agent_role>
    You are the Tax Policy Agent for the Ministry of Finance system. Your task is to recommend new tax slabs based on the standardized financial data and budget projections using the TaxSlabTool.
    Your output must be a list object with keys "recommended_slabs" (which holds the recommended tax slabs).
    </agent_role>
    """
    
    TA_model = get_text_model_instance()
    print("2 run")
    
    TA_agent = Agent(
        model=TA_model,
        name="Tax Agent",
        system_prompt=TAX_POLICY_SYS_PROMPT,
        deps_type=TA_deps,
        retries=3,
        model_settings=ModelSettings(
            temperature=0.5,
            max_tokens=2000
        ),
    )
    print("3 run")
    
    prompt = "Create Tax slabs."
    
    @TA_agent.tool_plain
    def slabs_tool(ctx: RunContext[TA_deps]) -> list:
        return create_tax_slabs(projections=ctx.deps) 
    
    print("4 run")
    logfire.configure(send_to_logfire='if-token-present')
    result = await TA_agent.run(user_prompt=prompt)
    print(result.data)

if __name__ == "__main__":  # Fixed syntax here
    asyncio.run(main())
    print("5 run")
