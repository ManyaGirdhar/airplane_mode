// Copyright (c) 2025, Manya and contributors
// For license information, please see license.txt


frappe.ui.form.on("Airplane Ticket", {
    refresh: function(frm) {  
        frm.add_custom_button("Assign Seat", function() {
            let d = new frappe.ui.Dialog({
                title: 'Select Seat',
                fields: [
                    {
                        label: 'Seat',
                        fieldname: 'seat',
                        fieldtype: 'Data'
                    },
                ],
                size: 'small', 
                primary_action_label: 'Assign Seat',
                primary_action(values) {
                    if (values.seat) {
                        frm.set_value("seat", values.seat); 
                        frm.refresh_field("seat");
                    }
                    d.hide();
                }
            });

            d.show();
        }, "Actions");
    }
});

// frappe.ui.form.on("Airplane Flight", {
//     gate_number: function(frm) {
//         if (!frm.doc.__islocal) {  // Ensure it's an existing document
//             frappe.call({
//                 method: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_numbers",
//                 args: {
//                     flight_name: frm.doc.name,
//                     new_gate_number: frm.doc.gate_number
//                 },
//                 callback: function(response) {
//                     frappe.show_alert({
//                         message: __("Gate number update triggered in background."),
//                         indicator: "blue"
//                     });
//                 }
//             });
//         }
//     }
// });

// // Listen for real-time updates and update UI first
// frappe.realtime.on("refresh_tickets", function(data) {
//     if (cur_frm.doc.name === data.flight_name) {
//         cur_frm.set_value("gate_number", data.new_gate_number);
//         cur_frm.refresh_field("gate_number");

//         frappe.show_alert({
//             message: __("Gate number updated to " + data.new_gate_number),
//             indicator: "green"
//         });
//     }
// });
