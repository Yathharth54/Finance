def compile_report_content(standardized_data: dict,
                           budget_results: dict,
                           risk_analysis: dict,
                           allocation_plan: dict,
                           recommended_slabs: dict,
                           slab_effectiveness: dict) -> str:
    """
    Aggregates text from all steps into a coherent final report text.
    """
    text_sections = []

    text_sections.append("EXECUTIVE SUMMARY:\n")
    text_sections.append(f"Based on the input data, the projected revenue is {budget_results['projected_revenue']:.2f}.")

    text_sections.append("\nBUDGET ANALYSIS:\n")
    text_sections.append(f"Risk Level: {risk_analysis['risk_level']} - {risk_analysis['notes']}")
    text_sections.append(f"Resource Allocation Plan: {allocation_plan}")

    text_sections.append("\nTAX POLICY RECOMMENDATIONS:\n")
    text_sections.append(f"Recommended Slabs: {recommended_slabs}")
    text_sections.append(f"Slab Effectiveness: {slab_effectiveness}")

    return "\n\n".join(text_sections)
