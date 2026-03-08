from fpdf import FPDF
import io


def generate_osha_300_pdf(data: dict) -> bytes:
    """Generate OSHA 300 Log as PDF."""
    pdf = FPDF(orientation="L", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"OSHA Form 300 - Log of Work-Related Injuries and Illnesses ({data['year']})", ln=True, align="C")
    pdf.ln(5)

    # Table header
    pdf.set_font("Helvetica", "B", 7)
    col_widths = [12, 35, 30, 22, 30, 50, 25, 25, 12, 18, 18, 12]
    headers = ["Case#", "Employee", "Job Title", "Date", "Location", "Description", "Injury Type", "Body Part", "Death", "Days Away", "Days Restr.", "ER"]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C")
    pdf.ln()

    # Table rows
    pdf.set_font("Helvetica", "", 6)
    for entry in data.get("entries", []):
        pdf.cell(col_widths[0], 7, str(entry.get("case_number", "")), border=1, align="C")
        pdf.cell(col_widths[1], 7, str(entry.get("employee_name", ""))[:25], border=1)
        pdf.cell(col_widths[2], 7, str(entry.get("job_title", ""))[:20], border=1)
        pdf.cell(col_widths[3], 7, str(entry.get("date_of_injury", "")), border=1, align="C")
        pdf.cell(col_widths[4], 7, str(entry.get("location", ""))[:20], border=1)
        pdf.cell(col_widths[5], 7, str(entry.get("description", ""))[:40], border=1)
        pdf.cell(col_widths[6], 7, str(entry.get("injury_type", ""))[:18], border=1)
        pdf.cell(col_widths[7], 7, str(entry.get("body_part_affected", ""))[:18], border=1)
        pdf.cell(col_widths[8], 7, "Y" if entry.get("death") else "N", border=1, align="C")
        pdf.cell(col_widths[9], 7, str(entry.get("days_away", 0)), border=1, align="C")
        pdf.cell(col_widths[10], 7, str(entry.get("days_restricted", 0)), border=1, align="C")
        pdf.cell(col_widths[11], 7, "Y" if entry.get("treated_in_er") else "N", border=1, align="C")
        pdf.ln()

    # Summary
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 8, f"Total Cases: {data.get('total_cases', 0)}", ln=True)

    return pdf.output()


def generate_osha_300a_pdf(data: dict) -> bytes:
    """Generate OSHA 300A Summary as PDF."""
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"OSHA Form 300A - Summary of Work-Related Injuries and Illnesses ({data['year']})", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 11)
    rows = [
        ("Total number of cases", str(data.get("total_cases", 0))),
        ("Total deaths", str(data.get("total_deaths", 0))),
        ("Cases with days away from work", str(data.get("total_days_away_cases", 0))),
        ("Total days away from work", str(data.get("total_days_away", 0))),
        ("Cases with job transfer or restriction", str(data.get("total_restricted_cases", 0))),
        ("Total days of job transfer or restriction", str(data.get("total_days_restricted", 0))),
        ("Other recordable cases", str(data.get("total_other_cases", 0))),
    ]

    for label, value in rows:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(120, 9, label, border=1)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(40, 9, value, border=1, align="C")
        pdf.ln()

    # Injury type breakdown
    breakdown = data.get("injury_type_breakdown", {})
    if breakdown:
        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Injury Type Breakdown", ln=True)
        pdf.set_font("Helvetica", "", 11)
        for itype, count in breakdown.items():
            pdf.cell(120, 8, itype, border=1)
            pdf.cell(40, 8, str(count), border=1, align="C")
            pdf.ln()

    return pdf.output()


def generate_osha_301_pdf(data: dict) -> bytes:
    """Generate OSHA 301 Incident Report as PDF."""
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "OSHA Form 301 - Injury and Illness Incident Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 11)
    fields = [
        ("Case Number", str(data.get("case_number", ""))),
        ("Employee Name", data.get("employee_name", "")),
        ("Job Title", data.get("job_title", "")),
        ("Date of Injury", str(data.get("date_of_injury", ""))),
        ("Time of Event", str(data.get("time_of_event", ""))),
        ("Location", data.get("location", "")),
        ("Description of Injury", data.get("description_of_injury", "")),
        ("Body Part Affected", data.get("body_part_affected", "")),
        ("Object/Substance", data.get("object_or_substance", "")),
        ("Death", "Yes" if data.get("death") else "No"),
        ("Days Away from Work", str(data.get("days_away", 0))),
        ("Days of Restricted Activity", str(data.get("days_restricted", 0))),
        ("Treated in ER", "Yes" if data.get("treated_in_er") else "No"),
        ("Hospitalized", "Yes" if data.get("hospitalized") else "No"),
        ("Severity", data.get("severity", "")),
        ("Witness Info", data.get("witness_info", "")),
        ("Immediate Actions Taken", data.get("immediate_actions", "")),
    ]

    for label, value in fields:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(60, 9, label, border=1)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 9, str(value)[:80], border=1, ln=True)

    return pdf.output()
