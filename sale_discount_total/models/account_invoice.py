from openerp import api, models, fields
from openerp.osv import osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount = fields.Float(string='Dis1',
                            # digits=(16, 10),
                            # digits= dp.get_precision('Discount'),
                            default=0.0,
                            # compute = "_get_sup_discount_amt"
                            )
    # compute = "_get_sup_discount_amt"
    # @api.one
    # @api.depends('product_id', 'medicine_name_subcat', 'medicine_grp', 'medicine_name_subcat')
    # def _get_sup_discount_amt(self):
    #     if self.partner_id.supplier == True:
    #         for rec in self:
    #             s_obj = self.env['supplier.discounts'].search([('supplier','=',rec.partner_id.id)])
    #             if s_obj:
    #                 print("abhizzzzzzzzzzz",s_obj.supplier.name)
    #                 for lines in s_obj.lines:
    #                     # for lines in items:
    #                     #     if (lines.supplier.id == rec.partner_id.id):
    #                     #         print("discount", lines.supplier.name)
    #                             print("inv line", rec.partner_id.name)
    #                             if (lines.company.id == rec.product_of.id):
    #                                 if (lines.medicine_1.id == rec.product_id.id):
    #                                     if (lines.potency.id == rec.medicine_name_subcat.id):
    #                                         if (lines.medicine_grp1.id == rec.medicine_grp.id):
    #                                             if (lines.medicine_name_packing.id == rec.medicine_name_packing.id):
    #                                                 print("555555555555555555555555555555555555555555555555")
    #                                                 rec.discount = lines.discount



# PRODUCT SEARCH FOR INVOICE LINE


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        if not ids: return []
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_voucher',
                                                                             'view_vendor_receipt_dialog_form')

        inv = self.browse(cr, uid, ids[0], context=context)
        return {
            'name': _("Pay Invoice"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'payment_expected_currency': inv.currency_id.id,
                'default_partner_id': self.pool.get('res.partner')._find_accounting_partner(inv.partner_id).id,
                'default_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                'default_reference': inv.name,
                'close_after_process': True,
                'invoice_type': inv.type,
                'invoice_id': inv.id,
                'default_type': inv.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment',
                'type': inv.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment'
            }
        }

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

    # FOOTER TOTAL AMT CALCULATIONS
    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        if self.partner_id.supplier == True:
            disc = 0.0
            total_dis = 0
            tax_total = 0
            test = 0
            test2 =0
            test3 =0
            for inv in self:
                for line in inv.invoice_line:
                    print line.discount
                    disc += (line.quantity * line.price_unit) * line.discount / 100
                    test += line.grand_total
                    test3 = test3+line.rate_amt
                    test2 = test2+(line.quantity * line.price_unit)
                    total_dis = total_dis +(line.dis1 + line.dis2)
                    tax_total = tax_total+line.amount_amount1
            self.amount_untaxed = test2
            self.amount_tax = tax_total
            total_d = test2 - test3
            self.amount_discount = total_d
            # self.amount_total = ((test2 -total_d) + tax_total)
            self.amount_total = test
        if self.partner_id.customer == True:
            disc = 0.0
            total_dis = 0
            tax_total = 0
            test = 0
            test2 = 0
            test3 = 0
            for inv in self:
                for line in inv.invoice_line:
                    print line.discount
                    disc += (line.quantity * line.price_unit) * line.discount / 100
                    test += line.amt_w_tax
                    test3 = test3 + line.amt_w_tax
                    test2 = test2 + (line.quantity * line.price_unit)
                    total_dis = total_dis + (line.dis1 + line.dis2)
                    tax_total = tax_total + line.amt_tax
            self.amount_untaxed = test2
            self.amount_tax = tax_total
            total_d = test2 - (test3-tax_total)
            self.amount_discount = total_d
            # self.amount_total = ((test2 -total_d) + tax_total)
            self.amount_total = test


    discount_category = fields.Many2one('cus.discount','Discount Category')
    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount'),],default='percent', string='Discount Type', readonly=True,
                                     states={'draft': [('readonly', False)]},)
    discount_rate = fields.Float('Discount Rate', compute='compute_discount_rate',
                                 digits_compute=dp.get_precision('Account'),
                                 readonly=True,
                                 states={'draft': [('readonly', False)]},)
    amount_discount = fields.Float(string='Discount',
                                   digits=dp.get_precision('Account'),
                                   readonly=True, compute='_compute_amount')
    amount_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
                                  readonly=True, compute='_compute_amount', track_visibility='always')
    amount_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
                              readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
                                readonly=True, compute='_compute_amount')


    @api.onchange('discount_category')
    def onchange_category_id(self):
        for rec in self:
            if rec.type != 'in_invoice':
                rec.discount_rate = rec.discount_category.percentage
                for line in rec.invoice_line:
                    line.discount = rec.discount_category.percentage

    @api.depends('discount_category')
    def compute_discount_rate(self):
        for rec in self:
            if rec.type != 'in_invoice':
                rec.discount_rate = rec.discount_category.percentage
                for line in rec.invoice_line:
                    line.discount = rec.discount_category.percentage

    @api.multi
    def compute_discount(self, discount):
        for inv in self:
            val1 = val2 = 0.0
            disc_amnt = 0.0
            val2 = sum(line.amount for line in self.tax_line)
            for line in inv.invoice_line:
                val1 += (line.quantity * line.price_unit)
                line.discount = discount
                disc_amnt += (line.quantity * line.price_unit) * discount / 100
            total = val1 + val2 - disc_amnt
            self.amount_discount = disc_amnt
            self.amount_tax = val2
            self.amount_total = total

    @api.onchange('discount_type', 'discount_rate')
    def supply_rate(self):
        for inv in self:
            if inv.discount_rate != 0:
                print("000000000000000000000000000000000", inv.discount_rate)
                for line in self.invoice_line:
                    line.test3 = inv.discount_rate
                amount = sum(line.price_subtotal for line in self.invoice_line)
                tax = sum(line.amount for line in self.tax_line)
                if inv.discount_type == 'percent':
                    self.compute_discount(inv.discount_rate)
                else:
                    total = 0.0
                    discount = 0.0
                    for line in inv.invoice_line:
                        total += (line.quantity * line.price_unit)
                    if inv.discount_rate != 0:
                        discount = (inv.discount_rate / total) * 100
                    self.compute_discount(discount)

    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        res = super(AccountInvoice, self)._prepare_refund(invoice, date, period_id,
                                                          description, journal_id)
        res.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return res

