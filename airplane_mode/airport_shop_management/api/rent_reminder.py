# import frappe
# from frappe.utils import today

# def send_rent_reminders():

#     # Checks if rent notifications are enabled in Global Settings
#     global_settings = frappe.get_single("Global Settings")
#     if not global_settings.get("enable_rent_reminders"):
#         frappe.msgprint("Rent notifications are disabled in Global Settings.")
#         return
    
#     occupied_shops = frappe.get_all("Shop", fields=["lease_status"])
    
#     for shop in occupied_shops:
        
#         if shop.get("lease_status") != "Available":


#             # Get the current month and year
#             current_month = frappe.utils.getdate(today()).strftime("%B")
#             current_year = frappe.utils.getdate(today()).year

#             # Fetch all occupied shops
#             occupied_shops = frappe.get_all(
#                 "Lease Contract",
#                 fields=["name", "tenant", "tenant_email", "airport"]
#             )

#             for shop in occupied_shops:
#                 if shop.get("tenant_email"):
#                     subject = f"Monthly Rent Due - {current_month} {current_year}"
#                     message = f"""
#                         Dear {shop['tenant']},

#                         This is a gentle reminder that your rent for {current_month} {current_year} is due. 
#                         Please ensure timely payment to avoid any penalties.

#                         Regards,  
#                         Airport Management
#                     """

#                     # Send Email
#                     frappe.sendmail(
#                         recipients=[shop["tenant_email"]],
#                         subject=subject,
#                         message=message
#                     )

#                     frappe.msgprint(f"Reminder sent to {shop['tenant']} ({shop['tenant_email']})")


#################################clean code:
import frappe
from frappe.utils import add_days, nowdate, getdate

def send_rent_reminders():
    global_settings = frappe.get_single("Global Settings")
    if not global_settings.get("enable_rent_reminders"):
        frappe.msgprint("Rent notifications are disabled in Global Settings.")
        return

    today = getdate(nowdate())  
    current_month = today.strftime("%B")
    current_year = today.year

    occupied_contracts = frappe.get_all("Shop", filters={"lease_status": "Occupied"}, fields=["lease_contract"])


    for contract in occupied_contracts:

        occupied_contract = frappe.get_doc(
            "Lease Contract", contract.lease_contract
        )

        start_date = getdate(occupied_contract.start_date) 
        reminder_date = add_days(start_date, -2)  

        # Check if today is the correct reminder date
        if reminder_date.day == today.day:
            subject = f"Monthly Rent Due - {current_month} {current_year}"
            message = f"""
                Dear {contract.tenant},

                This is a gentle reminder that your rent {contract.rent_amount} for {current_month} {current_year} is due. 
                Please ensure timely payment to avoid any penalties.

                Regards,  
                Airport Management
            """

            # Send Email
            frappe.sendmail(
                recipients=[occupied_contract.tenant_email],
                subject=subject,
                message=message
            )

            frappe.logger().info(f"Reminder sent to {occupied_contract.tenant} ({occupied_contract.tenant_email})")