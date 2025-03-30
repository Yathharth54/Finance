import json
from pathlib import Path
from dotenv import load_dotenv
import logging

# Import agents
from agent_factory import get_text_model_instance
from agents.data_manager_agent import DMA_agent, DMA_deps
from agents.budget_agent import BA_agent, BA_deps
from agents.tax_policy_agent import TA_agent, TA_deps
from agents.report_agent import RA_agent, RA_deps

first_step_deps = DMA_deps(json_file_path="input_data.json")

class Orchestrator:
    """
    Orchestrates the execution of multiple agents in sequence to process financial data
    and generate reports. Manages the flow of data between agents and handles errors.
    """
    def __init__(self, input_file_path="input_data.json"):
        """
        Initialize the Orchestrator with input file path and set up agents.

        Args:
            input_file_path (str): Path to the input JSON file (default: "input_data.json").
        """
        load_dotenv()  # Load environment variables for model credentials
        self.logger = logging.getLogger(__name__)

        # Resolve absolute path for input file
        base_dir = Path(__file__).parent
        self.input_file_path = base_dir / input_file_path

        # Load input data
        with open(self.input_file_path, 'r', encoding='utf-8') as f:
            self.input_data = json.load(f)

        # Initialize the model
        self.model = get_text_model_instance()

    def run(self):
        """
        Run the agents in sequence to process data and generate a report.
        Each agent's result is passed as a dependency to the next agent.
        """
        try:
            # First step: Data Manager Agent
            dma_result = DMA_agent.run(deps=first_step_deps, user_prompt="Process the input data")
            self.logger.debug("Data Manager Agent completed successfully")

            # Update second step dependencies with DMA result
            second_step_deps = BA_deps(json_file_path="input_data.json")
            second_step_deps.input_data = dma_result

            # Second step: Budget Agent
            ba_result = BA_agent.run(deps=second_step_deps, user_prompt="Generate budget projections")
            self.logger.debug("Budget Agent completed successfully")

            # Update third step dependencies with BA result
            third_step_deps = TA_deps(projections={})
            third_step_deps.projections = ba_result

            # Third step: Tax Policy Agent
            ta_result = TA_agent.run(deps=third_step_deps, user_prompt="Generate tax policy recommendations")
            self.logger.debug("Tax Policy Agent completed successfully")

            # Update fourth step dependencies with previous results
            fourth_step_deps = RA_deps(projections={}, risk_ranking="", slabs={}, visual_plots_dir="visual plots")
            fourth_step_deps.projections = ba_result
            fourth_step_deps.slabs = ta_result

            # Fourth step: Report Agent
            ra_result = RA_agent.run(deps=fourth_step_deps, user_prompt="Generate final report")
            self.logger.debug("Report Agent completed successfully")

            return dma_result, ba_result, ta_result, ra_result

        except Exception as e:
            if "Data Manager Agent" in str(e):
                self.logger.error("Data Manager Agent failed: %s", str(e))
            elif "Budget Agent" in str(e):
                self.logger.error("Budget Agent failed: %s", str(e))
            elif "Tax Policy Agent" in str(e):
                self.logger.error("Tax Policy Agent failed: %s", str(e))
            elif "Report Agent" in str(e):
                self.logger.error("Report Agent failed: %s", str(e))
            else:
                self.logger.error("Unexpected error: %s", str(e))
            
            raise