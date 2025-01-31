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

create_price_list(products)
