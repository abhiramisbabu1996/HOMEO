from datetime import datetime, timedelta
from datetime import timedelta

# import models
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api, tools


class AccountAccountInherit(models.Model):
    _inherit = 'account.account'

    medical = fields.Boolean('Medical')


class ChequeTransactions(models.Model):
    _name = 'cheque.entry'
    _rec_name = 's_no'

    s_no = fields.Char('Serial Number', readonly=True, required=True, copy=False, default='New')
    name = fields.Many2one('res.partner', 'Name', required=1)
    # journal_id = fields.Many2one('account.journal', 'Journal')
    # account_id = fields.Many2one('account.account', 'Account')
    t_date = fields.Date('Date', required=1)
    cheque_no = fields.Char('Cheque Number')
    cheque_date = fields.Date('Cheque Date')
    deposit_date = fields.Date('Deposit Date')
    clearance_date = fields.Date('Clearance Date')
    cheque_amount = fields.Float('Cheque Amount', required=1)
    balance = fields.Float('Balance', compute="_get_balace_amt")
    bank = fields.Char('Bank')
    branch = fields.Char('Branch')
    ifsc = fields.Char('IFSC')
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted'), ('bounce', 'Bounced'), ]
                             , required=True, default='draft')
    invoice_ids = fields.Many2many('account.invoice', string="Select Invoice")

    @api.one
    @api.depends('cheque_amount')
    def _get_balace_amt(self):
        if self.state == 'post':
            self.balance = self.cheque_amount
        if self.state == 'bounce':
            self.balance = 0.0

    @api.model
    def create(self, vals):
        if vals.get('s_no', 'New') == 'New':
            vals['s_no'] = self.env['ir.sequence'].next_by_code(
                'cheque.entry.sequence') or 'New'
        result = super(ChequeTransactions, self).create(vals)
        return result

    @api.multi
    def post(self):
        for rec in self:
            rec.write({'state': 'post'})
            if rec.balance == 0:
                rec.balance = self.cheque_amount
            if rec.invoice_ids:
                new_debit = 0
                for item in rec.invoice_ids:
                    if item.state != 'paid':
                        new_debit = item.account_id.debit - item.amount_total
                        item.account_id.write({'debit': new_debit})
                        # print("99999999999999999999999999999999999",new_debit)
                        item.paid_bool = True
                        item.write({'state': 'paid'})

    @api.multi
    def bounce(self):
        for rec in self:
            rec.balance = 0
            rec.write({'state': 'bounce'})


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"
    Tax_of_pdt = fields.Char('Medicine Tax')
    Tax_of_pdt = fields.Many2many('account.tax',
                                  'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
                                  string='Taxes',
                                  domain=[('parent_id', '=', False), '|', ('active', '=', False),
                                          ('active', '=', True)])


class ProductVariantInherit(models.Model):
    _inherit = "product.product"

    # Tax_of_pdt = fields.Char('Medicine Tax')
    Tax_of_pdt = fields.Many2many('account.tax',
                                  'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
                                  string='Taxes',
                                  domain=[('parent_id', '=', False), '|', ('active', '=', False),
                                          ('active', '=', True)])


class AccountInvoiceRefgen(models.Model):
    _inherit = "account.invoice.line"


    discount2 = fields.Float("DISCOUNT2")
    discount3 = fields.Float("Dis2", )


    @api.model
    def create(self, vals):
        result = super(AccountInvoiceRefgen, self).create(vals)
        if result.partner_id.supplier == True:
            for inv_lines in result:
                for lines in inv_lines:
                    pdt_obj = self.env['product.product'].browse(lines.product_id.id)
                    if lines.expiry_date:
                        text = lines.expiry_date
                        x = datetime.strptime(text, '%Y-%m-%d')
                        exp_det = {

                            'expiry_date': lines.expiry_date,
                            'manf_date': lines.manf_date,
                            'product_id': lines.product_id.id,
                            'ref': pdt_obj.id,
                            'alert_date': x - relativedelta(months=6)
                        }
                        # self.env['stock.production.lot'].create(exp_det)
                        self.env['stock.production.lot']
                        print(exp_det)
                        pdt_obj_1 = self.env['product.template'].search([('default_code', '=', pdt_obj.default_code)])
                        testtt = lines.invoice_line_tax_id.name
                        print("lassttttttt", testtt)
                        # pdt_obj.Tax_of_pdt = lines.invoice_line_tax_id
                        # pdt_obj_1.Tax_of_pdt = lines.invoice_line_tax_id

                    else:
                        print("this medicine has no expiry and mfd")

        return result


class Batches(models.Model):
    _name = "med.batch"
    _rec_name = 'batch'

    batch = fields.Char('Batch')


# All Calculations
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    # CALCULATE CATEGORY DISCOUNT-CUSTOMER INVOICE
    @api.one
    @api.depends('discount', 'calc')
    def _compute_mass_discount(self):
        if self.invoice_id.discount_rate == 0:
            pass
        else:
            if self.discount ==0:
                discount_rate = self.invoice_id.discount_rate
                self.discount = discount_rate


    # CUSTOMER TAX CALCULATION
    @api.model
    @api.depends('amt_w_tax', 'invoice_line_tax_id4', 'price_subtotal', 'amount_amount1', 'price_unit', 'rate_amtc')
    def _compute_customer_tax(self):
        if self.partner_id.customer == True:

            for rec in self:
                if rec.rate_amtc == 0:
                        if rec.rate_amtc < rec.price_subtotal:
                            if rec.rate_amtc == 0:
                                # print("NORMAL TAX")
                                rate_amount = rec.price_subtotal
                                perce = rec.invoice_line_tax_id4
                                tax = rate_amount * (perce / 100)
                                rec.amt_tax = tax
                                total = rate_amount + tax
                                rec.amt_w_tax = total

                else:

                    print("DIFFERENT TAX")
                    perce = rec.invoice_line_tax_id4
                    new_rate = rec.rate_amtc
                    print("rate_amt...", new_rate)
                    tax = new_rate * (perce / 100)
                    print("tax.....", tax)
                    rec.amt_tax = tax
                    total = new_rate + tax
                    print("this total", total)
                    rec.amt_w_tax = total


    @api.one
    @api.depends('product_id', 'medicine_name_subcat', 'medicine_grp', 'medicine_name_subcat', 'discount2',
                 'price_unit',
                 'quantity', 'discount')
    def _compute_all(self):
        if self.partner_id.supplier == True:
            # FETCH DISCOUNT1
            for rec in self:
                flag = 0
                s_obj = self.env['supplier.discounts'].search([('supplier', '=', rec.partner_id.id)])
                if s_obj:
                    for lines in s_obj.lines:
                        if (lines.company.id == rec.product_of.id):
                            if (lines.medicine_1.id == rec.product_id.id):
                                if (lines.potency.id == rec.medicine_name_subcat.id):
                                    if (lines.medicine_grp1.id == rec.medicine_grp.id):
                                        if (lines.medicine_name_packing.id == rec.medicine_name_packing.id):
                                            rec.discount = lines.discount
                                            flag = 1
                        if flag == 1:
                            pass
                        else:
                            if ((lines.company.id == rec.product_of.id) and (
                                    lines.medicine_grp1.id == rec.medicine_grp.id) and (
                                    lines.medicine_1.id == None) and (
                                    lines.potency.id == rec.medicine_name_subcat.id) and (
                                    lines.medicine_name_packing.id == rec.medicine_name_packing.id)):
                                rec.discount = lines.discount
                            else:
                                if ((lines.company.id == rec.product_of.id) and (
                                        lines.medicine_grp1.id == rec.medicine_grp.id) and (
                                        lines.medicine_1.id == None) and (
                                        lines.potency.id == rec.medicine_name_subcat.id) and (
                                        lines.medicine_name_packing.id == None)):
                                    rec.discount = lines.discount
                                else:
                                    if ((lines.company.id == rec.product_of.id) and (
                                            lines.medicine_grp1.id == rec.medicine_grp.id) and (
                                            lines.medicine_1.id == None) and (
                                            lines.potency.id == None) and (
                                            lines.medicine_name_packing.id == rec.medicine_name_packing.id)):
                                        rec.discount = lines.discount
                                    else:
                                        if ((lines.company.id == rec.product_of.id) and (
                                                lines.medicine_grp1.id == rec.medicine_grp.id) and (
                                                lines.medicine_1.id == None) and (lines.potency.id == None) and (
                                                lines.medicine_name_packing.id == None)):
                                            rec.discount = lines.discount


            # FETCH EXTRA DDISCOUNT
            if self.medicine_grp:
                dis_obj = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                             (
                                                                 'medicine_name_subcat', '=',
                                                                 self.medicine_name_subcat.id),
                                                             ('medicine_name_packing', '=',
                                                              self.medicine_name_packing.id)])
                if dis_obj:
                    varia = dis_obj.discount
                    self.discount3 = dis_obj.discount
                    if dis_obj.expiry_months:
                        if self.manf_date:
                            text = self.manf_date
                            x = datetime.strptime(text, '%Y-%m-%d')
                            nextday_date = x + relativedelta(months=dis_obj.expiry_months)
                            cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                            # print("calculated date............", cal_date)
                            self.expiry_date = cal_date
                            # self.write({'expiry_date': cal_date})
                else:
                    dis_obj2 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                                  ('medicine_name_subcat', '=',
                                                                   self.medicine_name_subcat.id),
                                                                  ('medicine_name_packing', '=', None)])

                    if dis_obj2:
                        self.discount3 = dis_obj2.discount
                        if dis_obj2.expiry_months:
                            if self.manf_date:
                                text = self.manf_date
                                x = datetime.strptime(text, '%Y-%m-%d')
                                nextday_date = x + relativedelta(months=dis_obj2.expiry_months)
                                cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                self.expiry_date = cal_date
                                # self.write({'expiry_date': cal_date})
                    else:
                        dis_obj4 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                                      ('medicine_name_subcat', '=', None),
                                                                      ('medicine_name_packing', '=',
                                                                       self.medicine_name_packing.id)])
                        if dis_obj4:
                            self.discount3 = dis_obj4.discount
                            if dis_obj4.expiry_months:
                                if self.manf_date:
                                    text = self.manf_date
                                    x = datetime.strptime(text, '%Y-%m-%d')
                                    nextday_date = x + relativedelta(months=dis_obj4.expiry_months)
                                    cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                    self.expiry_date = cal_date
                                    # self.write({'expiry_date': cal_date})


                        else:
                            dis_obj3 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                                          ('medicine_name_subcat', '=', None),
                                                                          ('medicine_name_packing', '=', None)])
                            if dis_obj3:
                                self.discount3 = dis_obj3.discount
                                if dis_obj3.expiry_months:
                                    if self.manf_date:
                                        text = self.manf_date
                                        x = datetime.strptime(text, '%Y-%m-%d')
                                        nextday_date = x + relativedelta(months=dis_obj3.expiry_months)
                                        cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                        self.expiry_date = cal_date
                                        # self.write({'expiry_date': cal_date})

            # TAX CALCULATION AND SUBTOTAL WITH 2 DISCOUNTS IF THERE IS DISCOUNT1 AND DISCOUNT2
            if self.price_unit:
                # print("price unit exist")
                subtotal_wo_dis1 = self.price_unit * self.quantity
                if self.discount:
                    # print("first discount exist")
                    if self.discount3:
                        # print("condition-extra discount")
                        discount1_amount = subtotal_wo_dis1 * (self.discount / 100)
                        item = self.invoice_line_tax_id4
                        subtotal_with_dis1 = subtotal_wo_dis1 - discount1_amount
                        tax_amount = subtotal_with_dis1 * (item / 100)
                        # self.price_subtotal = subtotal_with_dis1
                        self.amount_amount1 = tax_amount
                        # self.amount_w_tax = subtotal_with_dis1 + tax_amount
                        dis2_amt = subtotal_with_dis1 * (self.discount3 / 100)
                        subtotal_with_dis2 = subtotal_with_dis1 - dis2_amt
                        # print("1st round of calculation")
                        self.price_subtotal = subtotal_with_dis2
                        self.amount_w_tax = subtotal_with_dis2 + tax_amount
                        self.grand_total = subtotal_with_dis2 + tax_amount
                        # print("price_subtotal", subtotal_with_dis2)
                        # print("total", subtotal_with_dis2 + tax_amount)
                        # print("extra dis", dis2_amt)
                        self.price_subtotal = self.amount_w_tax - self.amount_amount1
                        self.dis1 = discount1_amount
                        self.dis2 = dis2_amt


                    else:
                        discount1_amount = subtotal_wo_dis1 * (self.discount / 100)
                        item = self.invoice_line_tax_id4
                        subtotal_with_dis1 = subtotal_wo_dis1 - discount1_amount
                        tax_amount = subtotal_with_dis1 * (item / 100)
                        self.price_subtotal = subtotal_with_dis1
                        self.amount_amount1 = tax_amount
                        self.amount_w_tax = subtotal_with_dis1 + tax_amount
                        self.grand_total = subtotal_with_dis1 + tax_amount
                        self.dis1 = discount1_amount
                else:
                    item = self.invoice_line_tax_id4
                    tax_amount = subtotal_wo_dis1 * (item / 100)
                    self.amount_amount1 = tax_amount
                    self.amount_w_tax = subtotal_wo_dis1 + tax_amount
                    self.grand_total = subtotal_wo_dis1 + tax_amount
        if self.partner_id.supplier == True:
            self.rate_amt = self.amount_w_tax - self.amount_amount1
            # self.grand_total = self.amount_w_tax - self.amount_amount1
            # print("finallyyyyy", self.rate_amt)

    # CUSTOMER EXTRA DISCOUNT

    @api.one
    @api.depends('product_id', 'medicine_name_subcat', 'medicine_grp', 'medicine_name_subcat', 'discount3',
                 'price_unit',
                 'quantity','amt_w_tax')
    def _compute_cus_ex_discount(self):

        percentage = 0
        if self.partner_id.customer == True:
            if self.rate_amtc:
                for rec in self:
                    # print("got")
                    new_rate = rec.rate_amtc
                    percentage = (new_rate / rec.price_subtotal) * 100
                    rec.new_disc = percentage




    medicine_rack = fields.Many2one('product.medicine.types', 'Rack')
    product_of = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Pack', )

    # medicine_grp = fields.Many2one('product.medicine.group', 'GROUP',compute='_compute_taxes',readonly="0")
    medicine_grp = fields.Many2one('tax.combo.new', 'Grp', )

    # medicine_group = fields.Char('Group', related="product_id.medicine_group")
    batch = fields.Char("BATCH", related="product_id.batch")
    batch_2 = fields.Many2one('med.batch', "Batch", )
    # test = fields.Float('Test', compute="_get_sup_discount_amt")
    test = fields.Float('Test')
    # test2 = fields.Float('Test2',compute="_get_sup_discount2")
    test2 = fields.Float('Test2')
    test3 = fields.Float('Test3', compute="_compute_all")
    expiry_date = fields.Date(string='Exp')
    manf_date = fields.Date(string='Mfd')
    alert_date = fields.Date(string='Alert Date')
    avail_qty = fields.Float(string='Stock Total', related="product_id.qty_available")
    hsn_code = fields.Char('Hsn')
    invoice_line_tax_id3 = fields.Many2one('tax.combo', string='Gst')
    invoice_line_tax_id4 = fields.Float(string='Tax')
    rack_qty = fields.Float(string="stock")
    rate_amt = fields.Float(string="Rate")
    rate_amtc = fields.Float(string="N-rate")
    dis1 = fields.Float('discount 1')
    dis2 = fields.Float('discount 2')
    grand_total = fields.Float('Grand Total')
    calc = fields.Float('Cal', compute="_compute_mass_discount",)
    calc2 = fields.Float('Cal2',)
    calc3 = fields.Float('Cal3', )
    new_disc = fields.Float('Disc2', compute="_compute_cus_ex_discount")
    amt_tax = fields.Float('Tax_amt')
    amt_w_tax = fields.Float('Total',compute="_compute_customer_tax")
    doctor_name = fields.Many2one('res.partner','Doctor Name')
    address_new = fields.Text('Address')



    @api.onchange('medicine_name_subcat')
    def onchange_potency_id(self):
        for rec in self:
            return {'domain': {'medicine_grp': [('medicine_name_subcat1', '=', rec.medicine_name_subcat.id)]}}

    @api.onchange('batch_2')
    def onchange_batch_id(self):
        for rec in self:
            if rec.product_id and rec.medicine_name_subcat:
                if rec.batch_2:
                    rack_obj = self.env['med.rack'].search([])
                    if rack_obj:
                        for item in rack_obj:
                            for lines in item.racks:
                                if (lines.product_id.id == rec.product_id.id):
                                    if (lines.potency.id == rec.medicine_name_subcat.id):
                                        if (lines.batch_2.id == rec.batch_2.id):
                                            if (lines.company.id == rec.product_of.id):
                                                if (lines.mrp == rec.price_unit):
                                                    if (lines.medicine_name_packing.id == rec.medicine_name_packing.id):
                                                        rec.medicine_rack = item.rack.id
                                                        rec.rack_qty = lines.qty
                                                        rec.manf_date = lines.manf_date
                                                        rec.expiry_date = lines.expiry_date

    # tax selection-based on group and potency
    @api.onchange('medicine_grp')
    def onchange_group_id(self):
        for rec in self:
            if self.medicine_grp.id:
                # print("medicine group exist")
                grp_obj = self.env['product.medicine.group'].search([])
                flag = 0
                for items in grp_obj:
                    # print("inside for loop")
                    for lines in items.potency_med_ids:
                        # print("1")
                        if (rec.product_id.id == lines.medicine.id):
                            # print("2")

                            if (rec.medicine_name_subcat.id == lines.potency.id):
                                # print("3")
                                if (rec.product_of.id == lines.company.id):
                                    # print("4")
                                    rec.hsn_code = lines.hsn
                                    rec.invoice_line_tax_id4 = lines.tax
                                    rec.product_of = lines.company
                                    # print("print tax", lines.tax)
                                    flag = 1
                if flag == 1:
                    # print("flag is 0")
                    pass
                else:
                    grp_obj = self.env['tax.combo.new'].browse(rec.medicine_grp.id)
                    if grp_obj.hsn and grp_obj.tax_rate:
                        # print("exist both")
                        self.hsn_code = grp_obj.hsn
                        self.invoice_line_tax_id4 = grp_obj.tax_rate


# GROUPS AND RESTRICTIONS

class ResUsers(models.Model):
    _inherit = 'res.users'

    hide_menu_access_ids = fields.Many2many('ir.ui.menu', 'ir_ui_hide_menu_rel', 'uid', 'menu_id',
                                            string='Hide Access Menu')


class Menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        menus = super(Menu, self)._visible_menu_ids(debug)
        if self.env.user.hide_menu_access_ids and not self.env.user.has_group('base.group_system'):
            for rec in self.env.user.hide_menu_access_ids:
                menus.discard(rec.id)
            return menus
        return menus


class InvoiceStockMove(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def add_items(self):
        pass

    number2 = fields.Char()
    duplicate = fields.Boolean()
    seq = fields.Integer()
    holding_invoice = fields.Boolean()
    packing_slip = fields.Boolean()

    @api.multi
    def invoice_open(self):
        self.ensure_one()
        # Search for record belonging to the current staff
        record = self.env['hiworth.invoice'].search([('origin', '=', self.name)])

        context = self._context.copy()
        context['type2'] = 'out'
        # context['default_name'] = self.id
        if record:
            res_id = record[0].id
        else:
            res_id = False
        # Return action to open the form view
        return {
            'name': 'Invoice view',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': 'hiworth.invoice',
            'view_id': 'hiworth_invoice_form',
            'type': 'ir.actions.act_window',
            'res_id': res_id,
            'context': context,
        }

    @api.model
    def create(self, vals):
        # self.button_reset_taxes()
        if 'duplicate' in self._context:
            if self._context['duplicate']:
                vals.update({'number2': self.browse(self._context['inv_id']).number2, 'duplicate': True})
        result = super(InvoiceStockMove, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        if 'internal_number' in vals:
            if self.duplicate:
                vals['internal_number'] = self.number2
                vals['number2'] = self.number2
            else:
                latest_ids = self.search([('duplicate', '=', False)], limit=2, order='id desc').ids
                latest = self.search([('id', 'in', latest_ids)], limit=1, order='id asc')
                if latest.number2:
                    last_index = int(latest.number2.split('/')[2]) + 1
                    if len(str(last_index)) < 4:
                        last_index = (4 - len(str(last_index))) * '0' + str(last_index)
                    index = latest.number2.split('/')
                    vals['number2'] = index[0] + "/" + index[1] + "/" + str(last_index)
                    vals['seq'] = int(latest.seq) + 1
                else:
                    vals['seq'] = 1
                    vals['number2'] = "SAJ/2022/0001"
                vals['internal_number'] = vals['number2']
        result = super(InvoiceStockMove, self).write(vals)
        # add custom codes here
        return result

    def copy(self, cr, uid, id, default=None, context=None):
        context.update({'duplicate': True, 'inv_id': id})
        result = super(InvoiceStockMove, self).copy(cr, uid, id, default, context)
        return result

    @api.multi
    def action_discount1(self):
        return {
            'name': 'group discount',
            'view_type': 'form',
            'view_mode': 'tree',
            'domain': [('inv_id', '=', self.id)],
            'res_model': 'group.discount.copy',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id},

        }

    @api.multi
    def action_discount(self):
        print("record id", self.id)
        prev_rec = self.env['group.discount'].search([])
        if prev_rec:
            for rec in prev_rec:
                rec.unlink()

        return {
            'name': 'group discount',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'group.discount',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id},

        }

