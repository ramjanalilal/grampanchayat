// Copyright (c) 2019, FinForce Consulting LLP and contributors
// For license information, please see license.txt
frappe.ui.form.on('Property', {
	// refresh: function(frm) {
	// }
	setup: function(frm) {
		frm.custom_make_buttons = {
			'All Pending Bills': 'All Pending Bills',
			'Pending Bill': 'Pending Bill'
		}
	},
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
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Tax",
				limit_page_length = 30
			},
			callback: function(r) {
				console.log(r);
				if (r.message) {
					for (var row in r.message) {
						var child = frm.add_child("property_tax");
						frappe.model.set_value(child.doctype, child.name, "tax", r.message.[row].tax);
						if (!taxable_tax) {
							if (default_rate = 0) {
								frappe.model.set_value(child.doctype, child.name, "amount", r.message.task[row].percentage_of_property_value * doc.property_value);
							} else {
								frappe.model.set_value(child.doctype, child.name, "amount", r.message.task[row].default_rate);
							}
						}
						refresh_field("property_tax");
					}
				}
			}
		});
	}
=======
    // refresh: function(frm) {
    // }
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
   /* get_property_taxes: function(frm) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Tax",
                limit_page_length = 30
            },
            callback: function(r) {
                console.log(r);
                if (r.message) {
                    for (var row in r.message) {
                        var child = frm.add_child("property_tax");
                        frappe.model.set_value(child.doctype, child.name, "tax", r.message.[row].tax);
                        if (!taxable_tax) {
                            if (default_rate = 0) {
                                frappe.model.set_value(child.doctype, child.name, "amount", r.message.task[row].percentage_of_property_value * doc.property_value);
                            } else {
                                frappe.model.set_value(child.doctype, child.name, "amount", r.message.task[row].default_rate);
                            }
                        }
                        refresh_field("property_tax");
                    }
                }
            }
        });
    }*/
});
