from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(row):

    filename = f"output/{row['Name']}.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>AI Resume Screening Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Candidate:</b> {row['Name']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Predicted Role:</b> {row['Category']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Final Score:</b> {row['Score']}%", styles["BodyText"]))

    story.append(Paragraph(f"<b>Semantic Score:</b> {row['Semantic']}%", styles["BodyText"]))

    story.append(Paragraph(f"<b>Skill Score:</b> {row['Skill']}%", styles["BodyText"]))

    story.append(Paragraph(f"<b>Dataset Match:</b> {row['Dataset Similarity']}%", styles["BodyText"]))

    story.append(Paragraph("<b>Matched Skills</b>", styles["Heading2"]))

    for skill in row["Matched"]:
        story.append(Paragraph(f"• {skill}", styles["BodyText"]))

    story.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))

    for skill in row["Missing"]:
        story.append(Paragraph(f"• {skill}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Recommendation:</b>", styles["Heading2"]))

    if row["Score"] >= 90:
        rec = "Strong Hire"
    elif row["Score"] >= 75:
        rec = "Hire"
    elif row["Score"] >= 60:
        rec = "Consider"
    else:
        rec = "Reject"

    story.append(Paragraph(rec, styles["BodyText"]))

    doc.build(story)

    return filename