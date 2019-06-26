from __future__ import unicode_literals
import frappe
from frappe.utils import cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day,flt,nowdate
from frappe import throw, msgprint
import json


@frappe.whitelist()
def get_gr_outstanding(gr_no, receipt_name):
	total_amount = frappe.get_value("Goods Receipt", gr_no, "total_amount")
	#frappe.msgprint("Total amount found: " + str(total_amount))
	receipts = frappe.db.get_list("Receipt", filters=[["goods_receipt_number","=", gr_no], ["name", "!=", receipt_name]],fields=["amount"])
	outstanding_amount = total_amount
	for d in receipts:
		outstanding_amount -= d.amount

	return outstanding_amount