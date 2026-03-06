# Exportar csv

import pandas as pd

def export_csv(metadata, output):

    df = pd.DataFrame(metadata)

    df.to_csv(output, index=False)

    return output

# Exportar pdf

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

def export_pdf(metadata, output):

    data = [["Tag", "Value"]]

    for item in metadata:
        data.append([item["tag"], item["value"]])

    pdf = SimpleDocTemplate(output, pagesize=letter)

    table = Table(data)

    pdf.build([table])

    return output

# Exportar jpg

from PIL import Image, ImageDraw

def export_jpg(metadata, output):

    width = 1200
    height = 40 * (len(metadata) + 2)

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    y = 20

    for item in metadata:
        text = f"{item['tag']} : {item['value']}"
        draw.text((20, y), text, fill="black")
        y += 40

    image.save(output)

    return output
