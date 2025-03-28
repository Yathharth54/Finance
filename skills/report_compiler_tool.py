from fpdf import FPDF
import os

def add_header(pdf):
    """Helper function to add a header to the current page."""
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Budget Analysis Report', border=0, ln=1, align='C')
    pdf.ln(5)

def add_footer(pdf):
    """Helper function to add a footer with the page number to the current page."""
    pdf.set_y(-15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f'Page {pdf.page_no()}', 0, 0, 'C')

def compile_report(projections: dict, risk_level: str, tax_slabs: list, visual_plots_dir: str = "visual plots", output_pdf: str = "report.pdf"):
    """
    Compiles a final report in PDF format that includes:
      - Budget Projections: Listing revenue, expenditure, inflation, and GDP growth projections.
      - Risk Identification: Overall risk ranking.
      - Tax Slabs: Details of tax slabs computed.
      - Visual Plots: All images from the 'visual plots' directory.
      
    Each section starts on a new page with a header and footer. The resulting PDF is saved as output_pdf.
    """
    # Create an instance of FPDF
    pdf = FPDF()

    # Section 1: Budget Projections
    pdf.add_page()
    add_header(pdf)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Budget Projections", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Projected Revenues:", ln=1)
    for rev in projections.get("projected_revenue", []):
        name = rev.get("name", "Unknown")
        amount = rev.get("projected_amount", 0)
        pdf.cell(0, 10, f"{name}: {amount}", ln=1)
    pdf.ln(5)
    pdf.cell(0, 10, "Projected Expenditures:", ln=1)
    for exp in projections.get("projected_expenditure", []):
        name = exp.get("name", "Unknown")
        amount = exp.get("projected_amount", 0)
        pdf.cell(0, 10, f"{name}: {amount}", ln=1)
    pdf.ln(5)
    projected_inflation = projections.get("projected_inflation", {})
    pdf.cell(0, 10, f"Projected Inflation for {projected_inflation.get('year', 'N/A')}: {projected_inflation.get('rate', 'N/A')}", ln=1)
    projected_gdp = projections.get("projected_gdp_growth", {})
    pdf.cell(0, 10, f"Projected GDP Growth for {projected_gdp.get('year', 'N/A')}: {projected_gdp.get('rate', 'N/A')}", ln=1)
    add_footer(pdf)

    # Section 2: Risk Identification
    pdf.add_page()
    add_header(pdf)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Risk Identification", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Overall Risk Ranking: {risk_level.upper()}", ln=1)
    add_footer(pdf)

    # Section 3: Tax Slabs
    pdf.add_page()
    add_header(pdf)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Tax Slabs", ln=1)
    pdf.set_font("Arial", size=12)
    for slab in tax_slabs:
        pdf.cell(0, 10, f"Slab {slab['slab']}: Range: {slab['range']}, Tax Rate: {slab['tax_rate']}", ln=1)
    add_footer(pdf)

    # Section 4: Visual Plots
    if os.path.exists(visual_plots_dir):
        for image_file in os.listdir(visual_plots_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(visual_plots_dir, image_file)
                pdf.add_page()
                add_header(pdf)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Plot: {image_file}", ln=1)
                pdf.image(image_path, w=pdf.w - 40)  # Resize image to fit page width
                add_footer(pdf)
    else:
        pdf.add_page()
        add_header(pdf)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "No visual plots found.", ln=1)
        add_footer(pdf)

    # Save the PDF
    pdf.output(output_pdf)
    print(f"Report compiled and saved as {output_pdf}")

# Example usage (you can remove this if not needed)
if __name__ == "__main__":
    sample_projections = {
        "projected_revenue": [{"name": "Sales", "projected_amount": 100000}],
        "projected_expenditure": [{"name": "R&D", "projected_amount": 50000}],
        "projected_inflation": {"year": "2024", "rate": "2.5%"},
        "projected_gdp_growth": {"year": "2024", "rate": "3.0%"}
    }
    sample_risk_level = "medium"
    sample_tax_slabs = [{"slab": 1, "range": "0-50000", "tax_rate": "10%"}]
    compile_report(sample_projections, sample_risk_level, sample_tax_slabs)