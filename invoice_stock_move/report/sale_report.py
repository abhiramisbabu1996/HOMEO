from openerp import models, fields, api, _
from openerp import tools, _
from datetime import datetime, date, timedelta


class SaleReport(models.TransientModel):
    _name = 'sale.report.cus'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    product = fields.Many2one('product.product', 'Product')
    packing = fields.Many2one('product.medicine.packing', 'Packing')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    group = fields.Many2one('tax.combo.new', 'Group')

    @api.multi
    def action_sale_report_open_window(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }

        return {
            'name': 'Sale Report',
            'type': 'ir.actions.report.xml',
            'report_name': 'invoice_stock_move.sale_report_template_new',
            'datas': datas,
            'report_type': 'qweb-pdf'
        }

    @api.multi
    def view_sale_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'invoice_stock_move.sale_report_template_new',
            'datas': datas,
            'report_type': 'qweb-html',
        }

    @api.multi
    def get_details(self):
        d1 = self.date_from
        d2 = self.date_to
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        lst = []

        if self.date_from:
            cust_invs = self.env['account.invoice'].search(
                [('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to),
                 ])
            for rec in cust_invs:
                if rec.state == 'draft':
                    pass
                    print("ERICA...")
                else:
                    for lines in rec.invoice_line:
                        if self.product.id and self.company.id and self.group.id and self.packing.id:
                            if ((lines.product_id.id == self.product.id) and (
                                            lines.product_of.id == self.company.id)
                                    and (lines.medicine_grp.id == self.group.id) and (
                                            lines.medicine_name_packing.id == self.packing.id)):
                                vals = {
                                    'inv_no': rec.number,
                                    'date': rec.date_invoice,
                                    'customer': rec.partner_id.name,
                                    'bill_type':"none",
                                    'medicine': lines.product_id.name,
                                    'qty': lines.quantity,
                                }
                                lst.append(vals)
                        if self.product.id and self.company.id and self.group.id:
                            if ((lines.product_id.id == self.product.id) and (
                                            lines.product_of.id == self.company.id)
                                    and (lines.medicine_grp.id == self.group.id)):
                                if (self.packing.id == False):
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)
                        if self.product.id and self.company.id and self.packing.id:
                            if ((lines.product_id.id == self.product.id) and (
                                    lines.product_of.id == self.company.id)and (
                                            lines.medicine_name_packing.id == self.packing.id)):
                                if (self.group.id == False):
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)
                        if self.product.id and self.company.id:
                            if ((lines.product_id.id == self.product.id) and (
                                    lines.product_of.id == self.company.id)):
                                if (self.group.id == False) and (self.packing.id == False):
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)
                        if self.product.id:
                            if ((lines.product_id.id == self.product.id)):
                                print("hitsssssssssss")
                                print(self.group.id,self.packing.id,self.company.id)
                                if (self.group.id == False) and (self.packing.id == False) and (self.company.id == False):
                                    print("knocked")
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)
                        if self.company.id:
                            if ((lines.product_of.id == self.company.id)):
                                if (self.group.id == False) and (self.packing.id == False) and (self.product.id == False):
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)
                        if self.group.id:
                            if ((lines.medicine_grp.id == self.group.id)):
                                if (self.company.id == False) and (self.packing.id == False) and (self.product.id == False):
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)
                        if self.packing.id:
                            if ((lines.medicine_name_packing.id == self.packing.id)):
                                if (self.company.id == False) and (self.packing.id == False) and (self.product.id == False):
                                    vals = {
                                        'inv_no': rec.number,
                                        'date': rec.date_invoice,
                                        'customer': rec.partner_id.name,
                                        'bill_type': "none",
                                        'medicine': lines.product_id.name,
                                        'qty': lines.quantity,
                                    }
                                    lst.append(vals)

            return lst
