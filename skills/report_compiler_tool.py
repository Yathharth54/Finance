from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Budget Analysis Report', border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def compile_report(projections: dict, risk_level: str, tax_slabs: list, visual_plots_dir: str = "visual plots", output_pdf: str = "report.pdf"):
    """
    Compiles a final report in PDF format that includes:
      - Budget Projections: Listing revenue, expenditure, inflation and GDP growth projections.
      - Risk Identification: Overall risk ranking.
      - Tax Slabs: Details of tax slabs computed.
      - Visual Plots: All images from the 'visual plots' directory.
      
    Each section is headed by a title. The resulting PDF is saved as output_pdf.
    """
    pdf = PDFReport()
    pdf.add_page()

    # Section 1: Budget Projections
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
    
    pdf.ln(10)
    
    # Section 2: Risk Identification
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Risk Identification", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Overall Risk Ranking: {risk_level.upper()}", ln=1)
    pdf.ln(10)

    # Section 3: Tax Slabs
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Tax Slabs", ln=1)
    pdf.set_font("Arial", size=12)
    for slab in tax_slabs:
        pdf.cell(0, 10, f"Slab {slab['slab']}: Range: {slab['range']}, Tax Rate: {slab['tax_rate']}", ln=1)
    pdf.ln(10)

    # Section 4: Visual Plots
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Visual Plots", ln=1)
    pdf.ln(5)
    if os.path.exists(visual_plots_dir):
        for image_file in os.listdir(visual_plots_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(visual_plots_dir, image_file)
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Plot: {image_file}", ln=1)
                # Resize the image width to fit the page
                pdf.image(image_path, w=pdf.w - 40)
                pdf.ln(10)
    else:
        pdf.cell(0, 10, "No visual plots found.", ln=1)

    pdf.output(output_pdf)
    print(f"Report compiled and saved as {output_pdf}")