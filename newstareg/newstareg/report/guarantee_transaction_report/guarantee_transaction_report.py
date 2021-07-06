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
			"label": _("Guarantee Transaction"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Guarantee Transaction",
			"width": 145
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 105
		},
		{
			"label": _("Type"),
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("Reference Party"),
			"fieldname": "reference_party",
			"fieldtype": "Data",
			"width": 110
		},
		{
			"label": _("Paid From"),
			"fieldname": "paid_from",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Paid To"),
			"fieldname": "paid_to",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Paid Amount"),
			"fieldname": "paid_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Fees Amount"),
			"fieldname": "fees_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Fees Account"),
			"fieldname": "fees_account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 100
		},
		{
			"label": _("Notes"),
			"fieldname": "notes",
			"fieldtype": "Data",
			"width": 250
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and a.posting_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and a.posting_date<=%(to_date)s"
	if filters.get("type"):
		conditions += " and a.type=%(type)s"
	item_results = frappe.db.sql("""
				select
						a.name as name,
						a.posting_date as posting_date,
						a.type as type,
						a.reference_party as reference_party,
						CONCAT_WS('-',a.party_from,a.bank_from,a.party_account_from,a.bank_account_from_acc,a.account_from) as paid_from,
						CONCAT_WS('-',a.party_to,a.bank_to,a.account_paid_to,a.bank_account_to_acc,a.acc_to) as paid_to,
						a.paid_amount as paid_amount,
						a.fees_amount as fees_amount,
						a.fees_account as fees_account,
						a.notes as notes					
				from `tabGuarantee Transaction` a 
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
				'posting_date': item_dict.posting_date,
				'type': item_dict.type,
				'reference_party': item_dict.reference_party,
				'paid_from': item_dict.paid_from,
				'paid_to': item_dict.paid_to,
				'paid_amount': item_dict.paid_amount,
				'fees_amount': item_dict.fees_amount,
				'fees_account': item_dict.fees_account,
				'notes': item_dict.notes,
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
