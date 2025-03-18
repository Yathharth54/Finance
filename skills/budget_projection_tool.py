import math
import openai
import os

# Set your OpenAI API key from environment or config
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

def generate_budget_forecast(data: dict) -> dict:
    """
    Uses historical patterns, growth rates, and LLM to produce a future budget projection.
    """
    revenues = data["financial_data"]["revenues"]
    expenditures = data["financial_data"]["expenditures"]
    inflation_rate = data["financial_data"]["economic_indicators"]["inflation_rate"]
    gdp_growth = data["financial_data"]["economic_indicators"]["gdp_growth_rate"]

    # Basic arithmetic projection
    last_revenue = revenues[-1] if revenues else 0
    last_expenditure = expenditures[-1] if expenditures else 0

    # Let's do a simple next-year estimate
    projected_revenue = last_revenue * (1 + gdp_growth + inflation_rate)
    projected_expenditure = last_expenditure * (1 + inflation_rate)

    # Optionally use LLM to refine or generate textual analysis
    # (We keep it minimal here, but you can expand it)
    prompt = f"""You are a finance expert. 
    We have last year's revenue = {last_revenue} and expenditure = {last_expenditure}.
    The inflation rate is {inflation_rate}, GDP growth is {gdp_growth}.
    Suggest an approximate revenue and expenditure for next year."""
    
    llm_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert financial forecaster."},
                  {"role": "user", "content": prompt}]
    )

    text_analysis = llm_response["choices"][0]["message"]["content"]

    return {
        "projected_revenue": projected_revenue,
        "projected_expenditure": projected_expenditure,
        "analysis_summary": text_analysis
    }
