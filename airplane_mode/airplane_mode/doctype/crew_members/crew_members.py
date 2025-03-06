# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import random


class CrewMembers(Document):
	def before_insert(self, department_code):
		random_number = random.randint(100, 999)  # Ensuring a 3-digit unique number
		random_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # A single random letter
		
		self.employee_id = f"{department_code}{random_number}{random_letter}"

