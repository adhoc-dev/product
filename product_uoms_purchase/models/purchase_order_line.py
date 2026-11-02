##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends("product_id.product_tmpl_id.use_product_uom")
    def _compute_allowed_uom_ids(self):
        super()._compute_allowed_uom_ids()
        for line in self:
            product = line.product_id
            if product:
                supplier_uoms = product.seller_ids.mapped("product_uom_id")
                if product.product_tmpl_id.use_product_uom:
                    line.allowed_uom_ids = product.uom_id | product.uom_po_ids | supplier_uoms
                else:
                    line.allowed_uom_ids = product.uom_po_ids | supplier_uoms

    def _product_id_change(self):
        """The product UoM is out of allowed_uom_ids when use_product_uom is off: start on a packaging."""
        super()._product_id_change()
        product = self.product_id
        if product and not product.product_tmpl_id.use_product_uom and product.uom_po_ids:
            self.product_uom_id = product.uom_po_ids[0]
