import os
import pandas as pd
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def export_csv(metadata: list[dict], output_path: str) -> str:
    """Exporta la tabla de metadatos a CSV."""
    df = pd.DataFrame(metadata)
    df.to_csv(output_path, index=False)
    return output_path


def export_pdf(metadata: list[dict], output_path: str) -> str:
    """Exporta la tabla de metadatos a PDF."""
    data = [["Tag", "Value"]]
    for item in metadata:
        data.append([item["tag"], item["value"]])

    pdf = SimpleDocTemplate(output_path, pagesize=letter)
    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
    ]))
    pdf.build([table])
    return output_path


def export_jpg(metadata: list[dict], output_path: str) -> str:
    """Exporta la tabla de metadatos como imagen JPG."""
    row_height = 40
    width = 1200
    height = row_height * (len(metadata) + 2)

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    y = 20
    for item in metadata:
        draw.text((20, y), f"{item['tag']}  :  {item['value']}", fill="black")
        y += row_height

    image.save(output_path)
    return output_path