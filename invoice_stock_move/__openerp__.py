# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
{
    'name': "Stock Picking From Invoice",
    'version': '10.0.1.1.1',
    'summary': """Stock Picking From Customer/Supplier Invoice""",
    'description': """This Module Enables To Create Stocks Picking From Customer/Supplier Invoice""",
    'author': "Hiworth Solutions",
    'company': 'Hiworth Solutions',
    'website': "https://www.hiworthsolutions.com",
    'category': 'Accounting',
    'depends': ['base', 'account', 'stock','purchase','sale',"product_expiry",
                "account_accountant",'product_expiry_simple','sale_discount_total'],
    'data': [
'security/security.xml',
             'security/ir.model.access.csv',
             'views/menu.xml',
             'views/rack_transfer.xml',
             'views/partial_transfer.xml',
             'views/credit_limit.xml',
             'views/invoice_history.xml',
             'views/invoice_stock_move_view.xml',
             'views/product.xml',
             'views/invoice.xml',
             'views/stockpicking.xml',
             'expiry_manage/expiry_manage_view.xml',
             'report/customer_inv_report.xml',
             'report/supplier_inv_report.xml',
             'report/pending_invoice_report.xml',
             'report/sale_report.xml',
             'report/customer_inv_history.xml',
             'report/supplier_inv_history.xml',
             'report/purchase_report.xml',
             'report/inherit_supplier_invoice_report.xml',

             ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
