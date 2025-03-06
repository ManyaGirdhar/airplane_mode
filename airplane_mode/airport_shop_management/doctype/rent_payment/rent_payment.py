# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
    def before_submit(self):
        if not self.payment_proof:
            frappe.throw("Payment Proof is required for rent confirmation")
