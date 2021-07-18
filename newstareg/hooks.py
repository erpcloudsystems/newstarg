# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe, erpnext
import frappe.defaults
from frappe.utils import cint, flt, getdate, add_days, cstr, nowdate, get_link_to_form, formatdate
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date, get_party_details
from frappe.model.mapper import get_mapped_doc
from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.utils import get_account_currency
from erpnext.stock.doctype.delivery_note.delivery_note import update_billed_amount_based_on_so
from erpnext.projects.doctype.timesheet.timesheet import get_projectwise_timesheet_data
from erpnext.assets.doctype.asset.depreciation \
	import get_disposal_account_and_cost_center, get_gl_entries_on_asset_disposal
from erpnext.stock.doctype.batch.batch import set_batch_nos
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos, get_delivery_note_serial_no
from erpnext.setup.doctype.company.company import update_company_current_month_sales
from erpnext.accounts.general_ledger import get_round_off_account_and_cost_center
from erpnext.accounts.doctype.loyalty_program.loyalty_program import \
	get_loyalty_program_details_with_points, get_loyalty_details, validate_loyalty_points
from erpnext.accounts.deferred_revenue import validate_service_stop_date
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_party_tax_withholding_details
from frappe.model.utils import get_fetch_values
from frappe.contacts.doctype.address.address import get_address_display
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_party_tax_withholding_details

from erpnext.healthcare.utils import manage_invoice_submit_cancel

from six import iteritems
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

# ======================================================================= SalesInvoice =========method to make taxes JV
@frappe.whitelist()
def test(self):
    self.commercial_no = 12

SalesInvoice.validate = test

def validate_taxe_type(self):
	if self.tax_type == "Included":
		for y in self.items:
			group = y.item_group
			item_taxes_template = frappe.db.sql(""" select item_tax_template from `tabItem Tax` where parent=%s """,group,as_dict=1)
			for z in item_taxes_template:
				y.item_tax_template = z.item_tax_template
		for x in self.taxes:
			x.included_in_print_rate = 1
	if self.tax_type == "Excluded":
		for y in self.items:
			group = y.item_group
			item_taxes_template = frappe.db.sql(""" select item_tax_template from `tabItem Tax` where parent=%s """,group,as_dict=1)
			for z in item_taxes_template:
				y.item_tax_template = z.item_tax_template
		for x in self.taxes:
			x.included_in_print_rate = 0
	if self.tax_type == "Commercial":
		for x in self.items:
			x.item_tax_template = ""
		self.set("taxes", [])

@frappe.whitelist()
def make_tax(self):
	default_tax_acc = frappe.db.get_value("Company", self.company, "default_taxes")
	deferred_tax_acc = frappe.db.get_value("Company", self.company, "deferred_tax")
	default_income_account = frappe.db.get_value("Company", self.company, "default_income_account")
	default_receivable_account = frappe.db.get_value("Company", self.company, "default_receivable_account")
	#if self.deferred_tax_jv:
	#	frappe.throw(_("لايمكن انشاء القيود مرة اخرى !"))
	if self.tax_type in ("Included","Excluded"):
		accounts = [
			{
				"doctype": "Journal Entry Account",
				"account": default_tax_acc,
				"debit": 0,
				"credit": self.total_taxes_and_charges,
				"credit_in_account_currency": self.total_taxes_and_charges,
				"user_remark": self.name
			},
			{
				"doctype": "Journal Entry Account",
				"account": deferred_tax_acc,
				"debit": self.total_taxes_and_charges,
				"credit": 0,
				"debit_in_account_currency": self.total_taxes_and_charges,
				"user_remark": self.name
			}
		]
		doc = frappe.get_doc({
			"doctype": "Journal Entry",
			"voucher_type": "Deferred Revenue",
			"sales_invoice": self.name,
			"company": self.company,
			"posting_date": self.posting_date,
			"accounts": accounts,
			"user_remark": _('ترحيل مخصص الضرائب  {0}').format(self.name),
			"total_debit": self.total_taxes_and_charges,
			"total_credit": self.total_taxes_and_charges,
			"remark": _('ترحيل مخصص الضرائب  {0}').format(self.name)

		})
		doc.insert()
		doc.submit()
		djv = doc.name
		docs = frappe.get_doc('Sales Invoice', self.name)
		docs.deferred_tax_jv = djv
		docs.save()
		if not self.serial:
			serial = frappe.get_doc({
				"doctype": "Invoice Serial",
				"link": self.name,
				"status": "Active"
			})
			serial.insert()
			docs.serial = serial.name
		else:
			serial = frappe.get_doc('Invoice Serial', self.serial)
			serial.status = "Active"
			serial.save()
			docs.serial = serial.name
		docs.save()

	elif self.tax_type == "Commercial":
		#taxes_amount = float(self.grand_total) - (float(self.grand_total) / 1.14)
		grand_tax_amount = 0
		for y in self.items:
			group = y.item_group
			item_taxes_template = frappe.db.get_value('Item Tax', {'parent': group}, ['item_tax_template'])
			item_taxes_rate = frappe.db.get_value('Item Tax Template Detail', {'parent': item_taxes_template}, ['tax_rate'])
			tax_rate = item_taxes_rate/100
			grand_tax_amount += tax_rate * y.amount

		accounts = [
			{
				"doctype": "Journal Entry Account",
				"account": default_tax_acc,
				"debit": 0,
				"credit": grand_tax_amount,
				"credit_in_account_currency": grand_tax_amount,
				"user_remark": self.name
			},
			{
				"doctype": "Journal Entry Account",
				"account": default_receivable_account,
				"debit": grand_tax_amount,
				"party_type": "Customer",
				"party": self.customer,
				"credit": 0,
				"debit_in_account_currency": grand_tax_amount,
				"user_remark": self.name
			}
		]
		doc = frappe.get_doc({
			"doctype": "Journal Entry",
			"voucher_type": "Deferred Revenue",
			"sales_invoice": self.name,
			"company": self.company,
			"posting_date": self.posting_date,
			"accounts": accounts,
			"user_remark": _('ترحيل مخصص الضرائب  {0 }').format(self.name),
			"total_debit": grand_tax_amount,
			"total_credit": grand_tax_amount,
			"remark": _('ترحيل مخصص الضرائب  {0}').format(self.name)

		})
		doc.insert()
		doc.submit()
		djv = doc.name
		docs = frappe.get_doc('Sales Invoice', self.name)
		docs.deferred_tax_jv = djv

		if not self.serial:
			serial = frappe.get_doc({
				"doctype": "Invoice Serial",
				"link": self.name,
				"status": "Active"
			})
			serial.insert()
			docs.serial = serial.name
		else:
			serial = frappe.get_doc('Invoice Serial', self.serial)
			serial.status = "Active"
			serial.save()
			docs.serial = serial.name
		docs.save()

@frappe.whitelist()
def cancel_tax(self):
	inv = frappe.get_doc('Sales Invoice', self.name)
	inv.deferred_tax_jv = ""
	jv = frappe.get_doc('Journal Entry', self.deferred_tax_jv)
	jv.sales_invoice = ""
	serial = frappe.get_doc('Invoice Serial', self.serial)
	serial.status = "Cancelled"
	inv.save()
	jv.save()
	serial.save()
	jv.cancel()

SalesInvoice.validate = validate_taxe_type

#========================== End of sales invoice #############################################################







app_name = "newstareg"
app_title = "Newstareg"
app_publisher = "erpcloud.systems"
app_description = "some ERPNext Customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mg@erpcloud.systems"
app_license = "MIT"

override_doctype_class = {
    'SalesInvoice': 'newstareg.newstareg.overrides.sales_invoice.CustomSalesInvoice',
    'ToDo': 'newstareg.newstareg.overrides.sales_invoice.CustomToDo'
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/newstareg/css/newstareg.css"
# app_include_js = "/assets/newstareg/js/newstareg.js"

# include js, css files in header of web template
# web_include_css = "/assets/newstareg/css/newstareg.css"
# web_include_js = "/assets/newstareg/js/newstareg.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "newstareg/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "newstareg.install.before_install"
# after_install = "newstareg.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "newstareg.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"newstareg.tasks.all"
# 	],
# 	"daily": [
# 		"newstareg.tasks.daily"
# 	],
# 	"hourly": [
# 		"newstareg.tasks.hourly"
# 	],
# 	"weekly": [
# 		"newstareg.tasks.weekly"
# 	]
# 	"monthly": [
# 		"newstareg.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "newstareg.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "newstareg.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "newstareg.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

