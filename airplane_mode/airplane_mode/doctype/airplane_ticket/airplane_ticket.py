# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt

import frappe
import random 
from frappe.model.document import Document


# class AirplaneTicket(Document):

	# def totalamount(self):
	# 	unique_adds = {}
	# 	for row in self.get("add_ons"):
	# 		if row.item not in unique_adds:
	# 			unique_adds[row.item] = row.amount
	# 	# Calculate total amount
	# 	self.total_amount = self.flight_price + sum(unique_adds.values())
	# 	return self.total_amount
	
class AirplaneTicket(Document):

	def validate(self):
		self.remove_dup()
		# self.check_capacity()
		self.fetch_gate_number()  

		
	def before_submit(self):
			if(self.status!= "Boarded"):
				frappe.throw('Please select the status to Boarded to submit the form!')


	def before_insert(self):
		random_number = random.randint(1, 99) 
		random_letter = random.choice(["A", "B", "C", "D", "E"])  
	
		self.seat = f"{random_number}{random_letter}"

	
	def remove_dup(self):
		"""Ensure add-ons are unique and update total amount before saving."""
		unique_adds = []
		seen_items = set()
		total_addons_amount = 0  # Initialize total add-ons amount

		# Remove duplicate add-ons and calculate total amount
		for row in self.get("add_ons", []):
			if row.item not in seen_items:
				seen_items.add(row.item)
				unique_adds.append(row)
				total_addons_amount += row.amount  # Sum the unique add-ons amount

		self.set("add_ons", unique_adds)  # Update child table with unique add-ons

		# Calculate total amount
		self.total_amount = self.flight_price + total_addons_amount

	def on_submit(self):
		flight = frappe.get_doc("Airplane Flight", self.flight)  # Assuming "Airplane Flight" is the correct DocType
		if not flight.airplane:
			frappe.throw("This flight is not linked to an airplane.")

		airplane = frappe.get_doc("Airplane", flight.airplane)
		capacity = airplane.capacity  

		# Count existing tickets for this flight
		ticket_count = frappe.db.count("Airplane Ticket", {"flight": self.flight})

		# Prevent overbooking
		if ticket_count >= capacity+1:
			frappe.throw(f"Cannot create a new ticket. The flight has reached its maximum capacity of {capacity} seats.")

		frappe.msgprint(f"Ticket created successfully. {capacity - ticket_count} seat remaining.")
	

	def fetch_gate_number(self):
		"""Fetch the gate number from the associated flight and update the ticket."""
		if self.flight:
			gate_number = frappe.db.get_value("Airplane Flight", self.flight, "gate_number")
			self.gate_number = gate_number if gate_number else None



	

	