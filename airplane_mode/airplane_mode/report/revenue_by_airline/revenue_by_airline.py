# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt


import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum

def execute(filters=None):
    # Define the Doctype
    RentPayment = DocType("Rent Payment")

    # Query to calculate rent collected per month by extracting year and month using SQL functions
    query = (
        frappe.qb.from_(RentPayment)
        .select(
            frappe.qb.functions.Year(RentPayment.payment_date).as_("year"),  # Extracting year using SQL function
            frappe.qb.functions.Month(RentPayment.payment_date).as_("month"),  # Extracting month using SQL function
            Sum(RentPayment.amount_paid).as_("total_rent_collected")  # Summing rent collected
        )
        .groupby(frappe.qb.functions.Year(RentPayment.payment_date), frappe.qb.functions.Month(RentPayment.payment_date))
        .orderby(frappe.qb.functions.Year(RentPayment.payment_date), frappe.qb.functions.Month(RentPayment.payment_date))
    )

    # Execute Query
    data = query.run(as_dict=True)

    # Define Report Columns
    columns = [
        {"label": "Year", "fieldname": "year", "fieldtype": "Int", "width": 100},
        {"label": "Month", "fieldname": "month", "fieldtype": "Int", "width": 100},
        {"label": "Total Rent Collected", "fieldname": "total_rent_collected", "fieldtype": "Currency", "width": 200}
    ]

    # Generate Chart (Bar Chart for Monthly Rent Collection)
    chart = {
        "data": {
            "labels": [f"{row['year']}-{row['month']:02d}" for row in data], 
            "datasets": [{"values": [row["total_rent_collected"] for row in data]}]
        },
        "type": "bar"
    }

    # Summary Section (Total Rent Collected)
    total_rent = sum(row["total_rent_collected"] for row in data)
    summary = [
        {
            "value": total_rent,
            "label": "Total Rent Collected",
            "datatype": "Currency",
            "indicator": "Green"
        }
    ]

    return columns, data, None, chart, summary
