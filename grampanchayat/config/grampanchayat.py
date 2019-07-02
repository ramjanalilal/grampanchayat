from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		{
			"label": _("Gram Panchayat Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Bill",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Receipt",
					"onboard": 0,
				},
				{
					"type": "doctype",
					"name": "Expense",
					"onboard": 0,
				},
			]
		},
		{
			"label": _("Gram Panchayat Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "Property",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Street Details",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Tax",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Property Type",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Property Category",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Expense Type",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Village Setting",
					"onboard": 1,
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "query-report",
					"name": "Register",
					"doctype": "Bill",
					"onboard": 0,
				},
			]
		},
	]
	return config
