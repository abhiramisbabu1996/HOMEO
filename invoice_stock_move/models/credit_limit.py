from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, tools

from openerp.exceptions import Warning
from openerp.tools.translate import _




class CreditLimitCustomerInv(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def button_validate(self):
        print("hellooooo")
        res = super(CreditLimitCustomerInv, self).button_validate()
        print("hiiiiii")
        if res.partner_id.customer == True:
            if res.pay_mode.state == 'credit':
                print("inside validate on behalf of credit limit")
        return res

        # add custom codes here

    @api.model
    @api.onchange('partner_id')
    def onchange_pay_mode_id(self):
        if self.pay_mode == 'credit':
            if self.partner_id.customer == True:
                print("inside credits onchange")

    @api.model
    def create(self, vals,):
        result = super(CreditLimitCustomerInv, self).create(vals)
        if result.partner_id.customer == True:
            if result.pay_mode == 'credit':
                credit_amount = result.partner_id.limit_amt
                used = result.partner_id.used_credit_amt
                bal = credit_amount - used
                if bal < result.amount_total:
                    print("Credit Amount is over")
                    raise Warning(_('This Customers Credit Limit Amount Rs. '+str(credit_amount)+'  has been Crossed.'+"\n" 'Check  '+result.partner_id.name+'s'+ ' Credit Limits'))
                   

        return result


class CreditLimitCustomer(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('limit_amt', 'used_credit_amt')
    def _compute_credited_amt(self):
        credit_ltd = self.limit_amt
        cust_obj = self.env['account.invoice'].search([('partner_id', '=', self.name)])
        if cust_obj:
            sum = 0
            for item in cust_obj:
                if item.state == 'paid':
                    if item.pay_mode == 'credit':
                        if item.partner_id.id == self.id:
                            sum = sum + item.amount_total
                            print(item.partner_id.id)
                            print(self.name)
            print("used amount", sum)
            self.used_credit_amt = sum

    limit_amt = fields.Float('Credit Limit Amount')
    used_credit_amt = fields.Float('Used Amount', compute="_compute_credited_amt")
