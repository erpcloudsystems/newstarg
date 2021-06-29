# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_data(filters,columns)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Facility Transaction"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Facility Transaction",
			"width": 80
		},
		{
			"label": _("No"),
			"fieldname": "bank_guarantee_number",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("Beneficiary"),
			"fieldname": "name_of_beneficiary",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("purpose"),
			"fieldname": "bank_guarantee_purpose",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Bank"),
			"fieldname": "bank",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Start Date"),
			"fieldname": "start_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("End Date"),
			"fieldname": "end_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Extend Date"),
			"fieldname": "new_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Status"),
			"fieldname": "bank_guarantee_status",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Bank %"),
			"fieldname": "bank_percent",
			"fieldtype": "Percent",
			"width": 80
		},
		{
			"label": _("Bank Amount"),
			"fieldname": "bank_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Facility %"),
			"fieldname": "facility_percent",
			"fieldtype": "Percent",
			"width": 80
		},
		{
			"label": _("Facility Amount"),
			"fieldname": "facility_amount",
			"fieldtype": "Currency",
			"width": 100
		}
	]
