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
			"width": 145
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 105
		},
		{
			"label": _("Facility No"),
			"fieldname": "facility",
			"fieldtype": "Link",
			"options": "Facility",
			"width": 140
		},
		{
			"label": _("Facility Type"),
			"fieldname": "facility_type",
			"fieldtype": "Data",
			"width": 110
		},
		{
			"label": _("Facility Amount"),
			"fieldname": "facility_amount",
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"label": _("Commission Amount"),
			"fieldname": "commission_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": _("Start Date"),
			"fieldname": "start_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("End Date"),
			"fieldname": "end_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Bank Account"),
			"fieldname": "bank_account",
			"fieldtype": "Link",
			"options": "Bank Account",
			"width": 300
		},
		{
			"label": _("Current Account"),
			"fieldname": "current_account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 250
		},
		{
			"label": _("Facility Account"),
			"fieldname": "facility_account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 250
		},
		{
			"label": _("Commission Account"),
			"fieldname": "commission_account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 250
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("facility"):
		conditions += " and a.facility=%(facility)s"
	if filters.get("facility_type"):
		conditions += " and a.facility_type=%(facility_type)s"
	if filters.get("from_date"):
		conditions += " and a.start_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and a.end_date<=%(to_date)s"
	if filters.get("current_account"):
		conditions += " and a.current_account=%(current_account)s"
	if filters.get("facility_account"):
		conditions += " and a.facility_account=%(facility_account)s"
	item_results = frappe.db.sql("""
				select
						a.name as name,
						a.facility as facility,
						a.posting_date as posting_date,
						a.facility_type as facility_type,
						a.facility_amount as facility_amount,
						a.bank_account as bank_account,
						a.current_account as current_account,
						a.facility_account as facility_account,
						a.start_date as start_date,
						a.end_date as end_date,
						a.commission_amount as commission_amount,
						a.commission_account as commission_account						
				from `tabFacility Transaction` a 
				where
					 a.docstatus = 1
					{conditions}
				""".format(conditions=conditions), filters, as_dict=1)


	#price_list_names = list(set([item.price_list_name for item in item_results]))

	#buying_price_map = get_price_map(price_list_names, buying=1)
	#selling_price_map = get_price_map(price_list_names, selling=1)

	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'name': item_dict.name,
				'facility': item_dict.facility,
				'posting_date': item_dict.posting_date,
				'facility_type': item_dict.facility_type,
				'facility_amount': item_dict.facility_amount,
				'bank_account': item_dict.bank_account,
				'end_date': item_dict.end_date,
				'start_date': item_dict.start_date,
				'current_account': item_dict.current_account,
				'facility_account': item_dict.facility_account,
				'commission_amount': item_dict.commission_amount,
				'commission_account': item_dict.commission_account,
			}
			result.append(data)

	return result

def get_price_map(price_list_names, buying=0, selling=0):
	price_map = {}

	if not price_list_names:
		return price_map

	rate_key = "Buying Rate" if buying else "Selling Rate"
	price_list_key = "Buying Price List" if buying else "Selling Price List"

	filters = {"name": ("in", price_list_names)}
	if buying:
		filters["buying"] = 1
	else:
		filters["selling"] = 1

	pricing_details = frappe.get_all("Item Price",
		fields = ["name", "price_list", "price_list_rate"], filters=filters)

	for d in pricing_details:
		name = d["name"]
		price_map[name] = {
			price_list_key :d["price_list"],
			rate_key :d["price_list_rate"]
		}

	return price_map
