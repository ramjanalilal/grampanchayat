// Copyright (c) 2019, FinForce Consulting LLP and contributors
// For license information, please see license.txt
frappe.ui.form.on('Property', {
	onload: function(frm) {
		frm.set_query("property_type", function() {
			return {
				filters: {
					property_category: frm.doc.property_category
				}
			}
		})
	},
	property_category: function(frm) {
		frm.set_value("property_type", "");
	},
	owner_name: function(frm) {
		if (!frm.doc.occupier_name) {
			frm.set_value("occupier_name", frm.doc.owner_name);
		}
	},
	get_property_taxes: function(frm) {
		var taxable_tax_total = 0;
		//frappe.msgprint("Testing...");
		//Taxable tax
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Tax",
				fields: "*",
				filters: {"taxable_tax": 1},
				limit_page_length: 30
			},
			callback: function(r) {
				r.message.sort();
				//frappe.msgprint("call back fired");
				if (r.message) {
					for (var row in r.message) {
						var child = frm.add_child("property_tax");
						child.tax = r.message[row].tax_name;
						if (r.message[row].default_rate == 0) {
							//frappe.msgprint("Default rate " + r.message[row].default_rate + " is set for " + r.message[row].tax_name);
							child.amount = r.message[row].percentage_of_property_value * frm.doc.property_value / 100;
						} else {
							//frappe.msgprint("Default rate " + r.message[row].default_rate + " is set for " + r.message[row].tax_name);
							child.amount = r.message[row].default_rate;
						}
						taxable_tax_total += child.amount
					}
					refresh_field("property_tax");
				}
			}
		});
		// Super tax
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Tax",
				fields: "*",
				filters: {"taxable_tax": 0},
				limit_page_length: 30
			},
			callback: function(r) {
				r.message.sort();
				//frappe.msgprint("call back fired");
				if (r.message) {
					for (var row in r.message) {
						var child = frm.add_child("property_tax");
						child.tax = r.message[row].tax_name;
						child.amount = taxable_tax_total * r.message[row].taxable_tax_percentage / 100;
					}
					refresh_field("property_tax");
				}
			}
		});
	}
});
