import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def read_csv():
    products = []

    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            products.append([row[1], row[9]])

    products.pop(0)

    return products


def create_pdf(products):
    c = canvas.Canvas("output.pdf", pagesize=letter)
    c.drawString(100, 750, "Test")
    c.save()


products = read_csv()
print(products)
create_pdf()
