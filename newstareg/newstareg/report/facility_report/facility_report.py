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
			"label": _("Facility"),
			"fieldname": "facility",
			"fieldtype": "Link",
			"options": "Facility",
			"width": 120
		},
		{
			"label": _("Contract No"),
			"fieldname": "contract_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Bank"),
			"fieldname": "bank",
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
			"label": _("Credit Limit"),
			"fieldname": "credit_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Booked"),
			"fieldname": "booked_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Remaining"),
			"fieldname": "remaining_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("BG Credit"),
			"fieldname": "bg_credit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("BG Booked"),
			"fieldname": "bg_booked_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("BG Remaining"),
			"fieldname": "bg_remaining_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("LC Credit"),
			"fieldname": "lc_credit_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("LC Booked"),
			"fieldname": "lc_booked_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("LC Remaining"),
			"fieldname": "lc_remaining_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("OD Credit"),
			"fieldname": "od_credit_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("OD Booked"),
			"fieldname": "od_booked_limit",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("OD Remaining"),
			"fieldname": "od_remaining_limit",
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
	if filters.get("type"):
		conditions += " and a.payment_type=%(type)s"
	if filters.get("status"):
		conditions += " and a.cheque_status=%(status)s"
	if filters.get("status_pay"):
		conditions += " and a.cheque_status_pay=%(status_pay)s"
	if filters.get("from_date"):
		conditions += " and a.reference_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and a.reference_date<=%(to_date)s"
	if filters.get("bank"):
		conditions += " and a.bank_acc=%(bank)s"
	if filters.get("mode_of_payment"):
		conditions += " and a.mode_of_payment=%(mode_of_payment)s"
	if filters.get("sad"):
		item_results = frappe.db.sql("""
			select
				a.name as payment_entry,
				a.reference_no as reference_no,
				a.party_type as party_type,
				a.Party as party,
				a.cheque_status as cheque_status,
				a.posting_date as posting_date,
				a.reference_date as reference_date,
				a.clearance_date as clearance_date,
				a.paid_amount as paid_amount,
				a.account as bank,
				a.party_ as party_,
				a.drawn_bank as drawn_bank ,
				a.cheque_type as cheque_type ,
				a.first_beneficiary as first_beneficiary ,
				a.person_name as person_name 
			from `tabPayment Entry` a 
			where
				docstatus =1
				{conditions}
			"""
			.format(conditions=conditions), filters, as_dict=1)
	else:
		item_results = frappe.db.sql("""
					select
							a.name as facility,
							a.contract_no as contract_no,
							a.bank as bank,
							a.start_date as start_date,
							a.end_date as end_date,
							a.credit_limit as credit_limit,
							a.booked_limit as booked_limit,
							a.remaining_limit as remaining_limit,
							a.bg_credit as bg_credit,
							a.bg_booked_limit as bg_booked_limit,
							a.bg_remaining_limit as bg_remaining_limit,
							a.lc_credit_limit as lc_credit_limit,
							a.lc_booked_limit as lc_booked_limit,
							a.lc_remaining_limit as lc_remaining_limit,
							a.od_credit_limit as od_credit_limit,
							a.od_booked_limit as od_booked_limit,
							a.od_remaining_limit as od_remaining_limit,
							CONCAT_WS(' / ',a.assets_credit_limit ,a.assets_booked_limit ,a.assets_remaining_limit ) as assets_credit_limit
							from `tabFacility` a
					where
						 docstatus !=2
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
				'facility': item_dict.facility,
				'contract_no': item_dict.contract_no,
				'bank': item_dict.bank,
				'start_date': item_dict.start_date,
				'end_date': item_dict.end_date,
				'credit_limit': item_dict.credit_limit,
				'booked_limit': item_dict.booked_limit,
				'remaining_limit': item_dict.remaining_limit,
				'bg_booked_limit': item_dict.bg_booked_limit,
				'bg_remaining_limit': item_dict.bg_remaining_limit,
				'bg_credit': item_dict.bg_credit,
				'lc_credit_limit': item_dict.lc_credit_limit,
				'lc_booked_limit': item_dict.lc_booked_limit,
				'lc_remaining_limit': item_dict.lc_remaining_limit,
				'od_credit_limit': item_dict.od_credit_limit,
				'od_booked_limit': item_dict.od_booked_limit,
				'od_remaining_limit': item_dict.od_remaining_limit
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


