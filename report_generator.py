from fpdf import FPDF
import os

def generate_report(img, hazards, risk_score, plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="HazardEye Safety Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Detected Hazards: {', '.join(hazards)}", ln=True)
    pdf.cell(200, 10, txt=f"Risk Score: {risk_score}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Action Plan:", ln=True)
    for step in plan:
        pdf.multi_cell(0, 10, f"- {step}")

    report_path = "HazardEye_Report.pdf"
    pdf.output(report_path)
    return report_path
