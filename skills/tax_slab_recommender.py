import math

def recommend_slabs(data: dict, budget_results: dict) -> dict:
    """
    Recommends new tax slabs based on target revenue increase and policy constraints.
    """
    desired_increase = data["policy_goals"]["desired_revenue_increase"]
    base_revenue = budget_results["projected_revenue"]
    # Just a simplistic logic: create slabs around base revenue
    slab1_rate = 0.05 + desired_increase / 2
    slab2_rate = 0.10 + desired_increase / 3
    slab3_rate = 0.15 + desired_increase / 4

    return {
        "Slab1": {"rate": slab1_rate, "range": "0 - 50k"},
        "Slab2": {"rate": slab2_rate, "range": "50k - 200k"},
        "Slab3": {"rate": slab3_rate, "range": "200k+"}
    }
