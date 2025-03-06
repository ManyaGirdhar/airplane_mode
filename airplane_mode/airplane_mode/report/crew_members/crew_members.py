import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    # Generate Chart Data using ORM
    chart_data = get_chart_data()

    return columns, data, None, chart_data  # Ensure only one chart is returned

def get_columns():
    return [
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Select", "width": 150},
        {"label": "Email", "fieldname": "email", "fieldtype": "Data", "width": 200},
        {"label": "Phone No.", "fieldname": "phone_no", "fieldtype": "Phone", "width": 150},
        {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 250},
        {"label": "Available", "fieldname": "available", "fieldtype": "Check", "width": 100},
        {"label": "Last Modified", "fieldname": "modified", "fieldtype": "Datetime", "width": 180}
    ]

def get_data(filters):
    Employee = frappe.qb.DocType("Employee")

    query = (
        frappe.qb.from_(Employee)
        .select(Employee.employee_name, Employee.designation, Employee.email, 
                Employee.phone_no, Employee.address, Employee.available, Employee.modified)
    )

    if filters and filters.get("designation"):
        query = query.where(Employee.designation == filters.get("designation"))

    query = query.orderby(Employee.modified, order=frappe.qb.desc)

    return query.run(as_dict=True)

# def get_chart_data():
#     designation_data = frappe.get_all("Employee", 
#         fields=["designation", "count(name) as count"], group_by="designation")

#     designation_labels = [row["designation"] for row in designation_data]
#     designation_values = [row["count"] for row in designation_data]

#     return {
#         "title": "Employees per Designation",
#         "data": {"labels": designation_labels, "datasets": [{"name": "Employees", "values": designation_values}]},
#         "type": "bar"
#     }

def get_chart_data():
    # Use ORM to Count Available & Unavailable Employees
    availability_data = frappe.get_all("Employee", 
        fields=["available", "count(name) as count"], group_by="available")

    # Process Pie Chart Data
    availability_labels = ["Available", "Unavailable"]
    availability_values = [
        next((row["count"] for row in availability_data if row["available"] == 1), 0),
        next((row["count"] for row in availability_data if row["available"] == 0), 0)
    ]

    return {
        "title": "Employee Availability",
        "data": {
            "labels": availability_labels,
            "datasets": [{"name": "Availability", "values": availability_values}]
        },
        "type": "pie"  # Ensure it's a pie chart
    }

