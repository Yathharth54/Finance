import os
import json
import asyncio
from agents.data_manager_agent import DataManagerAgent
from agents.budget_agent import BudgetAgent
from agents.tax_policy_agent import TaxPolicyAgent
from agents.report_agent import ReportAgent
from agent_factory import get_text_model_instance

async def main():
    input_json_path = "input_data.json"
    if not os.path.exists(input_json_path):
        sample_data = {
            "financial_data": {
                "revenues": [100, 120, 140],
                "expenditures": [80, 90, 110],
                "economic_indicators": {
                    "inflation_rate": 0.03,
                    "gdp_growth_rate": 0.04
                }
            },
            "policy_goals": {
                "desired_revenue_increase": 0.1,
                "risk_tolerance": "medium",
                "tax_reform_target": 0.15
            }
        }
        with open(input_json_path, "w") as f:
            json.dump(sample_data, f, indent=2)
        print(f"Sample input_data.json created at {input_json_path}")

    with open(input_json_path, "r") as f:
        input_data = json.load(f)

    # Create a model instance using the agent factory.
    model_instance = get_text_model_instance()

    # Run Data Manager Agent.
    data_manager = DataManagerAgent(model_instance)
    standardized_data = await data_manager.run_agent(input_data)

    # Run Budget Agent.
    budget_agent = BudgetAgent(model_instance)
    budget_info = await budget_agent.run_agent(standardized_data)

    # Run Tax Policy Agent.
    tax_agent = TaxPolicyAgent(model_instance)
    tax_info = await tax_agent.run_agent(standardized_data, budget_info)

    # Run Report Agent.
    report_agent = ReportAgent(model_instance)
    pdf_path = await report_agent.run_agent(standardized_data, budget_info, tax_info)

    print(f"\nProcess completed! Final PDF report generated at: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(main())
