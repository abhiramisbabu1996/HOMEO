from openerp import models, fields, api, _
from openerp import tools, _
from datetime import datetime, date, timedelta


class CustomerInvoiceReport(models.TransientModel):
    _name = 'customer.invoice.report'

    partner_id = fields.Many2one('res.partner', 'Customer')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    product = fields.Many2one('product.product', 'Product')
    potency = fields.Many2one('product.medicine.subcat', 'Potency')
    packing = fields.Many2one('product.medicine.packing', 'Packing')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    group = fields.Many2one('tax.combo.new', 'Group')

    @api.multi
    def action_customer_invoice_open_window(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }

        return {
            'name': 'Customer Invoice Report',
            'type': 'ir.actions.report.xml',
            'report_name': 'invoice_stock_move.report_customer_invoice_template_new',
            'datas': datas,
            'report_type': 'qweb-pdf'
        }

    @api.multi
    def get_details(self):
        lst = []
        domain = [('invoice_id.state', '=', 'paid')]
        if self.partner_id:
            domain += [('invoice_id.partner_id', '=', self.partner_id.id)]
        if self.product:
            domain += [('product_id', '=', self.product.id)]
        if self.date_from:
            domain += [('invoice_id.date_invoice', '>=', self.date_from)]
        if self.date_to:
            domain += [('invoice_id.date_invoice', '<=', self.date_to)]
        if self.potency:
            domain += [('medicine_name_subcat', '<=', self.potency.id)]
        if self.group:
            domain += [('medicine_grp', '<=', self.group.id)]
        if self.company:
            domain += [('product_of', '<=', self.company.id)]
        if self.packing:
            domain += [('medicine_name_packing', '<=', self.packing.id)]
        invoices = self.env['account.invoice.line'].search(domain)

        for rec in invoices:
            vals = {
                'date': rec.invoice_id.date_invoice,
                'medicine': rec.product_id.name,
                'exp': rec.expiry_date,
                'mfd': rec.manf_date,
                'amount': round(rec.amt_w_tax, 2),
                'total_amt': 0,
                'group': rec.medicine_grp.medicine_grp.med_grp,
                'potency': rec.medicine_name_subcat.medicine_rack_subcat,
                'packing': rec.medicine_name_packing.medicine_pack,
                'customer': rec.invoice_id.partner_id.name,
                'company': rec.product_of.name_responsible
            }
            lst.append(vals)
        sum = 0
        for vals in lst:
            sum = round(sum + vals['amount'], 2)
        for vals in lst:
            vals['total_amt'] = sum
        return lst



        # if self.partner_id:
        #     cust_invs = self.env['account.invoice'].search(
        #         [('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to),
        #          ('partner_id', '=', self.partner_id.id)])
        # else:
        #     cust_invs = self.env['account.invoice'].search(
        #         [('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to),
        #          ])
        #
        # for rec in cust_invs:
        #     if rec.partner_id.customer == True:
        #         if rec.state == 'draft':
        #             pass
        #         else:
        #             for lines in rec.invoice_line:
        #                 if self.date_from:
        #                     pass
        #
        #
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.company.id and self.group.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (lines.product_id.id == self.product.id) and
        #                             (lines.medicine_name_subcat.id == self.potency.id) and (lines.product_of.id == self.company.id)
        #                             and (lines.medicine_grp.id == self.group.id)and(lines.medicine_name_packing.id==self.packing.id)):
        #
        #
        #
        #                         vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amt_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                         }
        #                         lst.append(vals)
        #
        #                 # .................end of 6 Combination................................................
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.company.id and self.group.id:
        #                     if((lines.partner_id.id == self.partner_id.id)and(lines.product_id.id == self.product.id)and
        #                        (lines.medicine_name_subcat.id == self.potency.id)and(lines.product_of.id==self.company)
        #                             and(lines.medicine_grp.id==self.group.id)):
        #
        #                         if (self.packing.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amt_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.company.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (lines.product_id.id == self.product.id) and
        #                             (lines.medicine_name_subcat.id == self.potency.id) and (lines.product_of.id == self.company)
        #                             and (lines.medicine_name_packing.id == self.packing.id)):
        #
        #                         if (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amt_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.group.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (lines.product_id.id == self.product.id) and
        #                             (lines.medicine_name_subcat.id == self.potency.id) and (lines.medicine_grp.id == self.group)
        #                             and (lines.medicine_name_packing.id == self.packing.id)):
        #
        #                         if (self.company.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amt_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.company.id and self.group.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (lines.product_id.id == self.product.id) and
        #                             (lines.product_of.id == self.company.id) and (lines.medicine_grp.id == self.group)
        #                             and (lines.medicine_name_packing.id == self.packing.id)):
        #
        #                         if (self.potency.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.potency.id and self.company.id and self.group.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (lines.medicine_name_subcat.id == self.potency.id) and
        #                             (lines.product_of.id == self.company.id) and (lines.medicine_grp.id == self.group)
        #                             and (lines.medicine_name_packing.id == self.packing.id)):
        #
        #                         if (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.potency.id and self.company.id and self.group.id and self.packing.id:
        #                     if ((lines.product_id.id == self.product.id) and (lines.medicine_name_subcat.id == self.potency.id) and
        #                             (lines.product_of.id == self.company.id) and (lines.medicine_grp.id == self.group)
        #                             and (lines.medicine_name_packing.id == self.packing.id)):
        #
        #                         if (self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #
        #                 # .......................End of 5 combinations.....................................
        #                 if self.partner_id.id and self.product.id and self.packing.id and self.group.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.potency.id == False) and (
        #                                 self.company.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.packing.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.potency.id == False) and (
        #                                 self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.packing.id and self.group.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.medicine_grp.id == self.group.id) and (
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.potency.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #
        #                 if self.partner_id.id and self.packing.id and self.company.id and self.potency.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.product_of.id == self.company.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)):
        #                         if (self.group.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.packing.id and self.group.id and self.potency.id and self.company.id:
        #                     if ((lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.product_of.id == self.company.id)):
        #                         if (self.product.id == False)and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #
        #                 if self.product.id and self.group.id and self.company.id and self.potency.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.product_of.id == self.company.id)):
        #                         if (self.partner_id.id == False)and (
        #                                 self.packing.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #
        #
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.product_of.id == self.company.id)):
        #                         if (self.packing.id == False)and (
        #                                 self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.medicine_name_packing.id == self.packing.id)):
        #                         if (self.company.id == False)and (
        #                                 self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.potency.id and self.group.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.medicine_grp.id == self.group.id)):
        #                         if (self.packing.id == False)and (
        #                                 self.company.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.group.id and self.potency.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.medicine_grp.id == self.group.id)):
        #                         if (self.product.id == False)and (
        #                                 self.company.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.group.id and self.potency.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)and (lines.product_of.id == self.company.id)):
        #                         if (self.packing.id == False)and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id and self.potency.id and self.packing.id and self.company.id:
        #                     if ((lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)and (lines.product_of.id == self.company.id)):
        #                         if (self.product.id == False)and (
        #                                 self.partner.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id and self.potency.id and self.packing.id and self.product.id:
        #                     if ((lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)and (lines.product_id.id == self.product.id)):
        #                         if (self.company.id == False)and (
        #                                 self.partner.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.potency.id and self.packing.id and self.company.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)and (lines.product_of.id == self.company.id)):
        #                         if (self.group.id == False)and (
        #                                 self.partner.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #
        #                 # ........................ End of combination of 4............................
        #                 if self.partner_id.id and self.product.id and self.potency.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)):
        #                         if (self.packing.id == False) and (self.company.id == False) and (
        #                                 self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.group.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.packing.id == False) and (self.company.id == False) and (
        #                                 self.potency.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.packing.id == False) and (self.group.id == False) and (
        #                                 self.potency.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.product.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)):
        #                         if (self.company.id == False) and (self.group.id == False) and (
        #                                 self.potency.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.potency.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)):
        #                         if (self.company.id == False) and (self.group.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.potency.id and self.group.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_grp == self.group.id)):
        #                         if (self.company.id == False) and (self.packing.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.potency.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.product_of == self.company.id)):
        #                         if (self.group.id == False) and (self.packing.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.group.id and self.company.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_grp.id == self.group.id) and (
        #                             lines.product_of == self.company.id)):
        #                         if (self.potency.id == False) and (self.packing.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.group.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_packing == self.packing.id)):
        #                         if (self.potency.id == False) and (self.company.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.partner_id.id and self.company.id and self.packing.id:
        #                     if ((lines.partner_id.id == self.partner_id.id) and (
        #                             lines.product_of.id == self.company.id) and (
        #                             lines.medicine_name_packing == self.packing.id)):
        #                         if (self.potency.id == False) and (self.group.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.company.id and self.packing.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.product_of.id == self.company.id) and (
        #                             lines.medicine_name_packing == self.packing.id)):
        #                         if (self.potency.id == False) and (self.group.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.company.id and self.potency.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.product_of.id == self.company.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)):
        #                         if (self.packing.id == False) and (self.group.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.company.id and self.group.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.product_of.id == self.company.id) and (
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.packing.id == False) and (self.potency.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.packing.id and self.potency.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)):
        #                         if (self.company.id == False) and (self.group.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.packing.id and self.group.id:
        #                     if ((lines.product_id.id == self.product.id) and (lines.medicine_name_packing.id == self.packing.id)and(
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.company.id == False) and (self.potency.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.potency.id and self.group.id:
        #                     if ((lines.product_id.id == self.product.id) and (lines.medicine_name_subcat.id == self.potency.id)and(
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.company.id == False) and (self.packing.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.potency.id and self.packing.id and self.group.id:
        #                     if ((lines.medicine_name_subcat.id == self.potency.id) and (lines.medicine_name_packing.id == self.packing.id)and(
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.company.id == False) and (self.product.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.potency.id and self.packing.id and self.company.id:
        #                     if ((lines.medicine_name_subcat.id == self.potency.id) and (lines.medicine_name_packing.id == self.packing.id)and(
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.group.id == False) and (self.product.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id and self.packing.id and self.company.id:
        #
        #                     if ((lines.medicine_grp.id == self.group.id) and (lines.medicine_name_packing.id == self.packing.id)and(
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.potency.id == False) and (self.product.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id and self.packing.id and self.potency.id:
        #                     if ((lines.medicine_grp.id == self.group.id) and (lines.medicine_name_packing.id == self.packing.id)and(
        #                             lines.medicine_name_subcat.id == self.potency.id)):
        #                         if (self.company.id == False) and (self.product.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 # _________________________________________End Of Combination of 3___________________________________________
        #                 if self.product.id and self.potency.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_subcat.id == self.potency.id)):
        #                         if (self.packing.id == False) and (self.company.id == False) and (self.group.id == False) and (
        #                                 self.partner_id.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.group.id:
        #                     if ((lines.product_id.id == self.product.id) and (lines.medicine_grp.id == self.group.id)):
        #                         if (self.packing.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.potency.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.company.id:
        #                     if ((lines.product_id.id == self.product.id) and (lines.product_of.id == self.company.id)):
        #                         if (self.packing.id == False) and (self.partner_id.id == False) and (
        #                                 self.potency.id == False) and (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.packing.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)):
        #                         if (self.potency.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id and self.partner_id.id:
        #                     if ((lines.product_id.id == self.product.id) and (
        #                             lines.partner_id.id == self.partner_id.id)):
        #                         if (self.potency.id == False) and (self.packing.id == False) and (
        #                                 self.company.id == False) and (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.potency.id and self.group.id:
        #                     if ((lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_grp.id == self.group.id)):
        #                         if (self.packing.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.potency.id and self.company.id:
        #                     if ((lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.packing.id == False) and (self.partner_id.id == False) and (
        #                                 self.group.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.potency.id and self.packing.id:
        #                     if ((lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)):
        #                         if (self.group.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #                 if self.potency.id and self.partner_id.id:
        #                     if ((lines.medicine_name_subcat.id == self.potency.id) and (
        #                             lines.partner_id.id == self.partner_id.id)):
        #                         if (self.group.id == False) and (self.packing.id == False) and (
        #                                 self.company.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id and self.company.id:
        #                     if ((lines.medicine_grp.id == self.group.id) and (
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.packing.id == False) and (self.partner_id.id == False) and (
        #                                 self.potency.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id and self.packing.id:
        #                     if ((lines.medicine_grp.id == self.group.id) and (
        #                             lines.medicine_name_packing.id == self.packing.id)):
        #                         if (self.company.id == False) and (self.partner_id.id == False) and (
        #                                 self.potency.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #                 if self.group.id and self.partner_id.id:
        #                     if ((lines.medicine_grp.id == self.group.id) and (
        #                             lines.partner_id.id == self.partner_id.id)):
        #                         if (self.company.id == False) and (self.packing.id == False) and (
        #                                 self.potency.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.company.id and self.packing.id:
        #                     if ((lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.product_of.id == self.company.id)):
        #                         if (self.group.id == False) and (self.partner_id.id == False) and (
        #                                 self.potency.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #
        #                             }
        #                             lst.append(vals)
        #                 if self.company.id and self.partner_id.id:
        #                     if ((lines.medicine_name_packing.id == self.packing.id) and (
        #                             lines.partner_id.id == self.partner_id.id)):
        #                         if (self.group.id == False) and (self.packing.id == False) and (self.potency.id == False) and (
        #                                 self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.packing.id:
        #                     if (lines.medicine_name_packing.id == self.packing.id):
        #                         if (self.potency.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.product.id == False) and (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id:
        #                     if (lines.product_of.id == self.company.id):
        #                         if (self.potency.id == False) and (self.partner_id.id == False) and (
        #                                 self.product.id == False) and (self.packing.id == False) and (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.group.id:
        #                     if (lines.medicine_grp.id == self.group.id):
        #                         if (self.potency.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.packing.id == False) and (self.product.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #
        #                 if self.product.id:
        #                     if (lines.product_id.id == self.product.id):
        #                         if (self.potency.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.packing.id == False) and (self.group.id == False):
        #                             if rec.partner_id.customer == True:
        #                                 vals = {
        #
        #                                     'date': rec.date_invoice,
        #                                     'medicine': lines.product_id.name,
        #                                     'exp': lines.expiry_date,
        #                                     'mfd': lines.manf_date,
        #                                     'amount': round(lines.amount_w_tax, 2),
        #                                     'total_amt': 0,
        #                                     'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                     'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                     'packing': lines.medicine_name_packing.medicine_pack,
        #                                     'customer': rec.partner_id.name,
        #                                     'company': lines.product_of.name_responsible
        #                                 }
        #                                 lst.append(vals)
        #
        #                 if self.potency.id:
        #
        #                     if (lines.medicine_name_subcat.id == self.potency.id):
        #                         if (self.product.id == False) and (self.partner_id.id == False) and (
        #                                 self.company.id == False) and (self.packing.id == False) and (self.group.id == False):
        #
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)
        #                 if self.partner_id.id:
        #                     if (lines.partner_id.id == self.partner_id.id):
        #                         if (self.potency.id == False) and (self.product.id == False) and (
        #                                 self.company.id == False) and (self.packing.id == False) and (self.group.id == False):
        #                             vals = {
        #
        #                                 'date': rec.date_invoice,
        #                                 'medicine': lines.product_id.name,
        #                                 'exp': lines.expiry_date,
        #                                 'mfd': lines.manf_date,
        #                                 'amount': round(lines.amount_w_tax, 2),
        #                                 'total_amt': 0,
        #                                 'group': lines.medicine_grp.medicine_grp.med_grp,
        #                                 'potency': lines.medicine_name_subcat.medicine_rack_subcat,
        #                                 'packing': lines.medicine_name_packing.medicine_pack,
        #                                 'customer': rec.partner_id.name,
        #                                 'company': lines.product_of.name_responsible
        #                             }
        #                             lst.append(vals)

        sum = 0
        for vals in lst:
            sum = round(sum + vals['amount'], 2)
        for vals in lst:
            vals['total_amt'] = sum
        return lst
