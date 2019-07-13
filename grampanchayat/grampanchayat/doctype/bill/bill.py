# -*- coding: utf-8 -*-
# Copyright (c) 2019, FinForce Consulting LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
import frappe
import datetime
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, format_datetime,get_datetime_str,now_datetime,add_days,today,formatdate,date_diff,getdate,add_months,flt, nowdate, fmt_money, add_to_date, DATE_FORMAT, rounded
from frappe import _
from operator import itemgetter

class Bill(Document):
	pass

@frappe.whitelist()
def create_bills_for_year(billdate=None):
	if billdate == None:
		billdate = getdate(today())
		# frappe.msgprint("None billdate found. Setting: " + str(billdate))
	# frappe.msgprint("billdate: " + str(billdate))

	# Find bill year
	fiscal_year = frappe.get_list("Fiscal Year", fields={"name", "year_start_date", "year_end_date"}, filters={"disabled": 0, "year_start_date": ("<=", billdate), "year_end_date": (">=", billdate) }, limit_page_length=1)
	# frappe.msgprint("Fiscal year selected: " + str(fiscal_year))

	# Find all property for which bill is not created
	unbilled_properties = frappe.db.sql(
		'''select name from `tabProperty` where billable = 1
		and name not in	(select bill_property_number from `tabBill` where fiscal_year = %s)''',
		(fiscal_year[0].name),
		as_dict=1
		)
	frappe.msgprint("Number of properties found to create bills " + str(len(unbilled_properties)))

	# Get preivous_amount into a list
	# Assumed that all receipts in system will be considered for calculations
	property_tax_previous_amount_list = frappe.db.sql('''select b.bill_property_number, bt.tax,
		sum(bt.current_amount) - sum(ifnull(total_received, 0)) as tax_previous_amount
		from `tabBill` b
		inner join `tabBill Tax` bt on b.name = bt.parent
		left outer join `tabReceipt Tax` rt on rt.tax = bt.tax and rt.docstatus = 1
		where b.docstatus = 1 and b.bill_date <= %s
		group by bill_property_number''', (billdate))

	unbilled_properties = frappe.db.sql(
		'''select name, owner_name, occupier_name from `tabProperty` where billable = 1
		and name not in	(select bill_property_number from `tabBill` where fiscal_year = %s)
		LIMIT 50''',
		(fiscal_year[0].name),
		as_dict=1
		)
	frappe.msgprint("Number of bills that will be created " + str(len(unbilled_properties)))

	# Create one bill at a time for each non-created property
	for property in unbilled_properties:
		# frappe.msgprint("Property loaded to create the bill: " + property.name + " fy:" + fiscal_year[0].name )
		bill = frappe.new_doc('Bill')
		bill.bill_date = billdate
		bill.fiscal_year = fiscal_year[0].name
		bill.bill_property_number = property.name
		# # Get all taxes for the property and add them to the bill taxes table
		# bill.taxes = 
		property_tax_list = frappe.get_list("Property Tax", filters={"parent": property.name}, fields={"parent", "previous_amount", "tax", "amount"})
		total_current_amount = 0
		for tax in property_tax_list:
			tax_previous_amount = 0
			bill_row = bill.append("bill_taxes")
			bill_row.tax = tax.tax
			#tom_index = next((index for (index, d) in enumerate(lst) if d["name"] == "Tom"), None)
			for property_tax_previous_amount in property_tax_list:
				if property_tax_previous_amount["bill_property_number"] == property.name and property_tax_previous_amount["tax"]:
					frappe.msgprint("Property Previous tax: " + str(property_tax_previous_amount["tax"]) )
					# previous_amount_index = itemgetter(*mykeys)(mydict) next((index for (index, d) in enumerate(previous_amount_list) if d["bill_property_number"] == property.name), None)
			# if previous_amount_index:
			# 	tax_previous_amount = previous_amount_list[previous_amount_index].tax_previous_amount
			bill_row.previous_amount = tax_previous_amount
			bill_row.current_amount = tax.amount
			bill_row.total_amount = tax_previous_amount + tax.amount
			bill_row.original_previous_amount = tax_previous_amount
			bill_row.original_current_amount = tax.amount
			total_previous_amount += tax_previous_amount
			total_current_amount += tax.amount

		# Find total current amount and add value here
		bill.total_previous_amount = total_previous_amount
		bill.total_current_amount = total_current_amount
		bill.total_bill_amount = total_previous_amount + total_current_amount
		bill.total_received = 0
		bill.bill_settled = False
		bill.save(ignore_permissions = True)

	# Administrator to reveiw draft bill report and confirm if all maounts are OK and then submit manually.
	frappe.msgprint(str(len(unbilled_properties)) + " bills created!")
