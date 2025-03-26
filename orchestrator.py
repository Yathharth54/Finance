import asyncio
import os
import json
from dotenv import load_dotenv
from pathlib import Path
import logging

# Import agents
from agent_factory import get_text_model_instance
from agents.data_manager_agent import DataManagerAgent
from agents.budget_agent import BudgetAgent
from agents.tax_policy_agent import TaxPolicyAgent
from agents.report_agent import ReportAgent

# Import skills
from skills.dataset_standardization_tool import standardize_data
from skills.data_validation_tool import validate_data
from skills.visualization_tool import create_visual_plots
from skills.budget_projection_tool import project_budget
from skills.risk_identification_tool import risk_identification
from skills.tax_slab_tool import create_tax_slabs
from skills.report_compiler_tool import compile_report

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def main():
    logger.debug("Starting main execution")
    load_dotenv()
    
    # Get the absolute path to the input file
    base_dir = Path(__file__).parent
    input_file_path = base_dir / 'input_data.json'
    
    try:
        with open(input_file_path, 'r') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Error: input_data.json file not found at {input_file_path}")
        return
    except json.JSONDecodeError:
        logger.error("Error: Invalid JSON format in input_data.json.")
        return
    
    try:
        model = get_text_model_instance()
        logger.debug("Successfully initialized model")
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        return

    # Initialize all tools first
    try:
        dataset_tool = DatasetStandardizationTool()
        validation_tool = DataValidationTool()
        visualization_tool = VisualizationTool()
        budget_tool = BudgetProjectionTool()
        risk_tool = RiskIdentificationTool()
        tax_tool = TaxSlabTool()
        report_tool = ReportCompilerTool()
        logger.debug("Successfully initialized all tools")
    except Exception as e:
        logger.error(f"Failed to initialize tools: {str(e)}")
        return

    # Initialize agents with their required tools
    try:
        data_manager_agent = DataManagerAgent(
            model=model,
            standardization_tool=dataset_tool,
            validation_tool=validation_tool,
            visualization_tool=visualization_tool
        )

        budget_agent = BudgetAgent(
            model=model,
            projection_tool=budget_tool,
            risk_tool=risk_tool
        )

        tax_policy_agent = TaxPolicyAgent(
            model=model,
            tax_tool=tax_tool
        )

        report_agent = ReportAgent(
            model=model,
            report_tool=report_tool
        )
        
        logger.debug("Successfully initialized all agents")
    except Exception as e:
        logger.error(f"Failed to initialize agents: {str(e)}")
        return

    # Execute agent pipeline
    try:
        # Run Data Manager Agent
        logger.debug("Running DataManagerAgent...")
        data_manager_result = await data_manager_agent.run_agent(data=input_data)
        logger.debug("DataManagerAgent completed successfully")

        # Run Budget Agent
        logger.debug("Running BudgetAgent...")
        budget_result = await budget_agent.run_agent(data=input_data)
        logger.debug("BudgetAgent completed successfully")

        # Run Tax Policy Agent
        logger.debug("Running TaxPolicyAgent...")
        tax_policy_result = await tax_policy_agent.run_agent(
            data=data_manager_result["standardized_data"],
            budget_info=budget_result["projections"]
        )
        logger.debug("TaxPolicyAgent completed successfully")

        # Run Report Agent
        logger.debug("Running ReportAgent...")
        report_path = await report_agent.run_agent(
            data=data_manager_result["standardized_data"],
            budget_info=budget_result["projections"],
            tax_info=tax_policy_result
        )
        logger.info(f"Final report generated at: {report_path}")

    except Exception as e:
        logger.error(f"Error during agent execution: {str(e)}")
        return

if __name__ == "__main__":
    asyncio.run(main())
