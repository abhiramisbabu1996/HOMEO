from openerp import models, fields, api, _
from openerp import tools, _
from datetime import datetime, date, timedelta


class CustomerInvoiceReport(models.TransientModel):
    _name = 'purchase.invoice.report'

    partner_id = fields.Many2one('res.partner', 'Customer')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    product = fields.Many2one('product.product', 'Product')
    potency = fields.Many2one('product.medicine.subcat', 'Potency')
    packing = fields.Many2one('product.medicine.packing', 'Packing')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    group = fields.Many2one('tax.combo.new', 'Group')
