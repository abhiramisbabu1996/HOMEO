from openerp import models, fields, api



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    local_customer = fields.Boolean("Local Customer", default=True)
    interstate_customer = fields.Boolean("Interstate Customer")
    b2b = fields.Boolean("B2B")
    b2c = fields.Boolean("B2C", default=True)
    bill_nature = fields.Selection([('gst', 'GST'), ('igst', 'IGST')], default='gst', compute='compute_bill')
    doctor_name = fields.Many2one('res.partner','Doctor Name')
    res_person = fields.Many2one('res.partner',string="Responsible Person")
    address_new = fields.Text('Address',related="partner_id.address_new")

    # @api.onchange('partner_id')
    # def onchange_address_id(self):
    #
    #     pass


    # @api.onchange('b2b')
    # def onchange_b2b(self):
    #     for rec in self:
    #         if rec.b2b:


    @api.depends('interstate_customer','local_customer')
    def compute_bill(self):
        for rec in self:
            if rec.local_customer:
                rec.bill_nature = 'gst'
            if rec.interstate_customer:
                rec.bill_nature = 'igst'
    
    @api.multi
    def tree_stock(self):
        print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
        return {
            'name': 'stock tree',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'entry.stock',
            'type': 'ir.actions.act_window',

            'search_view_id': self.env.ref('invoice_stock_move.stock_search_view').id
        }

    @api.multi
    def wiz_tree(self):
        print("9999999999999999999999999999")
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'entry.stock',
            'res_id': self.id,
            'view_id': 'invoice_stock_move.new_stock_entry_tree_id_js',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class ResPartner(models.Model):
    _inherit = "res.partner"

    local_customer = fields.Boolean(default=True)
    interstate_customer = fields.Boolean()
    b2b = fields.Boolean(compute="_change_boolean_status")
    b2c = fields.Boolean()
    gst_no = fields.Char()
    drug_license_number = fields.Char()
    address_new = fields.Text('Address')
    res_person_id = fields.Boolean('Sale Responsible Person ?')

    @api.depends('gst_no')
    def _change_boolean_status(self):
        if self.gst_no:
            self.b2b = True
            self.b2c = False
        else:
            self.b2c = True
            self.b2b = False
            # students = self.env['<_name>'].search([('id', '!=', self.id)])
            # for student in students:
            #     student.default_selected_student = False




    @api.multi
    def open_tree_view(self, context=None):
        field_ids = self.env['account.invoice'].search([('res_person', '=', self.id)]).ids

        domain = [('id', 'in', field_ids)]

        view_id_tree = self.env['ir.ui.view'].search([('name', '=', "model.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_type': 'form',
            'view_mode': 'tree,form',
            # 'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'view_id ref="customer_sale_history.tree_view"': '',
            'target': 'current',
            'domain': domain,
        }
