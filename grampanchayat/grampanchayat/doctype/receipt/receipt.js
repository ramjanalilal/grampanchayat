// Copyright (c) 2019, FinForce Consulting LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Receipt', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
		frm.set_query("bill_being_settled", function() {
			return {
				 filters: { docstatus: 1, bill_settled: 0 } 
			};
		})
	},
	amount_received: function(frm) {
		if (frm.doc.amount_received > (frm.doc.total_bill_amount - frm.doc.total_received)) {
			frm.doc.amount_received = 0
			frm.doc.receipt_tax = []
			frm.refresh_fields()
			frappe.throw(__("Amount received cannot be more than pending amount. Please check the pending amount and update amount received!"))
		}

		var amount_remaining = frm.doc.amount_received;
		var prev_amount_remaining = frm.doc.amount_received;
		// Allocate amount to previous amounts
		$.each(frm.doc.receipt_tax || [], function(i, row) {
			frappe.msgprint("prev test" + prev_amount_remaining + " " + amount_remaining);
			prev_amount_remaining = amount_remaining;
			amount_remaining -= row.bill_previous_amount;
			row.previous_amount = 0;
			if(flt(amount_remaining) > 0)
				row.previous_amount = row.bill_previous_amount;
			else if (amount_remaining <= 0 && prev_amount_remaining > 0) {
				row.previous_amount = prev_amount_remaining;
				prev_amount_remaining = 0;
			}
		});
		// Allocate amount to current amounts
		$.each(frm.doc.receipt_tax || [], function(i, row) {
			frappe.msgprint("curr test" + prev_amount_remaining + " " + amount_remaining);
			prev_amount_remaining = amount_remaining;
			amount_remaining -= row.bill_current_amount;
			row.current_amount = 0;
			if(flt(amount_remaining) > 0)
				row.current_amount = row.bill_current_amount;
			else if (amount_remaining <= 0 && prev_amount_remaining > 0) {
				row.current_amount = prev_amount_remaining;
				prev_amount_remaining = 0;
			}
			row.total_amount = row.previous_amount + row.current_amount;
		});
		frm.refresh_fields()

		// frm.doc.receipt_tax.forEach((tax) => {
		// 	frappe.msgprint("test" + prev_amount_remaining + " " + amount_remaining);
		// 	prev_amount_remaining = amount_remaining;
		// 	amount_remaining -= tax.bill_current_amount;
		// 	if (amount_remaining > 0) {
		// 		frappe.model.set_value("Receipt Tax", tax.docname,
		// 			"current_amount", tax.current_amount);
		// 	} else if (amount_remaining == 0 && prev_amount_remaining == 0) {
		// 		frappe.model.set_value("Receipt Tax", tax.docname,
		// 			"current_amount", prev_amount_remaining);
		// 		amount_remaining = 0;
		// 	}
		// });
		// Upon submit update bill
	},
	bill_being_settled: function(frm) {
		// frappe.msgprint("Testing...");
		//Taxable tax
		frm.doc.receipt_tax = [];
		refresh_field("receipt_tax");
		if (frm.doc.bill_being_settled) {
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Bill Tax",
					fields: ["parent", "tax", "previous_amount", "current_amount"],
					filters: {"parent": frm.doc.bill_being_settled},
					parent: "Bill",
					order_by: "idx"
				},
				callback: function(r) {
					//console.log(r.message);
					//frappe.msgprint("call back fired");
					if (r.message) {
						for (var row in r.message) {
							var child = frm.add_child("receipt_tax");
							// frappe.msgprint("current amount: " + r.message[row].current_amount)
							child.tax = r.message[row].tax;
							// child.previous_amount = r.message[row].previous_amount;
							// child.current_amount = r.message[row].current_amount;
							// child.total_amount =  r.message[row].previous_amount + r.message[row].current_amount;
							child.bill_previous_amount = r.message[row].previous_amount;
							child.bill_current_amount = r.message[row].current_amount;
						}
						refresh_field("receipt_tax");
					}
				}
			});
		}
		else {
			frm.set_value("fiscal_year", "");
			frm.set_value("occupier", "");
		}
	},
});
