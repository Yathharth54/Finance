import json
import os

def validate_data(file_path: str) -> bool:
    """
    Loads the JSON file at file_path and validates its structure:
      - 'revenue' (list of items with 'name', 'amount')
      - 'expenditure' (list of items with 'name', 'amount')
      - 'inflation' (list of items with 'year', 'rate')
      - 'gdp_growth' (list of items with 'year', 'rate')

    Prints out the reason for any validation failure.
    Returns True if the JSON is valid, False otherwise.
    """
    # 1. Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        return False

    # 2. Load the JSON data
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {file_path}")
        return False

    # 3. Define the expected structure
    required_keys = {
        "revenue": ["name", "amount"],
        "expenditure": ["name", "amount"],
        "inflation": ["year", "rate"],
        "gdp_growth": ["year", "rate"]
    }

    # 4. Validate each required key and its structure
    for key, required_fields in required_keys.items():
        if key not in data:
            print(f"Error: Missing required field: '{key}'")
            return False

        if not isinstance(data[key], list):
            print(f"Error: The field '{key}' should be a list.")
            return False

        for index, item in enumerate(data[key]):
            if not isinstance(item, dict):
                print(f"Error: Item {index} in '{key}' is not a JSON object.")
                return False

            for field in required_fields:
                if field not in item:
                    print(f"Error: Missing field '{field}' in item {index} of '{key}'.")
                    return False
                
                # Optional type checks
                if field == "amount" and not isinstance(item[field], (int, float)):
                    print(f"Error: Field 'amount' in item {index} of '{key}' must be numeric.")
                    return False
                if field == "rate" and not isinstance(item[field], (int, float)):
                    print(f"Error: Field 'rate' in item {index} of '{key}' must be numeric.")
                    return False
                if field == "year" and not isinstance(item[field], str):
                    print(f"Error: Field 'year' in item {index} of '{key}' must be a string.")
                    return False
                # If needed, you can add type check for 'name'
                # if field == "name" and not isinstance(item[field], str):
                #     print(f"Error: Field 'name' in item {index} of '{key}' must be a string.")
                #     return False

    # All validations passed
    print("Validation succeeded! The input JSON structure is correct.")
    return True