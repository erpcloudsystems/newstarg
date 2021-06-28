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
			"options":  "\nBank Guarantee\nCheque\nCash\nDeduction",
		},
		{
			"fieldname":"bg_type",
			"label": __("Provider"),
			"fieldtype": "Select",
			"options":  "\nReceiving\nProviding",
		},
		{
			"fieldname":"status_of_letter_of_guarantee",
			"label": __("Type"),
			"fieldtype": "Select",
			"options":  "\nInitial\nAdvanced Payment\nFinal"
		},
		{
			"fieldname":"bank",
			"label": __("Bank"),
			"fieldtype": "Link",
			"options":  "Bank"
		},

	],
         "formatter": function (value, row, column, data, default_formatter) {
                value = default_formatter(value, row, column, data);

                if (column.fieldname == "bank_percent" && data && data.bank_percent > 0) {
                    value = "<span style='color:red'>" + value + "</span>";
                }
                else if (column.fieldname == "bank_percent" && data && data.bank_percent == 0) {
                    value = "<span style='color:green'>" + value + "</span>";
                }

                return value;
            }
};

