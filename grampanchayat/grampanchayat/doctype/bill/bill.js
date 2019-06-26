// Copyright (c) 2019, FinForce Consulting LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bill', {
	// refresh: function(frm) {

	// }
	bill_property_number: function(frm) {
		//frappe.msgprint("Testing...");
		//Taxable tax
		frm.doc.bill_taxes = [];
		frm.doc.total_previous_amount = 0;
		frm.doc.total_current_amount = 0;
		frm.doc.total_bill_amount = 0;
		refresh_field("bill_taxes");
		refresh_field("total_previous_amount");
		refresh_field("total_current_amount");
		refresh_field("total_bill_amount");
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Property Tax",
				fields: "*",
				filters: {"parent": frm.doc.bill_property_number},
				parent: "Property",
				limit_page_length: 30
			},
			callback: function(r) {
				r.message.sort();
				//console.log(r.message);
				//frappe.msgprint("call back fired");
				if (r.message) {
					for (var row in r.message) {
						var child = frm.add_child("bill_taxes");
						child.tax = r.message[row].tax;
						child.previous_amount = r.message[row].previous_amount;
						child.current_amount = r.message[row].amount;
						child.total_amount = child.previous_amount + child.current_amount;
						frm.doc.total_previous_amount += child.previous_amount;
						frm.doc.total_current_amount += child.current_amount;
						frm.doc.total_bill_amount += child.total_amount;
					}
					refresh_field("bill_taxes");
					refresh_field("total_previous_amount");
					refresh_field("total_current_amount");
					refresh_field("total_bill_amount");
				}
			}
		});
	},
	total_received: function(frm) {
		//frappe.msgprint("Testing... if total_received is fired");
		//Taxable tax
		frm.doc.new_pending_amount = frm.doc.total_bill_amount - frm.doc.total_received;
		if (frm.doc.total_bill_amount > frm.doc.total_received) {
			//frappe.msgprint("bill is higher than received");
			frm.set_value("bill_settled", "");
			}
		else {
			//frappe.msgprint("bill is lower than received");
			frm.set_value("bill_settled", "Checked");
			//frappe.msgprint("Final settlement will be recorded");
		}
		refresh_field("new_pending_amount");
		refresh_field("bill_settled");
	}
});
