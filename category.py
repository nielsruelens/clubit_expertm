from openerp.osv import osv, fields
from openerp.tools.translate import _

class product_category(osv.Model):
    _name = "product.category"
    _inherit = 'product.category'
    _description = "Category extensions"
    _columns = {
        'refund_account': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Refund Account",
            view_load=True,
            domain="[('type', '<>', 'view'),('type', '<>', 'consolidation')]",
            help="This account is used during refund line account determination."),
    }
