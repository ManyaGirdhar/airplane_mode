# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # SQL Query to get rent collected per month
    data = frappe.db.sql("""
        SELECT 
            YEAR(payment_date) AS year, 
            MONTH(payment_date) AS month, 
            SUM(amount_paid) AS total_rent_collected
        FROM `tabRent Payment`
        GROUP BY YEAR(payment_date), MONTH(payment_date)
        ORDER BY YEAR(payment_date), MONTH(payment_date)
    """, as_dict=True)

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
