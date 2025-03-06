# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class LeaseContract(Document):
	def before_insert(self):
		# Fetch the default rent amount from Global Settings
		global_settings = frappe.get_single("Global Settings")
		
		# Ensure the field exists in Global Settings and self.rent_amount is not set
		if hasattr(global_settings, "default_rent_amount") and not self.rent_amount:
			self.rent_amount = global_settings.default_rent_amount

	def on_submit(self):
			if self.shop:
				try:
					shop_doc = frappe.get_doc("Shop", self.shop)

					shop_doc.lease_status = "Occupied"
					shop_doc.lease_contract = self.name
					shop_doc.tenant = self.tenant
					shop_doc.save()
					frappe.db.commit()  

				except Exception as e:
					frappe.log_error(f"Failed to update lease status for shop {self.shop}: {str(e)}", "LeaseContract Error")

	def on_update_after_submit(self):
		"""Check if the lease has expired and update the shop status to 'Available'."""
		update_expired_shops()

# def update_expired_shops():
# 	"""Fetch all expired lease contracts and update shop status to 'Available'."""
# 	expired_contracts = frappe.get_all(
# 		"Lease Contract",
# 		filters={"expiry_date": ["<=", nowdate()], "docstatus": 1},
# 		fields=["name", "shop"]
# 	)

# 	for contract in expired_contracts:
# 		try:
# 			if contract.shop:
# 				shop_doc = frappe.get_doc("Shop", contract.shop)

# 				if shop_doc.lease_status != "Available":
# 					shop_doc.lease_status = "Available"
# 					shop_doc.lease_contract = None
# 					shop_doc.tenant = None
# 					shop_doc.save()
# 					frappe.db.commit()
# 					print(f"✅ Shop {contract.shop} marked as available!")
# 		except Exception as e:
# 			frappe.log_error(f"Failed to update expired lease for shop {contract.shop}: {str(e)}", 
# 							 "LeaseContract Expiry Error")

def update_expired_shops():
    """Fetch all expired lease contracts and update shop status to 'Available'."""
    expired_contracts = frappe.get_all(
        "Lease Contract",
        filters={"expiry_date": ["<=", nowdate()], "docstatus": 1},
        fields=["name", "shop"]
    )

    for contract in expired_contracts:
        if contract.shop:
            try:
                # Batch update instead of loading document
                frappe.db.set_value("Shop", contract.shop, {
                    "lease_status": "Available",
                    "lease_contract": None,
                    "tenant": None
                })
                frappe.logger().info(f"Shop {contract.shop} marked as available!")
            except Exception as e:
                frappe.log_error(f"Failed to update expired lease for shop {contract.shop}: {str(e)}", 
                                 "LeaseContract Expiry Error")
