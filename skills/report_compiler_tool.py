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

def compile_report(projections: dict, risk_level: str, tax_slabs: list, visual_plots_dir: str = "visual plots", output_pdf: str = "report.pdf"):
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
    
    # Expenditure Table
    pdf.ln(8)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Projected Expenditures", ln=1)
    pdf.set_font("Arial", size=11)
    with pdf.table() as table:
        for exp in projections.get("projected_expenditure", []):
            row = table.row()
            row.cell(exp.get("name", "Unknown"))
            row.cell(f"${exp.get('projected_amount', 0):,.2f}")
    
    # Inflation & GDP
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Projected Inflation (2026): {projections.get('projected_inflation', {}).get('rate', 'N/A')}%", ln=1)
    pdf.cell(0, 10, f"Projected GDP Growth (2026): {projections.get('projected_gdp_growth', {}).get('rate', 'N/A')}%", ln=1)
    
    # Section 2: Risk Identification
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Risk Identification", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0)
    pdf.ln(8)
    pdf.cell(0, 10, f"Overall Risk Ranking: {risk_level.upper()}", ln=1)
    
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
    
    # Section 4: Visual Plots
    if os.path.exists(visual_plots_dir):
        for image_file in sorted(os.listdir(visual_plots_dir)):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Visual Analysis: {image_file.split('.')[0]}", ln=1)
                pdf.image(os.path.join(visual_plots_dir, image_file), x=20, w=pdf.w - 40, keep_aspect_ratio=True)
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
        "projected_inflation": {"year": "2024", "rate": "2.5%"},
        "projected_gdp_growth": {"year": "2024", "rate": "3.0%"}
    }
    sample_risk_level = "medium"
    sample_tax_slabs = [{"slab": 1, "range": "0-50000", "tax_rate": "10%"}]
    compile_report(sample_projections, sample_risk_level, sample_tax_slabs)