import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter


class Product:
    def __init__(self, name, supplier, pack, price, barcode):
        self.name = name
        self.supplier = supplier
        self.pack = pack
        self.price = price
        self.barcode = barcode


def read_csv():
    products = []

    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            product = Product(row[1], row[2], row[4], row[9], row[11])
            products.append(product)

    products.pop(0)

    return products


def create_barcode(product_code):
    upc = barcode.get_barcode_class("upca")
    upc_obj = upc(product_code, writer=ImageWriter())

    options = {
        "module_width": 0.4,
        "module_height": 10,
        "write_text": False,
        "quiet_zone": 0,
    }

    upc_obj.save("barcodes/" + product_code, options)


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

        c.drawString(100, 730 - 10 * j, product.name)
        c.drawString(500, 730 - 10 * j, product.price)

    c.save()


def create_barcode_list(products):
    c = canvas.Canvas("Barcode List.pdf", pagesize=letter)

    product_per_page = 10

    for i in range(len(products)):
        product = products[i]
        j = i % product_per_page

        if j == 0:
            if i != 0:
                c.showPage()

        if len(product.barcode) == 11:
            create_barcode(product.barcode)
            c.drawImage(
                "barcodes/" + product.barcode + ".png",
                100,
                710 - 70 * j,
                width=200,
                height=40,
            )
        else:
            # using an empty barcode for now to see how it looks
            create_barcode("00000000000")
            c.drawImage(
                "barcodes/" + "00000000000" + ".png",
                100,
                720 - 70 * j,
                width=200,
                height=30,
            )

        c.drawString(100, 750 - 70 * j, product.name)
        c.drawString(170, 700 - 70 * j, product.barcode)

    c.save()


products = read_csv()

create_price_list(products)
create_barcode_list(products)
