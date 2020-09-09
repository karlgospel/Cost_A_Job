#!/usr/bin/env python3
from datetime import datetime, date
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice
from Customers import *
from Company import *
from JobMaterials import *

class InvoiceMaker1:
    
    def createInvoice(ID, job):
        doc = SimpleInvoice('invoice.pdf')
        
        # Paid stamp, optional
        doc.is_paid = True
        
        doc.invoice_info = InvoiceInfo(1023, datetime.now(), datetime.now())  # Invoice info, optional
        
        companyName = Company.getName(ID)
        companyAddress = Company.getAddress(ID)
        companyCity = Company.getCity(ID)
        companyPostcode = Company.getPostcode(ID)
        companyPhone = Company.getPhone(ID)
        companyAccNumber = Company.getAccNumber(ID)
        companySortCode = Company.getSort(ID)
        # Service Provider Info, optional
        doc.service_provider_info = ServiceProviderInfo(
            name = companyName,
            street = companyAddress,
            city = companyCity,
            post_code = companyPostcode,
            vat_tax_number='Vat/Tax number'
        )
        
        clientName = Customers.getName(ID)
        clientAddress = Customers.getAddress(ID)
        clientCity = Customers.getCity(ID)
        clientPostcode = Customers.getPostcode(ID)
        # Client info, optional
        doc.client_info = ClientInfo(
            name = clientName,
            street = clientAddress,
            city = clientCity,
            post_code = clientPostcode,
            email='client@example.com'
            )
        invoiceMaterials = JobMaterials.getInvoiceMaterials(job)

        for each in invoiceMaterials:
            materialName = each[0]
            pricePerUnit = each[1]
            desc = each[2]
            quantity = each[3]
            doc.add_item(Item(materialName,desc,quantity,pricePerUnit))  
        # Add Item
        #doc.add_item(Item('Item', 'Item desc', 1, '1.1'))
        #doc.add_item(Item('Item', 'Item desc', 2, '2.2'))
        #doc.add_item(Item('Item', 'Item desc', 3, '3.3'))
        
        # Tax rate, optional
        doc.set_item_tax_rate(20)  # 20%
        
        ## Transactions detail, optional
        #doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
        #doc.add_transaction(Transaction('Stripe', 222, date.today(), 2))
        
        # Optional
        doc.set_bottom_tip("Email: example@example.com<br />Don't hesitate to contact us for any questions.")
        
        doc.finish()

InvoiceMaker1.createInvoice(1, "Karl")