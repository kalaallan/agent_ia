from reportlab.pdfgen import canvas
from io import BytesIO


def create_simple_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Calcule la dérivée de x^2")
    c.save()
    buffer.seek(0)
    return buffer.read()