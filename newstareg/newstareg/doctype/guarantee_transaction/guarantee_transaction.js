// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Guarantee Transaction', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("reference_party_type", function() {
			return {
				filters: [
					["DocType", "name", "in", ["Customer","Supplier"]]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("party_type_from", function() {
			return {
				filters: [
					["DocType", "name", "in", ["Customer","Supplier"]]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("party_type_to", function() {
			return {
				filters: [
					["DocType", "name", "in", ["Customer","Supplier"]]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("bank_account_from", function() {
			return {
				filters: [
					["Bank Account","bank", "in", frm.doc.bank_from]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("bank_account_to", function() {
			return {
				filters: [
					["Bank Account","bank", "in", frm.doc.bank_to]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("bank_account_from_acc", function() {
			return {
				filters: [
					["Account","account_type", "in", "Bank"]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("bank_account_to_acc", function() {
			return {
				filters: [
					["Account","account_type", "in", "Bank"]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("party_account_from", function() {
			return {
				filters: [
					["Account","account_type", "in", ["Payable","Receivable"]]
				]
			};
		});
	}
});
frappe.ui.form.on("Guarantee Transaction", {
	setup: function(frm) {
		frm.set_query("account_paid_to", function() {
			return {
				filters: [
					["Account","account_type", "in", ["Payable","Receivable"]]
				]
			};
		});
	}
});