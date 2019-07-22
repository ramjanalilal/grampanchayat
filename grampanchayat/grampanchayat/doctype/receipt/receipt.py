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
	def on_cancel(self):
		frappe.set_value("Bill", self.bill_being_settled, "total_received", self.total_received)
		frappe.set_value("Bill", self.bill_being_settled, "new_pending_amount", self.total_bill_amount - self.total_received)
		if (self.total_bill_amount - (self.total_received + self.amount_received) != 0):
			frappe.set_value("Bill", self.bill_being_settled, "bill_settled", False)

@frappe.whitelist()
def on_submit(self):
	if method == "on_submit":
		frappe.set_value("Bill", self.bill_being_settled, "total_received", self.total_received + self.amount_received)
		frappe.set_value("Bill", self.bill_being_settled, "new_pending_amount", self.total_bill_amount - (self.total_received + self.amount_received))
	elif method == "on_cancel":
		frappe.set_value("Bill", self.bill_being_settled, "total_received", self.total_received - self.amount_received)
		frappe.set_value("Bill", self.bill_being_settled, "new_pending_amount", self.total_bill_amount - (self.total_received - self.amount_received))
