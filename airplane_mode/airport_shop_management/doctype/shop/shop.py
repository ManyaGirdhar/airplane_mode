# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Shop(WebsiteGenerator):
    def before_save(self):
        """Update shop counts for the related airport when a shop is added or modified."""
        if self.airport:
            self.adjust_airport_shop_counts(is_new=self.is_new())

    def on_trash(self):
        """Update shop counts for the related airport when a shop is deleted."""
        if self.airport:
            self.adjust_airport_shop_counts(deleted=True)

    def adjust_airport_shop_counts(self, is_new=False, deleted=False):
        """Update shop counts incrementally instead of recounting."""
        airport = frappe.get_doc("Airport", self.airport)

        # Get previous lease status if the shop exists
        previous_shop = None
        if not is_new and not deleted:
            previous_shop = frappe.get_doc("Shop", self.name)

        # Handling deletion
        if deleted:
            if self.lease_status == "Available":
                airport.available_shops -= 1
            elif self.lease_status == "Occupied":
                airport.occupied_shops -= 1
            airport.total_shops -= 1

        # Handling addition
        elif is_new:
            airport.total_shops += 1
            if self.lease_status == "Available":
                airport.available_shops += 1
            elif self.lease_status == "Occupied":
                airport.occupied_shops += 1

        # Handling updates
        elif previous_shop:
            if previous_shop.lease_status != self.lease_status:
                if previous_shop.lease_status == "Available":
                    airport.available_shops -= 1
                elif previous_shop.lease_status == "Occupied":
                    airport.occupied_shops -= 1

                if self.lease_status == "Available":
                    airport.available_shops += 1
                elif self.lease_status == "Occupied":
                    airport.occupied_shops += 1

        airport.save()
