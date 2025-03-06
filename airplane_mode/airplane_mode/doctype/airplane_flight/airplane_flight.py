import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.background_jobs import enqueue

class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        """Mark flight as completed when submitted."""
        self.status = "Completed"
        self.save()

    def on_update(self):
        """Trigger background job when the gate number changes and auto-refresh the document."""
        if self.has_value_changed("gate_number"):
            enqueue(
                update_ticket_gate_numbers, 
                queue="long", 
                flight_name=self.name, 
                gate_number=self.gate_number
            )

@frappe.whitelist()
def update_ticket_gate_numbers(flight_name, gate_number):
    flight = frappe.get_doc("Airplane Flight", flight_name)
    
    flight.gate_number = gate_number
    flight.save()


    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, fields=["name"])

    for ticket in tickets:
        ticket_doc = frappe.get_doc("Airplane Ticket", ticket["name"])
        ticket_doc.gate_number = gate_number  
        ticket_doc.save()

    # frappe.db.commit()
    return f"Updated gate number to {gate_number} for flight {flight_name} and all associated tickets."
