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
            product = Product(
                row[1].strip(),
                row[2].strip(),
                row[4].strip(),
                row[9].strip(),
                row[11].strip(),
            )
            products.append(product)

    products.pop(0)

    return products


def create_barcode(product_code):
    if len(product_code) != 12:
        product_code = "000000000000"

    upc = barcode.get_barcode_class("upca")
    upc_obj = upc(product_code[0:11], writer=ImageWriter())

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

    product_per_column = 10

    products.sort(key=lambda x: x.name)
    products.sort(key=lambda x: x.supplier)

    prev_supplier = ""
    vertical_page_index = 0
    supplier_product_index = 0

    for product_index in range(len(products)):

        product = products[product_index]

        if product.supplier != prev_supplier:
            prev_supplier = product.supplier
            vertical_page_index = 0
            supplier_product_index = 0

            if product_index != 0:
                c.showPage()

            c.drawString(100, 750, "Supplier: " + product.supplier)

        if vertical_page_index >= product_per_column:
            vertical_page_index = 0
            c.showPage()

        barcode = product.barcode
        if barcode == "":
            barcode = "000000000000"

        create_barcode(barcode)

        curr_column = supplier_product_index % 2
        vertical_displacement = 70 * vertical_page_index
        column_displacement = 250 * curr_column

        c.drawImage(
            "barcodes/" + barcode + ".png",
            100 + column_displacement,
            700 - vertical_displacement,
            width=200,
            height=40,
        )

        c.setFontSize(9)
        c.drawCentredString(
            200 + column_displacement,
            740 - vertical_displacement,
            product.name,
        )

        c.setFontSize(12)
        c.drawCentredString(
            200 + column_displacement,
            690 - vertical_displacement,
            barcode,
        )

        if curr_column == 1:
            vertical_page_index += 1

        supplier_product_index += 1

    c.save()


products = read_csv()

create_price_list(products)
create_barcode_list(products)
