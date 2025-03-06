# Copyright (c) 2025, Manya and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}

    # Fetch shop-related details directly from the Airport Doctype using ORM
    airports = frappe.get_all(
        "Airport",
        fields=["name", "total_shops", "available_shops", "occupied_shops"],
        order_by="name"
    )

    # Define Report Columns
    columns = [
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Data", "width": 200},
        {"label": "Total Shops", "fieldname": "total_shops", "fieldtype": "Int", "width": 120},
        {"label": "Available Shops", "fieldname": "available_shops", "fieldtype": "Int", "width": 120},
        {"label": "Occupied Shops", "fieldname": "occupied_shops", "fieldtype": "Int", "width": 120}
    ]

    # Prepare Data
    data = []
    total_shops = total_available = total_occupied = 0

    for airport in airports:
        data.append({
            "airport": airport.name,
            "total_shops": airport.total_shops,
            "available_shops": airport.available_shops,
            "occupied_shops": airport.occupied_shops
        })
        total_shops += airport.total_shops
        total_available += airport.available_shops
        total_occupied += airport.occupied_shops

    # Generate Chart (Bar Chart for Shop Lease Status per Airport)
    chart = {
        "data": {
            "labels": [row["airport"] for row in data],
            "datasets": [
                {"name": "Available Shops", "values": [row["available_shops"] for row in data]},
                {"name": "Occupied Shops", "values": [row["occupied_shops"] for row in data]}
            ]
        },
        "type": "bar"
    }

    # Summary Section
    summary = [
        {"value": total_shops, "label": "Total Shops", "datatype": "Int", "indicator": "Blue"},
        {"value": total_available, "label": "Total Available Shops", "datatype": "Int", "indicator": "Green"},
        {"value": total_occupied, "label": "Total Occupied Shops", "datatype": "Int", "indicator": "Red"}
    ]

    return columns, data, None, chart, summary
