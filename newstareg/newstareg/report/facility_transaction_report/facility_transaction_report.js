// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Facility Transaction Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname":"facility",
			"label": __("Facility No"),
			"fieldtype": "Link",
			"options":  "Facility",
		},
		{
			"fieldname":"facility_type",
			"label": __("Facility Type"),
			"fieldtype": "Select",
			"options":  ["Landed Cost","OverDraft","Assets"],
		},
		{
			"fieldname":"current_account",
			"label": __("Current Account"),
			"fieldtype": "Link",
			"options":  "Account",
		},
		{
			"fieldname":"facility_account",
			"label": __("Facility Account"),
			"fieldtype": "Link",
			"options":  "Account",
		},
	],
};