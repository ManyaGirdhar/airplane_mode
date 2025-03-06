// Copyright (c) 2025, Manya and contributors
// For license information, please see license.txt


frappe.ui.form.on("Airplane Flight", {
    refresh: function(frm) {  
        frm.add_custom_button("Update Gate Number", function() {
            let d = new frappe.ui.Dialog({
                title: 'Update Gate Number',
                fields: [
                    {
                        label: 'New Gate Number',
                        fieldname: 'new_gate_number',
                        fieldtype: 'Data',
                        reqd: 1 // Make it required
                    },
                ],
                size: 'small', 
                primary_action_label: 'Update',
                primary_action(values) {
                    if (values.new_gate_number) {
                        // Update the gate_number field in Airplane Flight
                        frm.set_value("gate_number", values.new_gate_number);
                        frm.refresh_field("gate_number");

                        // Call backend function to update all linked tickets
                        frappe.call({
                            method: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gate_numbers",
                            args: {
                                flight_name: frm.doc.name,
                                gate_number: values.new_gate_number
                            },
                            callback: function (r) {
                                if (!r.exc) {
                                    frappe.msgprint("Gate number updated for all linked tickets.");
                                    frm.save();  // Save the document to persist changes
                                }
                            }
                        });
                    }
                    d.hide();
                }
            });

            d.show();
        }, "Actions");

    },


    onload: function(frm) {  
        // Ensure crew_members is a child table before setting filters
        if (frm.fields_dict["crew_members"] && frm.fields_dict["crew_members"].grid) {
            frm.fields_dict["crew_members"].grid.get_field("employee_id").get_query = function(doc, cdt, cdn) {
                return {
                    filters: {
                        available: 1  // Ensures only employees with 'available' checked are listed
                    }
                };
            };
        }

        // Ensure crew (MultiSelect field) filters only available employees
        if (frm.fields_dict["crew"]) {
            frm.set_query("crew", function() {
                return {
                    filters: {
                        available: 1  // Ensures only employees with 'available' checked are listed
                    }
                };
            });
        }}

});


