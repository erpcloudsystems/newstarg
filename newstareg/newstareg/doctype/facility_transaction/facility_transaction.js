// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Facility Transaction',  'validate',  function(frm) {
    if (cur_frm.doc.commission_based_on == "Percent") {
        cur_frm.doc.commission_amount = cur_frm.doc.commission_rate * cur_frm.doc.facility_amount / 100;
    }
});

frappe.ui.form.on('Facility Transaction',  'with_bank_commission',  function(frm) {
    if (!cur_frm.doc.with_bank_commission) {
        cur_frm.doc.commission_amount = 0;
        cur_frm.doc.commission_account = "";
    }
});