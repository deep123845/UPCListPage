import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter


def read_csv():
    products = []

    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            products.append([row[1], row[9], row[11]])

    products.pop(0)

    return products


def create_barcode(product_code):
    upc = barcode.get_barcode_class("upca")

    upc_obj = upc(product_code, writer=ImageWriter())
    upc_obj.save("barcodes/" + product_code)


def create_price_list(products):
    c = canvas.Canvas("Price List.pdf", pagesize=letter)

    product_per_page = 70

    for i in range(len(products)):
        product = products[i]
        j = i % product_per_page

        if j == 0:
            if i != 0:
                c.showPage()

            c.drawString(100, 750, "Product Name")
            c.drawString(500, 750, "Price")

        c.drawString(100, 730 - 10 * j, product[0])
        c.drawString(500, 730 - 10 * j, product[1])

    c.save()


products = read_csv()

for product in products:
    if len(product[2]) == 12:
        create_barcode(product[2].strip())

create_price_list(products)
