from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, tools


class InvoiceHistory(models.Model):
    _inherit = 'account.invoice'

    invoices_id = fields.Many2one('account.invoice', 'Select Previous Invoice')
    period_id = fields.Many2one('account.period', 'Select Period')

    @api.multi
    def load(self):
        inv_obj = self.env['account.invoice'].browse(self.invoices_id.id)
        if inv_obj:
            print("yes")
        else:
            print("no")
        for rec in inv_obj:
            new_lines = []
            for line in rec.invoice_line:
                new_lines.append((0, 0, {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'medicine_name_subcat': line.medicine_name_subcat.id,
                    'medicine_name_packing': line.medicine_name_packing.id,
                    'product_of': line.product_of.id,
                    'medicine_grp': line.medicine_grp.id,
                    'batch_2': line.batch_2.id,
                    'hsn_code': line.hsn_code,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'discount': line.discount,
                    'price_subtotal': line.price_subtotal,
                    'invoice_line_tax_id4': line.invoice_line_tax_id4,
                    'amount_amount1': line.amount_amount1,
                    'amount_w_tax': line.amount_w_tax,
                    'manf_date': line.manf_date,
                    'expiry_date': line.expiry_date,
                    'medicine_rack': line.medicine_rack.id,

                }))

        self.write({'invoice_line': new_lines})


# ____________________________________________SUPPLIER DISCOUNTS________________________________________________________________________
class Discounts2(models.Model):
    _name = 'list.discount2'

    company = fields.Many2one('product.medicine.responsible', 'Company')
    # medicine_1 = fields.Many2one('product.product', string="Medicine")
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_grp1 = fields.Many2one('tax.combo.new', 'Group')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )  # discount calculation
    discount = fields.Float('Discount(%)')
    lists_id = fields.Many2one('supplier.discounts2', string='Set Discounts')


class Discounts(models.Model):
    _name = 'list.discount'

    company = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_grp1 = fields.Many2one('tax.combo.new', 'Group')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )  # discount calculation
    discount = fields.Float('Discount(%)')
    lists_id = fields.Many2one('supplier.discounts', string='Set Discounts')


class Discounts2(models.Model):
    _name = 'group.discount'

    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    medicine_grp = fields.Many2one('tax.combo.new', 'Group', )
    discount = fields.Float('Discount')
    expiry_months = fields.Integer('Expiry Months')
    lists_id = fields.Many2one('set.discount', string='Set Discount')
    inv_id = fields.Float("Inv.Id", compute="_get_inv_number")

    @api.model
    def create(self, vals):
        result = super(Discounts2, self).create(vals)
        print("++++++++++++++++++++++")
        for rec in result:
            print("---------------------------")
            vals = {
                'inv_id': result.env.context.get('active_id'),
                'medicine_name_subcat': rec.medicine_name_subcat.id,
                'medicine_grp': rec.medicine_grp.id,
                'discount': rec.discount,
                'expiry_months': rec.expiry_months,

            }
            self.env['group.discount.copy'].create(vals)
            print("created records..................")
            print("show id...",result.env.context.get('active_id'))
        return result

    @api.one
    def _get_inv_number(self):
        self.write({'inv_id': 7})

        # self.inv_id = self.env.context.get('active_id')

    # @api.onchange('medicine_grp')
    # def onchange_ref_id(self):
    #     for rec in self:
    #         rec.inv_id=self.active_id
    #         print("lllllllllllllllllllllllllllllll")


class DiscountsCopy(models.Model):
    _name = 'group.discount.copy'

    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    medicine_grp = fields.Many2one('tax.combo.new', 'Group', )
    discount = fields.Float('Discount')
    expiry_months = fields.Integer('Expiry Months')
    lists_id = fields.Many2one('set.discount', string='Set Discount')
    inv_id = fields.Float("Inv.Id")


class SupplierDiscounts1(models.Model):
    _name = 'supplier.discounts'
    _rec_name = 'supplier'

    supplier = fields.Many2one('res.partner', 'Supplier')
    lines = fields.One2many(
        comodel_name='list.discount',
        inverse_name='lists_id',
        string='Set Discounts',
        store=True,
    )


class SupplierDiscounts2(models.Model):
    _name = 'supplier.discounts2'
    _rec_name = 'supplier'

    supplier = fields.Many2one('res.partner', 'Supplier')
    lines = fields.One2many(
        comodel_name='list.discount2',
        inverse_name='lists_id',
        string='Set Discounts',
        store=True,
    )


class SetDiscount2(models.Model):
    _name = 'set.discount'

    lines = fields.One2many(
        comodel_name='group.discount',
        inverse_name='lists_id',
        string='Set Discounts',
        store=True,
    )
    ac_id = fields.Float('Active ID')
    test = fields.Many2one('res.partner', 'Test')

    @api.onchange('test')
    def onchange_ref_id(self):
        for rec in self:
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", self.env.context.get('active_id'))
            self.ac_id = self.env.context.get('active_id')

    @api.one
    def save_discount(self):
        pass
        # for lines in self.lines:
        #     self.env['group.discount'].create({
        #             'inv_id':self.env.context.get('active_id'),
        #             'medicine_grp':lines.medicine_grp.id,
        #             'medicine_name_subcat':lines.medicine_name_packing.id,
        #             'discount':lines.discount
        #
        #     })
        #
