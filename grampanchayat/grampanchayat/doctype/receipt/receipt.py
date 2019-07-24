# -*- coding: utf-8 -*-
# Copyright (c) 2019, FinForce Consulting LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Receipt(Document):
	def on_submit(self):
		frappe.set_value("Bill", self.bill_being_settled, "total_received", self.total_received + self.amount_received)
		frappe.set_value("Bill", self.bill_being_settled, "new_pending_amount", self.total_bill_amount - (self.total_received + self.amount_received))
		if (self.total_bill_amount - (self.total_received + self.amount_received) == 0):
			frappe.set_value("Bill", self.bill_being_settled, "bill_settled", True)
		for receipt_tax in self.receipt_tax:
			bill_tax_name = ""
			# Find bill tax name from Bill Tax using bill_being_settled
			bill_tax_name = frappe.db.get_value("Bill Tax", {"parent": self.bill_being_settled, "tax": receipt_tax.tax}, "name")
			# frappe.msgprint("Bill tax loaded: " + bill_tax_name + " for receipt tax: " + receipt_tax.tax)
			# Update previous and current amounts in bill based on previous and current receipt
			frappe.set_value("Bill Tax", bill_tax_name, "previous_amount", receipt_tax.bill_previous_amount - receipt_tax.previous_amount)
			frappe.set_value("Bill Tax", bill_tax_name, "current_amount", receipt_tax.bill_current_amount - receipt_tax.current_amount)
	def on_cancel(self):
		frappe.set_value("Bill", self.bill_being_settled, "total_received", self.total_received)
		frappe.set_value("Bill", self.bill_being_settled, "new_pending_amount", self.total_bill_amount - self.total_received)
		if (self.total_bill_amount - (self.total_received + self.amount_received) != 0):
			frappe.set_value("Bill", self.bill_being_settled, "bill_settled", False)
		for receipt_tax in self.receipt_tax:
			bill_tax_name = ""
			# Find bill tax name from Bill Tax using bill_being_settled
			bill_tax_name = frappe.db.get_value("Bill Tax", {"parent": self.bill_being_settled, "tax": receipt_tax.tax}, "name")
			# frappe.msgprint("Bill tax loaded: " + bill_tax_name + " for receipt tax: " + receipt_tax.tax)
			# Update previous and current amounts in bill based on previous and current receipt
			frappe.set_value("Bill Tax", bill_tax_name, "previous_amount", receipt_tax.bill_previous_amount + receipt_tax.previous_amount)
			frappe.set_value("Bill Tax", bill_tax_name, "current_amount", receipt_tax.bill_current_amount + receipt_tax.current_amount)
