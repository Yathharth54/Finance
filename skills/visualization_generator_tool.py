import os
import matplotlib.pyplot as plt

def create_visualizations(budget_results: dict, recommended_slabs: dict) -> list:
    """
    Creates simple charts (e.g., bar charts) to visualize budget results or tax slabs.
    Returns a list of file paths to the generated images.
    """
    viz_paths = []
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Example 1: Budget Pie Chart
    labels = list(budget_results.keys())
    values = [v for k, v in budget_results.items() if isinstance(v, (int, float))]
    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    budget_pie_path = os.path.join(output_folder, "budget_pie_chart.png")
    plt.savefig(budget_pie_path)
    plt.close()
    viz_paths.append(budget_pie_path)

    # Example 2: Slab Rate Bar Chart
    slab_labels = list(recommended_slabs.keys())
    slab_rates = [slab["rate"] for slab in recommended_slabs.values()]
    plt.figure()
    plt.bar(slab_labels, slab_rates)
    plt.title("Proposed Tax Slab Rates")
    slab_chart_path = os.path.join(output_folder, "tax_slab_chart.png")
    plt.savefig(slab_chart_path)
    plt.close()
    viz_paths.append(slab_chart_path)

    return viz_paths
