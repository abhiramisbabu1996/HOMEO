from openerp import models, fields, api


class RackTransfer(models.TransientModel):
    _name = 'rack.transfer'

    racks_id_1 = fields.Many2one('product.medicine.types', string='From')
    racks_id_2 = fields.Many2one('product.medicine.types', string='To')
    stock_full_id = fields.One2many(
        comodel_name='full.transfer',
        inverse_name='full_id',
        string=' ',
        store=True,
    )

    @api.multi
    def load_lines(self):
        # stock_obj = self.env['entry.stock'].search([])
        stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id)])
        print("id", self.racks_id_1.id)
        if stock_obj:
            print(stock_obj)
            new_lines = []
            for rec in stock_obj:
                print("box ids from stock", rec.rack.id)
                new_lines.append((0, 0, {
                    'qty': round(rec.qty, 0),
                    'name': rec.medicine_1.name,
                    'medicine_1': rec.medicine_1.id,
                    'potency': rec.potency.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'company': rec.company.id,
                    'batch_2': rec.batch_2.id,
                }))
            self.write({'stock_full_id': new_lines})
        else:
            print("no stock")
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rack.transfer',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def full_transfer(self):
        print("welcome")
        stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id)])
        if stock_obj:
            for rec in stock_obj:
                rec.write({'rack': self.racks_id_2.id})
            for rec in self:
                rec.write({'stock_full_id': [(5, 0, 0)]})

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rack.transfer',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class FullyTranser(models.Model):
    _name = 'full.transfer'

    expiry_date = fields.Date(string='Expiry Date')
    manf_date = fields.Date(string='Manufacturing Date')
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    batch_2 = fields.Many2one('med.batch', "Batch")
    rack = fields.Many2one('product.medicine.types', 'Rack')
    qty = fields.Float('Stock')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    qty_received = fields.Float('Qty Trasfer')
    full_id = fields.Many2one('rack.transfer', string='Stock')



