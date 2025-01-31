from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf():
    c = canvas.Canvas("output.pdf", pagesize=letter)
    c.drawString(100, 750, "Test")
    c.save()


create_pdf()
