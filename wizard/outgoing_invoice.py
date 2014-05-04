from openerp.osv import osv
from openerp.tools.translate import _


class outgoing_invoice(osv.TransientModel):
    _inherit = ['clubit.tools.edi.wizard.outgoing']
    _name = 'outgoing.invoice'
    _description = 'Send Expert/M'