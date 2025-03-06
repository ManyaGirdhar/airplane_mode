// Copyright (c) 2025, Manya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lease Contract", {
    onload: function(frm) {
        if (!frm.doc.rent_amount) {  // Only set if it's empty
            frappe.call({
                method: "frappe.client.get_single_value",
                args: {
                    doctype: "Global Settings",
                    field: "default_rent_amount"
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value("rent_amount", response.message);
                    }
                }
            });
        }
    }
});
