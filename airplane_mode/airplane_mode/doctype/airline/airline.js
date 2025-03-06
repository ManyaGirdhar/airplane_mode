// Copyright (c) 2025, Manya and contributors
// For license information, please see license.txt


// Assuming there is a "Live Stream" DocType
// with a field `stream_link` that has the link to a YouTube video
frappe.ui.form.on('Airline', {
    refresh(frm) {
       const stream_link = frm.doc.website;
       frm.add_web_link(stream_link, "View Website");
    }
   });
    


