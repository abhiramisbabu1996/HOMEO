import datetime

from openerp import api, models, fields


class TaxReportWizard(models.TransientModel):
    _name = 'tax.report.wizard'

    from_date = fields.Date()
    customer = fields.Many2one('res.partner', domain=[('customer', '=', True)])
    product = fields.Many2one('product.product')
    potency = fields.Many2one('product.medicine.subcat')
    to_date = fields.Date()
    group = fields.Many2one('product.medicine.group')
    company = fields.Many2one('product.medicine.responsible')
    packing = fields.Many2one('product.medicine.packing')

    @api.multi
    def view_tax_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'customer_sale_history.tax_report_template',
            'datas': datas,
            'report_type': 'qweb-html',
        }

    @api.model
    def get_tax_invoices(self):
        domain = []
        if self.from_date:
            domain = [('invoice_id.date_invoice', '>=', self.from_date)]
        if self.to_date:
            domain += [('invoice_id.date_invoice', '<=', self.to_date)]
        if not self.to_date:
            domain += [('invoice_id.date_invoice', '<=', datetime.datetime.today())]
        if self.customer:
            domain += [('invoice_id.partner_id', '=', self.customer.id)]
        if self.product:
            domain += [('product_id', '=', self.product.id)]
        if self.potency:
            domain += [('product_medicine_subcat', '=', self.potency.id)]
        if self.packing:
            domain += [('medicine_name_packing', '=', self.packing.id)]
        if self.company:
            domain += [('product_of', '=', self.company.id)]
        if self.group:
            domain += [('medicine_grp', '=', self.group.id)]

        res = self.env['account.invoice.line'].search(domain)

        return res

    @api.multi
    def print_tax_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'customer_sale_history.tax_report_template',
            'datas': datas,
            'report_type': 'qweb-pdf',
            #
        }
