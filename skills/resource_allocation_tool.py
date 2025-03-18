def suggest_resource_allocation(budget_results: dict, risk_analysis: dict) -> dict:
    """
    Suggests how to allocate resources among key sectors based on budget constraints and risk.
    """
    total_budget = budget_results["projected_revenue"]
    risk_level = risk_analysis["risk_level"]

    # Very naive approach: shift resources if risk is high
    if risk_level == "high":
        health = total_budget * 0.3
        education = total_budget * 0.25
        defense = total_budget * 0.15
    else:
        health = total_budget * 0.25
        education = total_budget * 0.3
        defense = total_budget * 0.2

    return {
        "Health": health,
        "Education": education,
        "Defense": defense,
        "Unallocated": total_budget - (health + education + defense)
    }
