import os

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator

from InvoiceGenerator.pdf import SimpleInvoice

# choosing English as the document language

os.environ["INVOICE_LANG"] = "en"

client = Client('Client company')

provider = Provider('CanteenCo', bank_account='6454-6361-217273', bank_code='2023')

creator = Creator('CanteenCo')

invoice = Invoice(client, provider, creator)

invoice.add_item(Item(25, 2, description="Milk"))

invoice.add_item(Item(12, 3, description="Fruits"))

invoice.add_item(Item(51, 4, description="Nuts"))

invoice.add_item(Item(22, 5, description="Biscuits"))

invoice.currency = "Rs."

invoice.number = "10393069"

docu = SimpleInvoice(invoice)

docu.gen("invoice2.pdf", generate_qr_code=True) #you can put QR code by setting the #qr_code parameter to ‘True’

#docu.gen("invoice.xml") ## We can also generate an XML file of this invoice