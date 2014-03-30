from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_partner(osv.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {
        'reference': fields.char('Reference', size=64),
        'invoice_account_payable': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Invoice Account Payable",
            view_load=True,
            domain="[('type', '=', 'payable')]",
            help="This account is used during invoice line account determination."),
        'invoice_account_receivable': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Invoice Account Receivable",
            view_load=True,
            domain="[('type', '=', 'receivable')]",
            help="This account is used during invoice line account determination."),
    }
