from openerp import models, fields, api


class PartialTransfer(models.TransientModel):
    _name = 'partial.transferr'

    racks_id_1 = fields.Many2one('product.medicine.types', string='From')
    racks_id_2 = fields.Many2one('product.medicine.types', string='To')
    stock_part_id = fields.One2many(
        comodel_name='partial.transfernew',
        inverse_name='full_id',
        string=' ',
        store=True,
    )

    @api.multi
    def load_lines(self):
        # stock_obj = self.env['entry.stock'].search([])
        stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id)])
        if stock_obj:
            new_lines = []
            for rec in stock_obj:
                new_lines.append((0, 0, {
                    'qty': round(rec.qty, 0),
                    'name': rec.medicine_1.name,
                    'medicine_1': rec.medicine_1.id,
                    'potency': rec.potency.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'company': rec.company.id,
                    'batch_2': rec.batch_2.id,
                    'entry_stock_id': rec.id,
                }))
            self.write({'stock_part_id': new_lines})
        else:
            print("no stock")
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'partial.transferr',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    # @api.multi
    # def part_transfer(self):
    #     print("welcome")
    #     stock_obj = self.env['entry.stock'].search([('rack', '=', self.racks_id_1.id)])
    #     if stock_obj:
    #         # for rec in stock_obj:
    #         for item in self.stock_part_id:
    #             # if (rec.medicine_1.id == item.medicine_1.id) and (rec.potency.id == item.potency.id) and (rec.medicine_name_packing.id == item.medicine_name_packing.id)and(rec.company.id == item.company.id)and (rec.batch_2.id == item.batch_2.id):
    #                 # new_qty = rec.qty - item.qty_transfer
    #                 # rec.write({'qty':0})
    #                 item.entry_stock_id.qty -= float(item.qty_transfer)
    #
    #         #         vals={
    #         #         'qty': round(rec.qty, 0),
    #         #         'name': rec.medicine_1.name,
    #         #         'medicine_1': rec.medicine_1.id,
    #         #         'potency': rec.potency.id,
    #         #         'medicine_name_packing': rec.medicine_name_packing.id,
    #         #         'company': rec.company.id,
    #         #         'batch_2': rec.batch_2.id,
    #         #         'entry_stock_id': rec.id,
    #         #     }
    #         # stock_obj
    #
    #
    #         # rec.write({'rack': self.racks_id_2.id})
    #         # rec.write({'qty':})
    #         for rec in self:
    #             rec.write({'stock_part_id': [(5, 0, 0)]})
    #
    #     return {
    #         'context': self.env.context,
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'partial.transferr',
    #         'res_id': self.id,
    #         'view_id': False,
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #     }


class PartTranserNew(models.TransientModel):
    _name = 'partial.transfernew'
#
    expiry_date = fields.Date(string='Expiry Date')
    manf_date = fields.Date(string='Manufacturing Date')
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    batch_2 = fields.Many2one('med.batch', "Batch")
    rack = fields.Many2one('product.medicine.types', 'Rack')
    qty = fields.Float('Stock')
    company = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    qty_received = fields.Float('Qty Transfer')
    full_id = fields.Many2one('partial.transferr', string='Stock')
    qty_transfer = fields.Char('Transfer_Qty')
    entry_stock_id = fields.Many2one('entry.stock')

#

#