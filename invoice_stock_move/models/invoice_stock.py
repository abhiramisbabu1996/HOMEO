# from odoo.exceptions import UserError
# from odoo import models, fields, api, _
# from odoo.tools.safe_eval import safe_eval
from openerp.exceptions import Warning as UserError
from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.tools import safe_eval
from openerp.exceptions import except_orm
from openerp.exceptions import Warning as UserError


class MedicineTypes(models.Model):
    _name = 'customer.title'
    _rec_name = 'cus_type'

    cus_type = fields.Char(string="Customer Type")


class CusArea(models.Model):
    _name = 'customer.area'
    _rec_name = 'cus_area'

    cus_area = fields.Char(string="Customer Area")


class CustomerTitle(models.Model):
    _inherit = 'res.partner'

    cus_title = fields.Many2one('customer.title', "Customer Type")
    cust_area = fields.Many2one('customer.area', "Customer Area")


class MeDRacks(models.Model):
    _name = 'rack.batch'

    medicine = fields.Many2one('product.template', string="Medicine")
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    batch = fields.Char('Batch')
    batch_2 = fields.Many2one('med.batch', "Batch")
    rack = fields.Many2one('product.medicine.types', 'Rack')
    qty = fields.Float('Stock')
    racks_id = fields.Many2one('med.rack', string='Racks')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    mrp = fields.Float('Mrp')
    expiry_date = fields.Date(string='EXP')

    manf_date = fields.Date(string='MFD')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )


class NewStockEntry(models.Model):
    _name = 'entry.stock'
    _rec_name = 's_no'

    expiry_date = fields.Date(string='Expiry Date')
    manf_date = fields.Date(string='Manufacturing Date')
    alert_date = fields.Date(string='Alert Date')
    s_no = fields.Char('Serial Number', readonly=True, required=True, copy=False, default='New')
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    batch = fields.Char('Batch')
    batch_2 = fields.Many2one('med.batch', "Batch")
    rack = fields.Many2one('product.medicine.types', 'Rack')
    qty = fields.Float('Stock')
    racks_id = fields.Many2one('med.rack', string='Racks')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    mrp = fields.Float('Mrp')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    racks_id = fields.Many2one('med.rack', string='Racks')
    medicine_grp = fields.Many2one('product.medicine.group', 'Group')
    medicine_grp1 = fields.Many2one('tax.combo.new', 'Group')
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    hsn_code = fields.Char('HSN(CODE)')
    invoice_line_tax_id4 = fields.Float(string='GST(%)')
    discount = fields.Float(string='Discount')
    price_subtotal = fields.Float(string='Price Subtotal')
    amount_amount = fields.Float()
    qty_received = fields.Float('Qty Trasfer')
    amount_w_tax = fields.Float()
    custom_qty = fields.Integer()
    invoice_line_id = fields.Many2one('account.invoice.line')

    @api.model
    def create(self, vals):
        if vals.get('s_no', 'New') == 'New':
            vals['s_no'] = self.env['ir.sequence'].next_by_code(
                'stock.entry.sequence') or 'New'
        result = super(NewStockEntry, self).create(vals)
        return result

    @api.multi
    def call_function(self):
        # print("Active id",self.env.context.get('active_id'))
        cus_invoice = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        if cus_invoice:
            new_lines = []
            for rec in self:
                new_lines.append((0, 0, {
                    'name': rec.medicine_1.name,
                    'product_id': rec.medicine_1.id,
                    'medicine_name_subcat': rec.potency.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'product_of': rec.company.id,
                    'medicine_grp': rec.medicine_grp1.id,
                    'batch_2': rec.batch_2.id,
                    'hsn_code': rec.hsn_code,
                    'price_unit': rec.mrp,
                    'discount': rec.discount,
                    'manf_date': rec.manf_date,
                    'expiry_date': rec.expiry_date,
                    'medicine_rack': rec.rack.id,
                    'invoice_line_tax_id4': rec.invoice_line_tax_id4,
                    'rack_qty': rec.qty,

                }))
            cus_invoice.write({'invoice_line': new_lines})
        else:
            pass


class FindRackMed(models.Model):
    _name = 'med.rack'
    _rec_name = 'rack'

    medicine = fields.Many2one('product.template', string="Medicine")
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    rack = fields.Many2one('product.medicine.types', 'Rack')
    qty = fields.Float('Stock Qty in Rack')
    # racks = fields.One2many(
    #     comodel_name='rack.batch',
    #     inverse_name='racks_id',
    #     string='Medicines',
    #     store=True,
    # )
    racks = fields.One2many(
        comodel_name='stock.production.lot',
        inverse_name='racks_id',
        string='Medicines',
        store=True,
    )

    @api.onchange('medicine')
    def do_find_med(self):
        print("product template id", self.medicine)
        print("product name", self.medicine.name)
        # med_obj = self.env['product.'].search([('product_id','=',self.medicine.id)])
        self.rack = self.medicine.medicine_rack
        self.qty = self.medicine.qty_available


class InvoiceStockMovewrite(models.Model):
    _inherit = 'account.invoice'

    # search_items = fields.Many2many('entry.stock')
    search_items = fields.Char('.')

    # @api.multi
    # def write(self, vals):
    #     # print("abcdefghijklmnopqrstuvwxyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    #     result = super(InvoiceStockMovewrite, self).write(vals)
    #     tax_total = 0
    #     for lines in self.invoice_line:
    #         print("hiiiiiiiiiiiiiiiiii")
    #         if lines.amount_amount1:
    #             tax_total = tax_total + lines.amount_amount1
    #
    #     # result.write({'amount_tax':tax_total})
    #     print("rrrrrrrrrrrrrrrrrrr",self.amount_tax)
    #     print("88888888888888888888888",tax_total)
    #     # self.amount_tax = tax_total
    #     #
    #
    #     # vals['amount_tax'] = tax_total
    #     print("[[[[[[[[[[[[[[[[[[[[[[[[",vals['amount_tax'])
    #     # vals['amount_total'] = vals['amount_total'] + tax_total
    #     # result.amount_total = result.amount_total + tax_total
    #     # if result.type == 'in_invoice':
    #     #     result.action_stock_receive()
    #     return result


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    stock_entry_id = fields.Many2one('entry.stock')

    @api.model
    def create(self,vals):
        result = super(InvoiceLine, self).create(vals)
        if result.invoice_id.type == 'in_invoice':
            vals = {
                'expiry_date': result.expiry_date,
                'manf_date': result.manf_date,
                'company': result.product_of.id,
                'medicine_1': result.product_id.id,
                'potency': result.medicine_name_subcat.id,
                'medicine_name_packing': result.medicine_name_packing.id,
                'medicine_grp1': result.medicine_grp.id,
                'batch_2': result.batch_2.id,
                'mrp': result.price_unit,
                'qty': result.quantity,
                'rack': result.medicine_rack.id,
                'hsn_code': result.hsn_code,
                'discount': result.discount,
                'invoice_line_tax_id4': result.invoice_line_tax_id4,
            }
            stock_entry = self.env['entry.stock'].create(vals)
            result.stock_entry_id = stock_entry.id
        return result

    #
    #
    #     result = super(InvoiceLine, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(InvoiceLine, self).write(vals)
        if self.invoice_id.type == 'in_invoice':
            vals = {
                'expiry_date': self.expiry_date,
                'manf_date': self.manf_date,
                'company': self.product_of.id,
                'medicine_1': self.product_id.id,
                'potency': self.medicine_name_subcat.id,
                'medicine_name_packing': self.medicine_name_packing.id,
                'medicine_grp1': self.medicine_grp.id,
                'batch_2': self.batch_2.id,
                'mrp': self.price_unit,
                'qty': self.quantity,
                'rack': self.medicine_rack.id,
                'hsn_code': self.hsn_code,
                'discount': self.discount,
                'invoice_line_tax_id4': self.invoice_line_tax_id4,
            }
            result = self.stock_entry_id.update(vals)
        return res



# UPDATE TAX BUTTON
class InvoiceStockMove(models.Model):
    _inherit = 'account.invoice'


    # TAX UPDATION IN SAVE BUTTON
    # @api.model
    # def create(self, vals):
    #     # print("abcdefghijklmnopqrstuvwxyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    #     result = super(InvoiceStockMove, self).create(vals)
    #     tax_total = 0
    #     for lines in result.invoice_line:
    #         if lines.amount_amount1:
    #             tax_total = tax_total + lines.amount_amount1
    #     result.amount_tax = tax_total
    #     result.amount_total = result.amount_total + tax_total
    #     if not result.holding_invoice or not result.packing_slip:
    #         if result.type != 'in_invoice':
                # if result.b2c:
                #     result.state = 'paid'
        # return result

    # @api.multi
    # def write(self, vals):
        # if self.type == 'in_invoice':
        #     if vals.get('invoice_line'):
        #         for rec in vals.get('invoice_line'):
        #             if rec[2] and rec[1] == False:
        #                 line = rec[2]
        #                 vals = {
        #                     'expiry_date': line['expiry_date'],
        #                     'manf_date': line['manf_date'],
        #                     'company': line['product_of'],
        #                     'medicine_1': line['product_id'],
        #                     'potency': line['medicine_name_subcat'],
        #                     'medicine_name_packing': line['medicine_name_packing'],
        #                     'medicine_grp1': line['medicine_grp'],
        #                     'batch_2': line['batch_2'],
        #                     'mrp': line['price_unit'],
        #                     'qty': line['quantity'],
        #                     'rack': line['medicine_rack'],
        #                     # 'hsn_code': line['hsn_code'],
        #                     'discount': line['discount'],
        #                     'invoice_line_tax_id4': line['invoice_line_tax_id4'],
        #                 }
        #                 stock_entry = self.env['entry.stock'].create(vals)
        #                 vals.update({'stock_entry_id': stock_entry.id})
        # res = super(InvoiceStockMove, self).write(vals)
        # if self.type == 'in_invoice':
            # if vals.get('invoice_line'):
            #     for rec in vals.get('invoice_line'):
            #         if rec[2] and rec[1]:
            #             line = rec[2]
            #             vals = {
            #                 'expiry_date': line.expiry_date,
            #                 'manf_date': line.manf_date,
            #                 'company': line.product_of.id,
            #                 'medicine_1': line.product_id.id,
            #                 'potency': line.medicine_name_subcat.id,
            #                 'medicine_name_packing': line.medicine_name_packing.id,
            #                 'medicine_grp1': line.medicine_grp.id,
            #                 'batch_2': line.batch_2.id,
            #                 'mrp': line.price_unit,
            #                 'qty': line.quantity,
            #                 'rack': line.medicine_rack.id,
            #                 # 'hsn_code': line.hsn_code,
            #                 'discount': line.discount,
            #                 'invoice_line_tax_id4': line.invoice_line_tax_id4,
            #             }
            #             line.stock_entry_id.update(vals)
        # return res

    @api.multi
    def button_reset_taxes(self):
        res = super(InvoiceStockMove, self).button_reset_taxes()
        # add custom codes here
        tax_total = 0
        for lines in self.invoice_line:
            if lines.amount_amount1:
                tax_total = tax_total + lines.amount_amount1
        self.amount_tax = tax_total
        self.amount_total = self.amount_total + tax_total
        return res

    # @api.one
    # @api.depends('invoice_line')
    # def _compute_total_tax_amount(self):
    #     tax_total = 0
    #     for lines in self.invoice_line:
    #         tax_total = tax_total+lines.amount_amount
    #     self.amount_tax = tax_total
    #
    #
    #     total_amt = self.quantity * self.price_unit
    #     for item in self.invoice_line_tax_id3:
    #         self.amount_amount = (total_amt * item.tax_rate) / 100

    cus_title_1 = fields.Many2one('customer.title', "Customer Type", related="partner_id.cus_title")
    cust_area = fields.Many2one('customer.area', "Customer Area", related="partner_id.cust_area")
    paid_bool = fields.Boolean('Invoice Paid?')
    pay_mode = fields.Selection([('cash', 'Cash'), ('credit', 'Credit'), ], 'Payment Mode', default='credit')

    # amount_tax = fields.Float(compute="_compute_total_tax_amount",string='Tax Amount')

    # @api.model
    # def create(self, vals):
    #     result = super(InvoiceStockMove, self).create(vals)
    #     print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    #
    #     return result

    @api.model
    def _default_picking_receive(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)], limit=1)
        if not types:
            types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return types[:1]

    @api.model
    def _default_picking_transfer(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)], limit=1)
        if not types:
            types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
        return types[:4]

    picking_count = fields.Integer(string="Count")
    invoice_picking_id = fields.Many2one('stock.picking', string="Picking Id")
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', required=True,
                                      default=_default_picking_receive,
                                      help="This will determine picking type of incoming shipment")
    picking_transfer_id = fields.Many2one('stock.picking.type', 'Deliver To', required=True,
                                          default=_default_picking_transfer,
                                          help="This will determine picking type of outgoing shipment")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('proforma', 'Pro-forma'),
        ('proforma2', 'Pro-forma'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
        ('done', 'Received'),
    ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False)

    @api.multi
    def action_stock_receive(self):
        # for line in self.invoice_line:
            # vals = {
            #     'expiry_date': line.expiry_date,
            #     'manf_date': line.manf_date,
            #     'company': line.product_of.id,
            #     'medicine_1': line.product_id.id,
            #     'potency': line.medicine_name_subcat.id,
            #     'medicine_name_packing': line.medicine_name_packing.id,
            #     'medicine_grp1': line.medicine_grp.id,
            #     'batch_2': line.batch_2.id,
            #     'mrp': line.price_unit,
            #     'qty': line.quantity,
            #     'rack': line.medicine_rack.id,
            ##     'hsn_code': line.hsn_code,
            #     'discount': line.discount,
            #     'invoice_line_tax_id4': line.invoice_line_tax_id4,
            # }
            # self.env['entry.stock'].create(vals)

        # CODE FOR CREATING CUSTOMMODEL RECORDS FOR RECEIVED MEDICINES
        # self.env['stock.pick'].create({'product_id': line.product_id,
        #                                'product_uom_qty': line.product_uom_qty,
        #                                'date': line.date})
        #
        for line in self.invoice_line:
            self.env['stock.pick'].create({
                'partner_id': self.partner_id.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'date': self.date_invoice,
                'date_exp': line.expiry_date})

        for order in self:
            if not order.invoice_line:
                pass
                # raise UserError(_('Please create some invoice lines.'))
            if not self.number:
                pass
                # raise UserError(_('Please Validate invoice.'))
            if not self.invoice_picking_id:
                pick = {
                    'picking_type_id': self.picking_type_id.id,
                    'partner_id': self.partner_id.id,
                    'origin': self.number,
                    'location_dest_id': self.picking_type_id.default_location_dest_id.id,
                    'location_id': self.partner_id.property_stock_supplier.id
                }
                picking = self.env['stock.picking'].create(pick)
                self.invoice_picking_id = picking.id
                self.picking_count = len(picking)
                moves = order.invoice_line.filtered(
                    lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves(picking)
                move_ids = moves.action_confirm()
                move_ids = moves.action_assign()
                move_ids = moves.action_done()

    @api.multi
    def action_stock_transfer(self):
        for line in self.invoice_line:
            self.env['stock.transfer'].create({
                'partner_id': self.partner_id.id,
                'title': self.cus_title_1.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'date': self.date_invoice})

            if line.rack_qty:

                obj = self.env['entry.stock'].search([('rack', '=', line.medicine_rack.id)])
                for lines in obj:
                    if (lines.medicine_1.id == line.product_id.id):
                        if (lines.potency.id == line.medicine_name_subcat.id):
                            if (lines.batch_2.id == line.batch_2.id):
                                old_qty = lines.qty
                                new_qty = old_qty - line.quantity
                                lines.write({
                                    'qty': new_qty,
                                })

        for order in self:
            if not order.invoice_line:
                pass
                # raise UserError(_('Please create some invoice lines.'))
            if not self.number:
                pass
                # raise UserError(_('Please Validate invoice.'))
            if not self.invoice_picking_id:
                pick = {
                    'picking_type_id': self.picking_transfer_id.id,
                    'partner_id': self.partner_id.id,
                    'origin': self.number,
                    'location_dest_id': self.partner_id.property_stock_customer.id,
                    'location_id': self.picking_transfer_id.default_location_src_id.id
                }
                picking = self.env['stock.picking'].create(pick)
                self.invoice_picking_id = picking.id
                self.picking_count = len(picking)
                moves = order.invoice_line.filtered(
                    lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves_transfer(picking)
                move_ids = moves.action_confirm()
                move_ids = moves.action_assign()
                move_ids = moves.action_done()

    @api.multi
    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_ready')
        result = action.read()[0]
        result.pop('id', None)
        result['context'] = {}
        result['domain'] = [('id', '=', self.invoice_picking_id.id)]
        pick_ids = sum([self.invoice_picking_id.id])
        if pick_ids:
            res = self.env.ref('stock.view_picking_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = pick_ids or False
        return result

    @api.multi
    def invoice_validate(self):
        if self.type == 'in_invoice':
            self.action_stock_receive()
        if self.type != 'in_invoice':
            self.action_stock_transfer()
        return self.write({'state': 'open'})


###############################################TAXXXXXXX###################################################3

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    # @api.one
    # @api.depends('price_unit', 'quantity', 'invoice_line_tax_id3', 'invoice_line_tax_id4', 'price_subtotal')
    # def _compute_amount_amount(self):
    #     # total_amt = self.quantity * self.price_unit
    #     if self.partner_id.customer == True:
    #         total_amt = self.price_subtotal
    #         item = self.invoice_line_tax_id4
    #         self.amount_amount1 = (total_amt * item) / 100

    # @api.one
    # @api.depends('price_unit', 'quantity', 'invoice_line_tax_id3', 'invoice_line_tax_id4', 'price_subtotal', 'discount',
    #              'discount2')
    # def _compute_amount_with_tax(self):
    #     if self.partner_id.customer == True:
    #         total_amt = self.price_subtotal
    #         item = self.invoice_line_tax_id4
    #         tax_amount = (total_amt * item) / 100
    #         self.amount_w_tax = tax_amount + total_amt
    #
    #     if self.partner_id.supplier == True:
    #         if self.discount3:
    #             if self.discount:
    #                 total_amt = self.price_subtotal
    #                 qty = self.quantity
    #                 mrp = self.price_unit
    #                 total_without_dis = mrp * qty
    #                 discount1_amount = total_without_dis * (self.discount / 100)
    #                 price_subtotal1 = total_without_dis - discount1_amount
    #                 print("((((((((((((((((((((((((((((((((((((((", price_subtotal1)
    #                 item = self.invoice_line_tax_id4
    #                 tax_amount = price_subtotal1 * (item / 100)
    #                 print("tax amount", tax_amount)
    #                 self.amount_w_tax = tax_amount + total_amt
    #                 self.amount_amount1 = tax_amount
    #         else:
    #             total_amt = self.price_subtotal
    #             item = self.invoice_line_tax_id4
    #             tax_amount = (total_amt * item) / 100
    #             self.amount_w_tax = tax_amount + total_amt
    #             self.amount_amount1 = tax_amount


class SupplierInvoiceLineTax(models.Model):
    _inherit = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    # amount_amount = fields.Float('TAX_AMOUNT', compute="_compute_amount_amount")
    amount_amount = fields.Float('TAX_AMOUNT')
    amount_amount1 = fields.Float('Tax_amt', )
    # amount_w_tax = fields.Float('TOTAL_AMT', compute="_compute_amount_with_tax")
    amount_w_tax = fields.Float('Total_amt')

    # @api.onchange('product_id')
    # def get_pack_details(self):
    #     pack_id = self.env['product.product'].search([("id", 'in', self.product_id.id)])
    #     self.update({'invoice_line_tax_id': pack_id.Tax_of_pdt})


###########################################################################################################

class SupplierInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    invoice_line_tax_id = fields.Many2many('account.tax',
                                           'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
                                           string='Taxes', related="product_id.Tax_of_pdt",
                                           domain=[('parent_id', '=', False), '|', ('active', '=', False),
                                                   ('active', '=', True)])

    @api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            price_unit = line.price_unit
            template = {
                'name': line.name or '',
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'location_id': line.invoice_id.partner_id.property_stock_supplier.id,
                'location_dest_id': picking.picking_type_id.default_location_dest_id.id,
                'picking_id': picking.id,
                'move_dest_id': False,
                'state': 'draft',
                'company_id': line.invoice_id.company_id.id,
                'price_unit': price_unit,
                'picking_type_id': picking.picking_type_id.id,
                'procurement_id': False,
                'route_ids': 1 and [
                    (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
                'warehouse_id': picking.picking_type_id.warehouse_id.id,
            }
            diff_quantity = line.quantity
            tmp = template.copy()
            tmp.update({
                'product_uom_qty': diff_quantity,
            })
            template['product_uom_qty'] = diff_quantity
            done += moves.create(template)
        return done

    def _create_stock_moves_transfer(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            price_unit = line.price_unit
            template = {
                'name': line.name or '',
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'location_id': picking.picking_type_id.default_location_src_id.id,
                'location_dest_id': line.invoice_id.partner_id.property_stock_customer.id,
                'picking_id': picking.id,
                'move_dest_id': False,
                'state': 'draft',
                'company_id': line.invoice_id.company_id.id,
                'price_unit': price_unit,
                'picking_type_id': picking.picking_type_id.id,
                'procurement_id': False,
                'route_ids': 1 and [
                    (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
                'warehouse_id': picking.picking_type_id.warehouse_id.id,
            }
            diff_quantity = line.quantity
            tmp = template.copy()
            tmp.update({
                'product_uom_qty': diff_quantity,
            })
            template['product_uom_qty'] = diff_quantity
            done += moves.create(template)
        return done

    # @api.onchange('product_id')
    # def do_stuff(self):
    #     print("we are hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    #     self.invoice_line_tax_id = self.product_id.Tax_of_pdt


class AccountInvoiceRefund(models.TransientModel):
    _inherit = 'account.invoice.refund'

    @api.model
    def compute_refund(self, mode='refund'):
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        inv_obj = self.env['account.invoice']
        inv_tax_obj = self.env['account.invoice.tax']
        inv_line_obj = self.env['account.invoice.line']
        context = dict(self._context or {})
        xml_id = False

        for form in self:
            created_inv = []
            date = False
            description = False
            for inv in inv_obj.browse(context.get('active_ids')):
                if inv.state in ['draft', 'proforma2', 'cancel']:
                    pass
                    # raise UserError(_('Cannot refund draft/proforma/cancelled invoice.'))
                if inv.reconciled and mode in ('cancel', 'modify'):
                    pass
                    # raise UserError(_(
                    #     'Cannot refund invoice which is already reconciled, invoice should be unreconciled first. You can only refund this invoice.'))

                date = form.date or False
                description = form.description or inv.name
                refund = inv.refund(form.date_invoice, date, description, inv.journal_id.id)

                created_inv.append(refund.id)
                if inv.picking_transfer_id.code == 'outgoing':
                    data = self.env['stock.picking.type'].search(
                        [('warehouse_id.company_id', '=', company_id), ('code', '=', 'incoming')], limit=1)
                    refund.picking_transfer_id = data.id
                if inv.picking_type_id.code == 'incoming':
                    data = self.env['stock.picking.type'].search(
                        [('warehouse_id.company_id', '=', company_id), ('code', '=', 'outgoing')], limit=1)
                    refund.picking_type_id = data.id
                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_ids
                    to_reconcile_ids = {}
                    to_reconcile_lines = self.env['account.move.line']
                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_lines += line
                            to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
                        if line.reconciled:
                            line.remove_move_reconcile()
                    refund.action_invoice_open()
                    for tmpline in refund.move_id.line_ids:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_lines += tmpline
                    to_reconcile_lines.filtered(lambda l: l.reconciled == False).reconcile()
                    if mode == 'modify':
                        invoice = inv.read(inv_obj._get_refund_modify_read_fields())
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(invoice['invoice_line'])
                        invoice_lines = inv_obj.with_context(mode='modify')._refund_cleanup_lines(invoice_lines)
                        tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
                        tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': form.date_invoice,
                            'state': 'draft',
                            'number': False,
                            'invoice_line': invoice_lines,
                            'tax_line_ids': tax_lines,
                            'date': date,
                            'origin': inv.origin,
                            'fiscal_position_id': inv.fiscal_position_id.id,
                        })
                        for field in inv_obj._get_refund_common_fields():
                            if inv_obj._fields[field].type == 'many2one':
                                invoice[field] = invoice[field] and invoice[field][0]
                            else:
                                invoice[field] = invoice[field] or False
                        inv_refund = inv_obj.create(invoice)
                        if inv_refund.payment_term_id.id:
                            inv_refund._onchange_payment_term_date_invoice()
                        created_inv.append(inv_refund.id)
                xml_id = (inv.type in ['out_refund', 'out_invoice']) and 'action_invoice_tree1' or \
                         (inv.type in ['in_refund', 'in_invoice']) and 'action_invoice_tree2'
                # Put the reason in the chatter
                subject = _("Invoice refund")
                body = description
                refund.message_post(body=body, subject=subject)
        if xml_id:
            result = self.env.ref('account.%s' % (xml_id)).read()[0]
            invoice_domain = safe_eval(result['domain'])
            invoice_domain.append(('id', 'in', created_inv))
            result['domain'] = invoice_domain
            return result
        return True


class InvoiceDetails(models.Model):
    _name = 'invoice.details'
    _inherits = {'account.invoice': 'invoice_id'}

    invoice_id = fields.Many2one('account.invoice')
    partner_payment_id = fields.Many2one('partner.payment')
    select = fields.Boolean()

    @api.model
    def create(self, vals):
        if not vals.get('account_id'):
            account_id = self.env['account.invoice'].browse(int(vals.get('invoice_id'))).account_id.id
            vals.update({'account_id': account_id})
        return super(InvoiceDetails, self).create(vals)


class PartnerPayment(models.Model):
    _inherits = {'account.voucher': 'voucher_relation_id'}
    _name = 'partner.payment'
    _rec_name = 'reference_number'

    voucher_relation_id = fields.Many2one('account.voucher')
    res_person_id = fields.Many2one('res.partner', domain=[('res_person_id', '=', True)])
    partner_id = fields.Many2one('res.partner')
    reference_number = fields.Char()
    date = fields.Date()
    payment_method = fields.Selection([('cheque', 'Cheque'), ('cash', 'Cash')], string="Mode of Payment")
    cheque_no = fields.Char()
    cheque_date = fields.Date()
    remarks = fields.Text()
    # total_amount = fields.Float(compute='_compute_amount')
    total_amount = fields.Float(compute='_compute_value', store=True)
    payment_amount = fields.Float()
    balance_amount = fields.Float(compute='_compute_balance')
    # balance_amount = fields.Float()
    invoice_ids = fields.One2many('invoice.details', 'partner_payment_id', compute='generate_lines', readonly=False,
                                  store=True)
    state = fields.Selection([('new', 'New'), ('draft', 'Draft'), ('paid', 'Paid')])

    @api.onchange('res_person_id', 'partner_id')
    def onchange_id(self):
        print('I am herte')
        for rec in self:
            print('I am herte22')
            if rec.res_person_id and rec.partner_id:
                rec.invoice_ids = []
                print('I am herte333')
                list = []
                invoices = self.env['account.invoice'].search(
                    [('partner_id', '=', rec.partner_id.id), ('res_person', '=', rec.res_person_id.id)])
                if invoices:
                    for line in invoices:
                        if line.state == 'open':
                            list.append([0, 0, {'partner_id': line.partner_id.id,
                                                'name': line.name,
                                                'reference': line.reference,
                                                'type': line.type,
                                                'state': line.state,
                                                'amount_total': line.amount_total,
                                                'amount_untaxed': line.amount_untaxed,
                                                'amount_tax': line.amount_tax,
                                                'residual': line.residual,
                                                'currency_id': line.currency_id.id,
                                                'origin': line.origin,
                                                'date_invoice': line.date_invoice,
                                                'journal_id': line.journal_id.id,
                                                'period_id': line.period_id.id,
                                                'company_id': line.company_id.id,
                                                'user_id': line.user_id.id,
                                                'date_due': line.date_due,
                                                'number2': line.number2,
                                                'account_id': line.account_id.id,
                                                'invoice_id': line.id
                                                }
                                         ])
                rec.invoice_ids = list
                print ('onchange')
                print list

    @api.depends('res_person_id', 'partner_id')
    def generate_lines(self):
        print (self)
        for rec in self:
            rec.account_id = 25
            rec.invoice_ids = []
            if rec.res_person_id and rec.partner_id:
                list = []
                invoices = self.env['account.invoice'].search(
                    [('partner_id', '=', rec.partner_id.id), ('res_person', '=', rec.res_person_id.id)])
                if invoices:
                    for line in invoices:
                        if line.state == 'open':
                            list.append([0, 0, {'partner_id': line.partner_id.id,
                                                'name': line.name,
                                                'reference': line.reference,
                                                'type': line.type,
                                                'state': line.state,
                                                'amount_total': line.amount_total,
                                                'amount_untaxed': line.amount_untaxed,
                                                'residual': line.residual,
                                                'currency_id': line.currency_id.id,
                                                'origin': line.origin,
                                                'date_invoice': line.date_invoice,
                                                'journal_id': line.journal_id.id,
                                                'period_id': line.period_id.id,
                                                'company_id': line.company_id.id,
                                                'user_id': line.user_id.id,
                                                'date_due': line.date_due,
                                                'number2': line.number2,
                                                'account_id': line.account_id.id,
                                                'invoice_id': line.id
                                                }
                                         ])
                rec.invoice_ids = list
                print ('depends')

                print list

    @api.onchange('invoice_ids')
    def onchange_compute(self):
        for record in self:
            if record.invoice_ids:
                record.total_amount = sum(line.residual for line in record.invoice_ids)

    @api.depends('invoice_ids')
    def _compute_value(self):
        for record in self:
            if record.invoice_ids:
                record.total_amount = sum(line.residual for line in record.invoice_ids)

    @api.depends('total_amount', 'payment_amount')
    def _compute_balance(self):
        for record in self:
            if record.total_amount and record.payment_amount:
                difference = record.total_amount - record.payment_amount
                if difference < 0:
                    raise osv.except_osv(_('Warning!'), _("Total amount is less than payment amount."))
                record.balance_amount = max(difference, 0.0)

    # @api.onchange('res_person_id', 'partner_id')
    # def onchange_compute_amount(self):
    #     for record in self:
    #         if record.invoice_ids:
    #             for invoice in record.invoice_ids:
    #                 invoice.amount_untaxed = sum(line.price_subtotal for line in invoice.invoice_id.invoice_line)
    #                 invoice.amount_tax = sum(line.amount for line in invoice.invoice_id.tax_line)
    #                 invoice.amount_total = invoice.amount_untaxed + invoice.invoice_id.amount_tax
    #
    # @api.depends('invoice_ids')
    # def _compute_amount(self):
    #     for record in self:
    #         if record.invoice_ids:
    #             for invoice in record.invoice_ids:
    #                 invoice.amount_untaxed = sum(line.price_subtotal for line in invoice.invoice_id.invoice_line)
    #                 invoice.amount_tax = sum(line.amount for line in invoice.invoice_id.tax_line)
    #                 invoice.amount_total = invoice.amount_untaxed + invoice.invoice_id.amount_tax
    #
    # @api.onchange('res_person_id', 'partner_id')
    # def onchange_compute_residual(self):
    #     for record in self:
    #         if record.invoice_ids:
    #             for invoice in record.invoice_ids:
    #                 invoice.residual = 0.0
    #                 # Each partial reconciliation is considered only once for each invoice it appears into,
    #                 # and its residual amount is divided by this number of invoices
    #                 partial_reconciliations_done = []
    #                 for line in invoice.sudo().move_id.line_id:
    #                     if line.account_id.type not in ('receivable', 'payable'):
    #                         continue
    #                     if line.reconcile_partial_id and line.reconcile_partial_id.id in partial_reconciliations_done:
    #                         continue
    #                     # Get the correct line residual amount
    #                     if line.currency_id == invoice.currency_id:
    #                         line_amount = line.amount_residual_currency if line.currency_id else line.amount_residual
    #                     else:
    #                         from_currency = line.company_id.currency_id.with_context(date=line.date)
    #                         line_amount = from_currency.compute(line.amount_residual, invoice.currency_id)
    #                     # For partially reconciled lines, split the residual amount
    #                     if line.reconcile_partial_id:
    #                         partial_reconciliation_invoices = set()
    #                         for pline in line.reconcile_partial_id.line_partial_ids:
    #                             if pline.invoice and invoice.type == pline.invoice.type:
    #                                 partial_reconciliation_invoices.update([pline.invoice.id])
    #                         line_amount = invoice.currency_id.round(line_amount / len(partial_reconciliation_invoices))
    #                         partial_reconciliations_done.append(line.reconcile_partial_id.id)
    #                     invoice.residual += line_amount
    #                 invoice.residual = max(invoice.residual, 0.0)
    #
    # @api.depends('invoice_ids')
    # def _compute_residual(self):
    #     for record in self:
    #         if record.invoice_ids:
    #             for invoice in record.invoice_ids:
    #                 invoice.residual = 0.0
    #                 # Each partial reconciliation is considered only once for each invoice it appears into,
    #                 # and its residual amount is divided by this number of invoices
    #                 partial_reconciliations_done = []
    #                 for line in invoice.sudo().move_id.line_id:
    #                     if line.account_id.type not in ('receivable', 'payable'):
    #                         continue
    #                     if line.reconcile_partial_id and line.reconcile_partial_id.id in partial_reconciliations_done:
    #                         continue
    #                     # Get the correct line residual amount
    #                     if line.currency_id == invoice.currency_id:
    #                         line_amount = line.amount_residual_currency if line.currency_id else line.amount_residual
    #                     else:
    #                         from_currency = line.company_id.currency_id.with_context(date=line.date)
    #                         line_amount = from_currency.compute(line.amount_residual, invoice.currency_id)
    #                     # For partially reconciled lines, split the residual amount
    #                     if line.reconcile_partial_id:
    #                         partial_reconciliation_invoices = set()
    #                         for pline in line.reconcile_partial_id.line_partial_ids:
    #                             if pline.invoice and invoice.type == pline.invoice.type:
    #                                 partial_reconciliation_invoices.update([pline.invoice.id])
    #                         line_amount = invoice.currency_id.round(line_amount / len(partial_reconciliation_invoices))
    #                         partial_reconciliations_done.append(line.reconcile_partial_id.id)
    #                     invoice.residual += line_amount
    #                 invoice.residual = max(invoice.residual, 0.0)

    @api.multi
    def action_payment_all(self, context=None):
        payment_amount = self.payment_amount
        for record in self.invoice_ids:
            if record.select:
                amount = 0
                invoice = record.invoice_id
                if payment_amount > 0:
                    if invoice.residual < payment_amount:
                        amount = invoice.residual
                    else:
                        amount = payment_amount
                    self.voucher_relation_id.amount = self.payment_amount
                    if amount == invoice.residual:
                        invoice.state = 'paid'
                    else:

                        move = self.env['account.move']
                        move_line = self.env['account.move.line']

                        values5 = {
                            'journal_id': 9,
                            'date': self.date,
                            'tds_id': invoice.id
                            # 'period_id': self.period_id.id,623393
                        }
                        move_id = move.create(values5)
                        balance_amount = invoice.residual - payment_amount

                        values4 = {
                            'account_id': 25,
                            'name': 'payment for invoice No ' + str(invoice.number2),
                            'debit': 0.0,
                            'credit': balance_amount,
                            'move_id': move_id.id,
                            'cheque_no': self.cheque_no,
                            'invoice_no_id2': invoice.id,
                        }
                        line_id1 = move_line.create(values4)

                        values6 = {
                            'account_id': invoice.account_id.id,
                            'name': 'Payment For invoice No ' + str(invoice.number2),
                            'debit': balance_amount,
                            'credit': 0.0,
                            'move_id': move_id.id,
                            'cheque_no': self.cheque_no,
                            # 'invoice_no_id2': line.bill_no.id,
                        }
                        line_id2 = move_line.create(values6)

                        invoice.move_id = move_id.id
                        invoice.move_lines = move_id.line_id.ids
                        move_id.button_validate()
                        move_id.post()
                        name = move_id.name
                        self.voucher_relation_id.write({
                            'move_id': move_id.id,
                            'state': 'posted',
                            'number': name,
                        })
                    payment_amount = payment_amount - amount
                    self.state = 'paid'
        return True

        # pay_id = id
        #
        #
        #
        #
        #
        #
        #
        # values = {'lang': 'en_US',
        #            'default_amount': invoice.amount_total,
        #            'tz': False,
        #            'uid': 1,
        #            'payment_expected_currency': 21,
        #            'invoice_id': invoice.id,
        #            'journal_type': 'sale',
        #            'default_type': 'receipt',
        #            'invoice_type': 'out_invoice',
        #            'search_disable_custom_filters': True,
        #            'default_reference': False,
        #            'default_partner_id': invoice.partner_id.id,
        #            'type': 'receipt',
        #            }
        # voucher = self.voucher_relation_id
        # context.update(values)
        # move_pool = self.pool.get('account.move')
        # move_line_pool = self.pool.get('account.move.line')
        # self.voucher_relation_id.amount = self.payment_amount
        # company_currency = invoice.currency_id
        # current_currency = invoice.currency_id
        # local_context={}
        # move_id = self.pool.get('account.move').create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context),
        #                            context=context)
        # name = move_pool.browse(cr, uid, move_id, context=context).name
        # self.voucher_relation_id.signal_workflow('proforma_voucher')
        # move_line_id = move_line_pool.create(cr, uid,
        #                                      self.first_move_line_get(cr, uid, voucher.id, move_id,
        #                                                               company_currency,
        #                                                               current_currency, local_context),
        #                                      local_context)
        # move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
        # line_total = move_line_brw.debit - move_line_brw.credit

        # vals = {
        #     'amount': amount,
        #     'payment_expected_currency': invoice.currency_id.id,
        #     'invoice_id': invoice.id,
        #     'journal_type': 'sale',
        #     'type': 'receipt',
        #     'invoice_type': 'out_invoice',
        #     'reference': False,
        #
        #     'partner_id': invoice.partner_id.id,
        #
        #     'account_id': invoice.account_id.id,
        #     'period_id': invoice.period_id.id,
        #     'company_id': invoice.company_id.id,
        #     'currency_id': invoice.currency_id.id,
        #     'date': self.date,
        #     'journal_id': invoice.journal_id.id,
        #
        #     'paid_amount_in_company_currency': invoice.currency_id.id,
        #     'pay_now': 'pay_now',
        #     'payment_option': 'without_writeoff',
        #     'payment_rate': 1.0,
        #     'payment_rate_currency_id': invoice.currency_id.id,
        #     'pre_line': True,
        #     'state': 'draft',
        #     'writeoff_amount': 0.0,
        # }
        #
        # self.env['account.voucher'].signal_workflow('proforma_voucher')
        #
        # voucher = self.env['account.voucher'].create(vals)
        # reconcile = False
        # if invoice.residual == amount:
        #     reconcile = True
        # tax_amount = sum(line.amount for line in invoice.tax_line)
        # amount_untaxed = sum(line.price_subtotal for line in invoice.invoice_line)
        # amount_unreconciled = invoice.residual
        # line_ids = self.env['account.voucher.line'].create({
        #     'account_id': invoice.account_id.id,
        #     'amount': amount,
        #     'company_id': invoice.company_id.id,
        #     'currency_id': invoice.currency_id.id,
        #     'date_due': invoice.date_due,
        #     'date_original': self.date,
        #     'partner_id': invoice.partner_id.id,
        #     'reconcile': reconcile,
        #     'state': 'draft',
        #     # 'untax_amount': invoice.amount_untaxed,
        #     'voucher_id': voucher.id, })
        #
        # voucher.line_ids = line_ids
        # context.update({'action_payment_all': True})
        # res = voucher.action_move_line_create(context=context)
        # if res:

        #         payment_amount = payment_amount - amount
        #         self.state = 'paid'
        # return True

        # if context is None:
        #     context = {}
        # move_pool = self.pool.get('account.move')
        # move_line_pool = self.pool.get('account.move.line')
        # account_voucher = self.pool.get('account.voucher')
        # for voucher in self.browse(cr, uid, ids, context=context):
        #     local_context = dict(context, force_company=invoice.journal_id.company_id.id)
        #     # if voucher.move_id:
        #     #     continue
        #     current_currency = invoice.journal_id.company_id.currency_id.id
        #     company_currency = invoice.journal_id.company_id.currency_id.id
        #     # current_currency = self._get_current_currency(cr, uid, voucher.id, context)
        #     # company_currency = self._get_company_currency(cr, uid, voucher.id, context)
        #     # we select the context to use accordingly if it's a multicurrency case or not
        #     context = account_voucher._sel_context(cr, uid, voucher.id, context)
        #     # But for the operations made by _convert_amount, we always need to give the date in the context
        #     ctx = context.copy()
        #     ctx.update({'date': voucher.date})
        #     # Create the account move record.
        #     move_id = move_pool.create(cr, uid, account_voucher.account_move_get(cr, uid, voucher.id, context=context),
        #                                context=context)
        #     # Get the name of the account_move just created
        #     name = move_pool.browse(cr, uid, move_id, context=context).name
        #     # Create the first line of the voucher
        #     move_line_id = move_line_pool.create(cr, uid, account_voucher.first_move_line_get(cr, uid, voucher.id, move_id,
        #                                                                            company_currency,
        #                                                                            current_currency, local_context),
        #                                          local_context)
        #     move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
        #     line_total = move_line_brw.debit - move_line_brw.credit
        #     rec_list_ids = []
        #     if voucher.type == 'sale':
        #         line_total = line_total - account_voucher._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
        #     elif voucher.type == 'purchase':
        #         line_total = line_total + account_voucher._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
        #     # Create one move line per voucher line where amount is not 0.0
        #     line_total, rec_list_ids = account_voucher.voucher_move_line_create(cr, uid, voucher.id, line_total, move_id,
        #                                                              company_currency, current_currency, context)
        #
        #     # Create the writeoff line if needed
        #     # ml_writeoff = account_voucher.writeoff_move_line_get(cr, uid, voucher.id, line_total, move_id, name,
        #     #                                           company_currency, current_currency, local_context)
        #     # if ml_writeoff:
        #     #     move_line_pool.create(cr, uid, ml_writeoff, local_context)
        #     # We post the voucher.
        #     account_voucher.write(cr, uid, [voucher.id], {
        #         'move_id': move_id,
        #         'state': 'posted',
        #         'number': name,
        #     })
        #     if voucher.journal_id.entry_posted:
        #         move_pool.post(cr, uid, [move_id], context={})
        #     # We automatically reconcile the account move lines.
        #     reconcile = False
        #     for rec_ids in rec_list_ids:
        #         if len(rec_ids) >= 2:
        #             reconcile = move_line_pool.reconcile_partial(cr, uid, rec_ids,
        #                                                          writeoff_acc_id=voucher.writeoff_acc_id.id,
        #                                                          writeoff_period_id=voucher.period_id.id,
        #                                                          writeoff_journal_id=voucher.journal_id.id)
        # return True

    @api.multi
    def open_tree_view_history(self, context=None):
        if self.res_person_id:
            field_ids = self.env['account.invoice'].search([('res_person', '=', self.res_person_id.id)]).ids
            domain = [('id', 'in', field_ids)]
            view_id_tree = self.env['ir.ui.view'].search([('name', '=', "model.tree")])
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                # 'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
                'view_id ref="invoice_stock_move.tree_view"': '',
                'target': 'current',
                'domain': domain,
            }

    @api.model
    def create(self, vals):
        if not vals.get('reference_number'):
            vals['reference_number'] = self.env['ir.sequence'].next_by_code(
                'partner.payment')
        vals.update({'state': 'draft'})
        vals.update({'account_id': 25})
        result = super(PartnerPayment, self).create(vals)
        return result


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    # @api.model
    # def create(self, vals):
    #     return super(AccountVoucher, self).create(vals)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _compute_residual(self):
        for record in self:
            record.residual = 0.0
            # Each partial reconciliation is considered only once for each invoice it appears into,
            # and its residual amount is divided by this number of invoices
            partial_reconciliations_done = []
            for line in record.sudo().move_id.line_id:
                if line.account_id.type not in ('receivable', 'payable'):
                    continue
                if line.reconcile_partial_id and line.reconcile_partial_id.id in partial_reconciliations_done:
                    continue
                # Get the correct line residual amount
                if line.currency_id == record.currency_id:
                    line_amount = line.amount_residual_currency if line.currency_id else line.amount_residual
                else:
                    from_currency = line.company_id.currency_id.with_context(date=line.date)
                    line_amount = from_currency.compute(line.amount_residual, record.currency_id)
                # For partially reconciled lines, split the residual amount
                if line.reconcile_partial_id:
                    partial_reconciliation_invoices = set()
                    for pline in line.reconcile_partial_id.line_partial_ids:
                        if pline.invoice and record.type == pline.invoice.type:
                            partial_reconciliation_invoices.update([pline.invoice.id])
                    line_amount = record.currency_id.round(line_amount / len(partial_reconciliation_invoices))
                    partial_reconciliations_done.append(line.reconcile_partial_id.id)
                record.residual += line_amount
            record.residual = max(record.residual, 0.0)
            # if record.type == 'out_invoice':
            #     if record.residual +=
            if record.state == 'paid':
                record.residual = 0.0
