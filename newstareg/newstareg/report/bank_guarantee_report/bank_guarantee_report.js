// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Bank Guarantee Report"] = {
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
			"fieldname":"bank_guarantee_purpose",
			"label": __("Purpose"),
			"fieldtype": "Select",
			"options":  ["شيك","شيك ضمان","شيك امانات","شيك تسهيل"],
		},
		{
			"fieldname":"type_of_letter_of_guarantee",
			"label": __("Type"),
			"fieldtype": "Select",
			"options":  ["Cheque","Cash","Bank Guarantee"]
		}
	]
};

