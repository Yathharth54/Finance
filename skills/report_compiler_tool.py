from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        # Logo or header styling
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102)  # Dark blue
        self.cell(0, 10, 'Budget Analysis Report', border=0, ln=1, align='C')
        self.line(10, 20, self.w - 10, 20)  # Add a line under header
        self.ln(10)
    
    def footer(self):
        # Page number styling
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def compile_report(projections: dict, risk_level: str, tax_slabs: list, visual_plots_dir: str = "visual plots", 
                  output_pdf: str = "report.pdf", insights: dict = None):
    """
    Compile all data into a final PDF report with insights
    
    Args:
        projections: Dictionary containing budget projections data
        risk_level: Overall risk assessment level
        tax_slabs: List of tax brackets and rates
        visual_plots_dir: Directory containing visualization plots
        output_pdf: Output PDF filename
        insights: Dictionary containing insight paragraphs for each section
            Expected format: {
                "revenue": "Insight text about revenue...",
                "expenditure": "Insight text about expenditure...",
                "economic": "Insight text about inflation and GDP...",
                "risk": "Insight text about risk assessment...",
                "tax": "Insight text about tax policy...",
                "visual": {
                    "plot_name": "Insight text for specific visual..."
                }
            }
    """
    # Default insights if none provided
    if insights is None:
        insights = {
            "revenue": "Revenue analysis shows a balanced distribution across tax and non-tax sources, with particular strength in corporate and personal income taxes.",
            "expenditure": "The expenditure allocation prioritizes education, healthcare, and debt servicing, representing a balanced approach to public spending.",
            "economic": "The projected inflation rate slightly exceeds GDP growth, suggesting careful monitoring of fiscal policies will be needed in the coming year.",
            "risk": "The medium risk assessment indicates potential challenges that require proactive management strategies.",
            "tax": "The progressive tax structure aims to balance revenue generation with equitable distribution of tax burden across income levels.",
            "visual": {}
        }
    
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Section 1: Budget Projections
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Budget Projections", ln=1)
    pdf.ln(5)
    
    # Revenue Table
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, "Projected Revenues", ln=1)
    pdf.set_font("Arial", size=11)
    with pdf.table() as table:
        for rev in projections.get("projected_revenue", []):
            row = table.row()
            row.cell(rev.get("name", "Unknown"))
            row.cell(f"${rev.get('projected_amount', 0):,.2f}")
    
    # Revenue Insights
    if "revenue" in insights:
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, insights["revenue"])
    
    # Expenditure Table
    pdf.ln(8)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, "Projected Expenditures", ln=1)
    pdf.set_font("Arial", size=11)
    with pdf.table() as table:
        for exp in projections.get("projected_expenditure", []):
            row = table.row()
            row.cell(exp.get("name", "Unknown"))
            row.cell(f"${exp.get('projected_amount', 0):,.2f}")
    
    # Expenditure Insights
    if "expenditure" in insights:
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, insights["expenditure"])
    
    # Inflation & GDP
    pdf.ln(8)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, "Economic Indicators", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, f"Projected Inflation (2026): {projections.get('projected_inflation', {}).get('rate', 'N/A')}%", ln=1)
    pdf.cell(0, 6, f"Projected GDP Growth (2026): {projections.get('projected_gdp_growth', {}).get('rate', 'N/A')}%", ln=1)
    
    # Economic Indicators Insights
    if "economic" in insights:
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, insights["economic"])
    
    # Section 2: Risk Identification
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Risk Identification", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0)
    pdf.ln(8)
    pdf.cell(0, 10, f"Overall Risk Ranking: {risk_level.upper()}", ln=1)
    
    # Risk Insights
    if "risk" in insights:
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, insights["risk"])
    
    # Section 3: Tax Slabs
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Tax Slabs", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.ln(5)
    with pdf.table() as table:
        headers = table.row()
        headers.cell("Slab")
        headers.cell("Income Range")
        headers.cell("Tax Rate")
        for slab in tax_slabs:
            row = table.row()
            row.cell(str(slab['slab']))
            row.cell(slab['range'])
            row.cell(slab['tax_rate'])
    
    # Tax Insights
    if "tax" in insights:
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, insights["tax"])
    
    # Section 4: Visual Plots
    if os.path.exists(visual_plots_dir):
        for image_file in sorted(os.listdir(visual_plots_dir)):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Visual Analysis: {image_file.split('.')[0]}", ln=1)
                pdf.image(os.path.join(visual_plots_dir, image_file), x=20, w=pdf.w - 40, keep_aspect_ratio=True)
                
                # Visual-specific insights
                image_name = image_file.split('.')[0]
                if "visual" in insights and image_name in insights["visual"]:
                    pdf.ln(5)
                    pdf.set_font("Arial", 'I', 11)
                    pdf.set_text_color(50, 50, 50)
                    pdf.multi_cell(0, 6, insights["visual"][image_name])
    else:
        pdf.add_page()
        pdf.cell(0, 10, "No visual plots found.", ln=1)
    
    pdf.output(output_pdf)
    print(f"Report compiled as {output_pdf}")

# Example usage (you can remove this if not needed)
if __name__ == "__main__":
    sample_projections = {
        "projected_revenue": [{"name": "Sales", "projected_amount": 100000}],
        "projected_expenditure": [{"name": "R&D", "projected_amount": 50000}],
        "projected_inflation": {"year": "2024", "rate": "2.5"},
        "projected_gdp_growth": {"year": "2024", "rate": "3.0"}
    }
    sample_risk_level = "medium"
    sample_tax_slabs = [{"slab": 1, "range": "0-50000", "tax_rate": "10%"}]
    
    sample_insights = {
        "revenue": "Analysis shows strong sales performance projected for the coming fiscal year, with a steady revenue stream anticipated.",
        "expenditure": "R&D spending represents a significant investment in future growth and competitive advantage.",
        "economic": "The economic outlook shows healthy GDP growth outpacing inflation, suggesting a favorable environment for continued expansion.",
        "risk": "The medium risk assessment indicates balanced opportunity with manageable challenges that require regular monitoring.",
        "tax": "The current tax structure is designed to encourage investment while ensuring fiscal sustainability."
    }
    
    compile_report(sample_projections, sample_risk_level, sample_tax_slabs, insights=sample_insights)