# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
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
			"label": _("Contract"),
			"fieldname": "contract",
			"fieldtype": "Link",
			"options": "Contract",
			"width": 120
		},
		{
			"label": _("Party"),
			"fieldname": "party_name",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Contract No"),
			"fieldname": "contract_no",
			"fieldtype": "Data",
			"width": 100
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
			"width": 120
		},
		{
			"label": _("Unit Type"),
			"fieldname": "unit_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Unit"),
			"fieldname": "unit",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Rent Value"),
			"fieldname": "rent_value_",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Rent Cycle"),
			"fieldname": "rent_cycle",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Annual Increase"),
			"fieldname": "annual_increase",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Annual Increase Type"),
			"fieldname": "annual_increase_type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Insurance Value"),
			"fieldname": "insurance_value",
			"fieldtype": "Currency",
			"width": 120
		}

	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and a.end_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and a.end_date<=%(to_date)s"
	if filters.get("sad"):
		item_results = frappe.db.sql("""
			select
				a.name as contract,
				a.party_name as party_name,
				a.contract_no as contract_no,
				a.start_date as start_date,
				a.end_date as end_date,
				a.unit_type as unit_type,
				a.unit as unit,
				a.rent_value_ as rent_value_,
				a.rent_cycle as rent_cycle,
				a.annual_increase as annual_increase,
				a.annual_increase_type as annual_increase_type,
				a.insurance_value as insurance_value
			from `tabContract` a 
			where
				docstatus =1
				{conditions}
			"""
			.format(conditions=conditions), filters, as_dict=1)
	else:
		item_results = frappe.db.sql("""
					select
							a.name as contract,
							a.party_name as party_name,
							a.contract_no as contract_no,
							a.start_date as start_date,
							a.end_date as end_date,
							a.unit_type as unit_type,
							a.warehouse as unit,
							a.rent_value_ as rent_value_,
							a.rent_cycle as rent_cycle,
							a.annual_increase as annual_increase,
							a.annual_increase_type as annual_increase_type,
							a.insurance_value as insurance_value							
							from `tabContract` a
					where
						 contract_type ="Lease"
						{conditions}
					"""
									 .format(conditions=conditions), filters, as_dict=1)


	#price_list_names = list(set([item.price_list_name for item in item_results]))

	#buying_price_map = get_price_map(price_list_names, buying=1)
	#selling_price_map = get_price_map(price_list_names, selling=1)

	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'contract': item_dict.contract,
				'party_name': item_dict.party_name,
				'contract_no': item_dict.contract_no,
				'start_date': item_dict.start_date,
				'end_date': item_dict.end_date,
				'unit_type': item_dict.unit_type,
				'unit': item_dict.unit,
				'rent_value_': item_dict.rent_value_,
				'rent_cycle': item_dict.rent_cycle,
				'annual_increase': item_dict.annual_increase,
				'annual_increase_type': item_dict.annual_increase_type,
				'insurance_value': item_dict.insurance_value
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


