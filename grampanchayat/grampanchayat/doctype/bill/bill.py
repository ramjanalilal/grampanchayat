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

	unbilled_properties = frappe.db.sql(
		'''select name, owner_name, occupier_name from `tabProperty` where billable = 1
		and name not in	(select bill_property_number from `tabBill` where fiscal_year = %s)
		LIMIT 10''',
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
		total_current_amount = 0
		for tax in frappe.get_list("Property Tax", filters={"parent": property.name}, fields={"parent", "tax", "amount"}):
			bill_row = bill.append("bill_taxes")
			bill_row.tax = tax.tax
			bill_row.current_amount = tax.amount
			total_current_amount += tax.amount
			# loan_nfs_row = loan.append("loan_repayments_not_from_salary")
			# loan_nfs_row.nfs_loan_repayment = doc.name
		# Find total current amount and add value here
		bill.total_current_amount = total_current_amount
		bill.total_received = 0
		bill.bill_settled = False
		bill.save(ignore_permissions = True)

	# Administrator to reveiw draft bill report and confirm if all maounts are OK and then submit manually.
	frappe.msgprint(str(len(unbilled_properties)) + " bills created!")
