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
		//frappe.msgprint("Testing...");
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Tax",
				fields: ["tax_name", "taxable_tax", "default_rate", "percentage_of_property_value"],
				limit_page_length: 30
			},
			callback: function(r) {
				//frappe.msgprint("call back fired");
				//console.log(r);
				if (r.message) {
					for (var row in r.message) {
						console.log(frm.doc.property_value);
						var child = frm.add_child("property_tax");
						child.tax = r.message[row].tax_name;
						if (r.message[row].default_rate = 0) {
							child.amount = r.message[row].percentage_of_property_value * frm.doc.property_value;
						} else {
							console.log(r.message[row].tax_name);
							console.log(r.message[row].percentage_of_property_value);
							console.log(r.message[row].default_rate);
							child.amount = r.message[row].default_rate;
						}
					}
					refresh_field("property_tax");
				}
			}
		});
	}
});
