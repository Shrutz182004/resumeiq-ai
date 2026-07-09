from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor

import os
import uuid

OUTPUT_FOLDER = "generated_resumes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_resume_pdf(content: str):
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#003366")

    heading_style = styles["Heading2"]
    heading_style.textColor = HexColor("#003366")

    normal_style = styles["BodyText"]

    story = []

    lines = content.split("\n")

    first_line = True

    headings = [
        "Summary",
        "Skills",
        "Projects",
        "Education",
        "Experience",
        "Certifications",
        "Certifications & Training",
    ]

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 10))
            continue

        # Remove markdown
        line = line.replace("**", "")

        # Convert markdown bullets
        if line.startswith("*"):
            line = "• " + line[1:].strip()

        # First line = Candidate Name
        if first_line:
            story.append(Paragraph(line, title_style))
            story.append(Spacer(1, 18))
            first_line = False
            continue

        if line in headings:
            story.append(Spacer(1, 12))
            story.append(Paragraph(line, heading_style))
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(line, normal_style))

    doc.build(story)

    return filename, filepath