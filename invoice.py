from openerp.osv import osv
from openerp.tools.translate import _
import re
import datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class account_invoice(osv.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"


    def expertm_partner_resolver(self, cr, uid, ids, context):
        raise osv.except_osv(_('Warning!'), _("Resolving is not supported for this flow."))

    def send_expertm_out(self, cr, uid, items, context=None):
        ''' account.invoice:send_edi_out()
            ------------------------------
            This method will perform the export of an invoice.
            -------------------------------------------------- '''

        edi_db = self.pool.get('clubit.tools.edi.document.outgoing')

        # Get the selected items
        # ----------------------
        inv_ids = [x['id'] for x in items]
        invoices = self.browse(cr, uid, inv_ids, context=context)


        # Actual processing of all the invoices
        # -------------------------------------
        root = ET.Element("ImportExpMPlus")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")


        sales = ET.SubElement(root, "Sales")
        for invoice in invoices:
            sale = ET.SubElement(sales, "Sale")
            total_done = False

            numbers = re.findall('\d+', invoice.number)
            invoice_type = '10'
            if invoice.type == 'out_refund':
                invoice_type = '30'


            if invoice.partner_id.parent_id:
                ET.SubElement(sale, "Customer_Prime").text = invoice.partner_id.parent_id.reference
            else:
                ET.SubElement(sale, "Customer_Prime").text = invoice.partner_id.reference

            ET.SubElement(sale, "CurrencyCode").text   = invoice.currency_id.name
            ET.SubElement(sale, "DocType").text        = invoice_type
            ET.SubElement(sale, "DocNumber").text      = ''.join(numbers)
            ET.SubElement(sale, "DocDate").text        = datetime.datetime.strptime(invoice.date_invoice, "%Y-%m-%d").strftime("%d/%m/%Y")
            ET.SubElement(sale, "DueDate").text        = datetime.datetime.strptime(invoice.date_due, "%Y-%m-%d").strftime("%d/%m/%Y")
            ET.SubElement(sale, "OurRef").text         = invoice.name
            ET.SubElement(sale, "Amount").text         = ('%.2f' % invoice.amount_total).replace('.',',')
            ET.SubElement(sale, "Status").text         = '0'

            details = ET.SubElement(sale, "Details")
            for line in invoice.move_id.line_id:

                if invoice.account_id.code == line.account_id.code and total_done:
                    continue

                detail = ET.SubElement(details, "Detail")
                anal = ET.SubElement(detail, "Analytics1")
                anal = ET.SubElement(anal, "Analytic")

                if invoice.account_id.code == line.account_id.code:

                    total_done = True
                    ET.SubElement(detail, "Amount").text  = ('%.2f' % invoice.amount_total).replace('.',',')
                    ET.SubElement(anal, "Amount").text    = ('%.2f' % invoice.amount_total).replace('.',',')
                    if invoice.type == 'out_refund':
                        ET.SubElement(detail, "DebCre").text  = '-1'
                    else:
                        ET.SubElement(detail, "DebCre").text  = '1'
                else:

                    if line.debit != 0:
                        ET.SubElement(detail, "Amount").text  = ('%.2f' % line.debit).replace('.',',')
                        ET.SubElement(anal, "Amount").text    = ('%.2f' % line.debit).replace('.',',')
                        ET.SubElement(detail, "DebCre").text  = '1'
                    else:
                        ET.SubElement(detail, "Amount").text  = ('%.2f' % line.credit).replace('.',',')
                        ET.SubElement(anal, "Amount").text    = ('%.2f' % line.credit).replace('.',',')
                        ET.SubElement(detail, "DebCre").text  = '-1'

                ET.SubElement(detail, "Account").text = line.account_id.code

                if line.tax_code_id:
                    ET.SubElement(detail, "Ventil").text  = line.tax_code_id.ventil_code
                    ET.SubElement(detail, "VAT1").text    = line.tax_code_id.code
                else:
                    ET.SubElement(detail, "Ventil").text  = ''



        # Add the XML structure to the EDI document
        # -----------------------------------------
        result = edi_db.create_from_content(cr, uid, 'invoices_to_expertm', root, items[0]['partner_id'], 'account.invoice', 'send_expertm_out', type='XML')
        if result != True:
            raise osv.except_osv(_('Error!'), _("Something went wrong while trying to create one of the EDI documents. Please contact your system administrator. Error given: {!s}").format(result))











class account_invoice_line(osv.Model):

    _name = "account.invoice.line"
    _inherit = "account.invoice.line"

    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, context=None, company_id=None):

        result = super(account_invoice_line,self).product_id_change(cr, uid, ids, product, uom_id, qty, name, type, partner_id, fposition_id, price_unit, currency_id, context, company_id)
        if not partner_id or not product:
            return result

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        if type == 'out_refund':
            backup = result['value']['account_id']
            result['value']['account_id'] = prod.property_account_expense.id
            if not result['value']['account_id']:
                result['value']['account_id'] = prod.categ_id.refund_account.id
            if not result['value']['account_id']:
                result['value']['account_id'] = backup

        fpos_db = self.pool.get('account.fiscal.position')
        fpos = fposition_id and fpos_db.browse(cr, uid, fposition_id, context=context) or False
        result['value']['account_id'] = fpos_db.map_account(cr, uid, fpos, result['value']['account_id'])
        return result


