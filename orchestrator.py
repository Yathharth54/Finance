import asyncio
import os
import json
from agent_factory import get_text_model_instance
from agents.data_manager_agent import DataManagerAgent
from agents.budget_agent import BudgetAgent
from agents.tax_policy_agent import TaxPolicyAgent
from agents.report_agent import ReportAgent

async def main():
    # Initialize the shared text model using your agent factory (.env supplies model and API key)
    model = get_text_model_instance()

    # Initialize all agents
    data_manager_agent = DataManagerAgent(model)
    budget_agent = BudgetAgent(model)
    tax_policy_agent = TaxPolicyAgent(model)
    report_agent = ReportAgent(model)

    # Run Data Manager Agent to validate, standardize, and generate visual plots.
    print("Running DataManagerAgent...")
    data_manager_result = await data_manager_agent.run_agent()
    print("DataManagerAgent Output:")
    print(json.dumps(data_manager_result, indent=2))
    
    # Run Budget Agent to generate projections and evaluate risk.
    print("\nRunning BudgetAgent...")
    budget_result = await budget_agent.run_agent()
    print("BudgetAgent Output:")
    print(json.dumps(budget_result, indent=2))
    
    # Run Tax Policy Agent to recommend tax slabs based on standardized data and budget projections.
    print("\nRunning TaxPolicyAgent...")
    # Here we pass the standardized data from Data Manager and projections from Budget Agent.
    tax_policy_result = await tax_policy_agent.run_agent(
        data=data_manager_result["standardized_data"],
        budget_info=budget_result["projections"]
    )
    print("TaxPolicyAgent Output:")
    print(json.dumps(tax_policy_result, indent=2))
    
    # Finally, run the Report Agent to compile all outputs into a final PDF report.
    print("\nRunning ReportAgent...")
    report_path = await report_agent.run_agent(
        data=data_manager_result["standardized_data"],
        budget_info=budget_result["projections"],
        tax_info=tax_policy_result
    )
    print("Final report generated at:", report_path)

if __name__ == "__main__":
    asyncio.run(main())
