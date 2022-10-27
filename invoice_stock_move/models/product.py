from openerp import models, fields, api


class Medicines(models.Model):
    _inherit = 'product.template'

    medicine_rack = fields.Many2one('product.medicine.types', 'Medicine Category/Rack')
    product_of = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency')
    # medicine_name_subcat = fields.Char('Potency')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing')
    medicine_grp = fields.Many2one('product.medicine.group', 'Grp')
    # medicine_group = fields.Char('Group')
    batch = fields.Char("Batch")
    tax_ids = fields.Many2many('account.tax', 'name', 'Tax')
    hsn_code = fields.Char('HSN', )
    tax_combo = fields.Many2one('tax.combo', 'Tax')

    @api.onchange('medicine_name_subcat')
    def onchange_ref_id(self):
        for rec in self:
            pass

            # rec.default_code = rec.medicine_name_subcat.medicine_rack_subcat

    @api.model
    def create(self, vals):
        result = super(Medicines, self).create(vals)
        # ref = result.default_code
        # inte_ref = str(ref) + "ref:"+str(result.id)
        # ref_obj = self.env['product.template'].search([('default_code', '=', ref),('name','=',result.name)])
        # print("object.............",ref_obj)
        # if ref_obj:
        #     for objs in ref_obj:
        #         if objs.id != result.id:
        #             result.default_code = inte_ref
        #             break
        #         elif(objs.id == result.id):
        #             result.default_code = ref
        #         else:
        #             result.default_code = ref
        #
        # else:
        #     result.default_code = ref


        return result


class MedicineRackSubcat(models.Model):
    _name = 'product.medicine.subcat'
    _rec_name = 'medicine_rack_subcat'

    medicine_rack_subcat = fields.Char(string="Potency Description")



# TAX-MED-POTENCY-COMBO-RELATION**********************************************************************

class MedPotencyCombo(models.Model):
    _name = 'medpotency.combo'

    groups_id = fields.Many2one('product.medicine.group', string="Group ID")
    medicine = fields.Many2one('product.product', string="Product")
    potency = fields.Many2one('product.medicine.subcat', string='Potency', requiered=True,
                              change_default=True, related="medicine.medicine_name_subcat")
    hsn = fields.Char(string='HSN')
    company = fields.Many2one('product.medicine.responsible', string="Company",related="medicine.product_of")
    tax = fields.Float(string='Tax')


class MedicineGroup(models.Model):
    _name = 'product.medicine.group'
    _rec_name = 'med_grp'

    med_grp = fields.Char("Group")
    potency_med_ids = fields.One2many(
        comodel_name='medpotency.combo',
        inverse_name='groups_id',
        string='Potency-Product Link',
        store=True,
    )


# **********************************************************************************************************

class MedicineTypes(models.Model):
    _name = 'product.medicine.types'
    _rec_name = 'medicine_type'

    medicine_type = fields.Char(string="Position/Rack")



class MedicinePacking(models.Model):
    _name = 'product.medicine.packing'
    _rec_name = 'medicine_pack'

    medicine_pack = fields.Char(string="Packing")


class MedicineResponsible(models.Model):
    _name = 'product.medicine.responsible'
    _rec_name = 'name_responsible'

    name_responsible = fields.Char(string="Product Of ")


class CustomerDiscounts(models.Model):
    _name = 'cus.discount'
    _rec_name = 'cus_dis'

    cus_dis = fields.Char(string="Discount Category", )
    percentage = fields.Float('Discount In Percentage(%)')



# New grp
class TaxComboNew(models.Model):
    _name = 'tax.combo.new'
    _rec_name = 'medicine_grp'

    combo_name = fields.Char('Description')
    # medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency')
    # medicine_name_subcat1 = fields.Many2many(comodel_name='product.medicine.subcat', string='Potency')
    medicine_grp = fields.Many2one('product.medicine.group', 'Group')
    product = fields.Many2one('product.template', 'Medicine')
    tax_rate = fields.Float('Tax(%)')
    hsn = fields.Char(string='HSN')
    company = fields.Many2one('product.medicine.responsible', string="Company")
    tax_cat = fields.Selection([('rate_tax', 'RATE TAX'), ('mrp_tax', 'MRP TAX'), ], 'Type', default='rate_tax')
    medicine_name_subcat1 = fields.Many2many(
        comodel_name='product.medicine.subcat',
        inverse_name='medicine_rack_subcat',
        string='Potencies',
        store=True,
    )


class TaxCombo(models.Model):
    _name = 'tax.combo'
    _rec_name = 'medicine_grp'

    combo_name = fields.Char('Description')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency')
    # medicine_name_subcat1 = fields.Many2many('product.medicine.subcat', 'Potency')
    medicine_grp = fields.Many2one('product.medicine.group', 'Group')
    product = fields.Many2one('product.template', 'Medicine')
    tax_rate = fields.Float('Tax(%)')
    hsn = fields.Char(string='HSN')
    company = fields.Many2one('product.medicine.responsible', string="Company")
    tax_cat = fields.Selection([('rate_tax', 'RATE TAX'), ('mrp_tax', 'MRP TAX'), ], 'Type', default='rate_tax')
