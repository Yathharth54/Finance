# print("0 run")
# # import os
# # import json
# # import asyncio
# import logfire
# # from typing import Dict, Any
# from dotenv import load_dotenv
# # from dataclasses import dataclass
# from pydantic import BaseModel
# from pydantic_ai import Agent
# from pydantic_ai.settings import ModelSettings
# from agent_factory import get_text_model_instance
# # Import and register the tools used by this agent.
# from skills.data_validation_tool import validate_data
# # from skills.dataset_standardization_tool import standardize_data
# # from skills.visualization_tool import create_visual_plots

# # Load environment variables from .env file
# load_dotenv()

# class DataManagerInput(BaseModel):
#     file_path: str

# def main():
#     print("1 run")
#     DATA_MANAGER_SYS_PROMPT = """
#     <agent_role>
#     You are the Data Manager Agent for the Ministry of Finance system. Your task is to validate the input financial data using the DataValidationTool.
#     </agent_role>
#     """

#     DMA_model = get_text_model_instance()
#     print("2 run")
#     DMA_agent = Agent(
#         model=DMA_model, 
#         name="Data Manager Agent",
#         system_prompt=DATA_MANAGER_SYS_PROMPT,
#         retries=3,
#         model_settings=ModelSettings(
#             temperature=0.5,
#         ),
#     )
#     print("3 run")
#     prompt = "Is the input data valid?"
#     @DMA_agent.tool_plain
#     def validate_data_tool() -> bool:  
#         return validate_data(file_path="input_data.json")  # Use file_path argument
#     print("before run")
#     logfire.configure(send_to_logfire='if-token-present')

#     result = DMA_agent.run_sync(user_prompt= prompt)
#     print(result.data)

# # import asyncio
# # from orchestrator import Orchestrator

# if __name__ == "__main__":
#     # orchestrator = Orchestrator()
#     # orchestrator.run()
#     main()
#     print("4 run")

print("0 run")  # This is the only print statement that runs

# import os
# import json
import asyncio
import logfire
# from typing import Dict, Any
from dotenv import load_dotenv
# from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from agent_factory import get_text_model_instance

# Import and register the tools used by this agent.
from skills.data_validation_tool import validate_data
# from skills.dataset_standardization_tool import standardize_data
# from skills.visualization_tool import create_visual_plots

# Load environment variables from .env file
load_dotenv()

class DataManagerInput(BaseModel):
    file_path: str

async def main():
    print("1 run")
    DATA_MANAGER_SYS_PROMPT = """ <agent_role> You are the Data Manager Agent for the Ministry of Finance system. Your task is to validate the input financial data using the DataValidationTool. </agent_role> """
    
    DMA_model = get_text_model_instance()
    print("2 run")
    
    DMA_agent = Agent(
        model=DMA_model,
        name="Data Manager Agent",
        system_prompt=DATA_MANAGER_SYS_PROMPT,
        retries=3,
        model_settings=ModelSettings(
            temperature=0.5,
            max_tokens=2000
        ),
    )
    print("3 run")
    
    prompt = "Is the input data valid?"
    
    @DMA_agent.tool_plain
    def validate_data_tool() -> bool:
        return validate_data(file_path="input_data.json") # Use file_path argument
    
    print("4 run")
    logfire.configure(send_to_logfire='if-token-present')
    result = await DMA_agent.run(user_prompt=prompt)
    print(result.data)

# import asyncio
# from orchestrator import Orchestrator

if __name__ == "__main__":  # Fixed syntax here
    # orchestrator = Orchestrator()
    # orchestrator.run()
    asyncio.run(main())
    print("5 run")
