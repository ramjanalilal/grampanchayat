// Copyright (c) 2019, FinForce Consulting LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bill', {
	// refresh: function(frm) {

	// }
	bill_property_number: function(frm) {
		var total_current_tax = 0;
		//frappe.msgprint("Testing...");
		//Taxable tax
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Property Tax",
				fields: "*",
				filters: {"parent": frm.doc.bill_property_number},
				limit_page_length: 30
			},
			callback: function(r) {
				r.message.sort();
				//frappe.msgprint("call back fired");
				if (r.message) {
					for (var row in r.message) {
						var child = frm.add_child("bill_taxes");
						child.tax = r.message[row].tax;
						child.current_amount = r.message[row].amount;
						total_current_tax += child.current_amount;
					}
					refresh_field("bill_taxes");
				}
			}
		});
		frm.doc.total_current_amount = total_current_tax;
	}
});
