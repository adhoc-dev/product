##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import Command
from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPurchaseUoms(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.group_ids |= cls.env.ref("uom.group_uom")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_pack = cls.env["uom.uom"].create(
            {
                "name": "Purchase UoMs pack of 5",
                "relative_factor": 5.0,
                "relative_uom_id": cls.uom_unit.id,
            }
        )
        cls.vendor = cls.env["res.partner"].create({"name": "Purchase UoMs vendor"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Purchase UoMs product",
                "type": "consu",
                "uom_id": cls.uom_unit.id,
                "uom_po_ids": [Command.set(cls.uom_pack.ids)],
            }
        )

    def _new_line_uom(self):
        order_form = Form(self.env["purchase.order"])
        order_form.partner_id = self.vendor
        with order_form.order_line.new() as line:
            line.product_id = self.product
            return line.product_uom_id

    def test_product_uom_is_kept_when_it_is_allowed(self):
        self.assertEqual(self._new_line_uom(), self.uom_unit)

    def test_first_packaging_is_used_when_product_uom_is_not_allowed(self):
        self.product.product_tmpl_id.use_product_uom = False

        self.assertEqual(self._new_line_uom(), self.uom_pack)
