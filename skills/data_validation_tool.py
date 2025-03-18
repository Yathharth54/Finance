def validate_input_structure(input_data: dict) -> tuple[bool, str]:
    """
    Checks if the input JSON has the required fields, no missing data, etc.
    Returns (True, "") if valid, or (False, "error message") if not.
    """
    if "financial_data" not in input_data:
        return False, "Missing 'financial_data' section."
    if "policy_goals" not in input_data:
        return False, "Missing 'policy_goals' section."

    # More rigorous checks as needed...
    return True, ""
