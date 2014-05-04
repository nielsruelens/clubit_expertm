from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_partner(osv.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {
        'reference': fields.char('ExpertM Reference', size=64),
    }
