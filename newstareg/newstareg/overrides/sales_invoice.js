frappe.ui.form.on("Sales Invoice", {

 make_tax: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "newstareg.newstareg.hooks.make_tax",
				callback: function(r) {
					frm.refresh_fields();

				}
			});
	}



});

frappe.ui.form.on("Sales Invoice", {

 tax_type: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "newstareg.newstareg.hooks.validate_taxe_type",
				callback: function(r) {
					frm.refresh_fields();

				}
			});
	}



});

frappe.ui.form.on("Sales Invoice", {

 cancel_tax: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "newstareg.newstareg.hooks.cancel_tax",
				callback: function(r) {
					frm.refresh_fields();

				}
			});
	}



});
