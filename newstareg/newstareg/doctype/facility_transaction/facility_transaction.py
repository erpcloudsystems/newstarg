# Copyright (c) 2021, erpcloud.systems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe, erpnext, json
from frappe import _, scrub, ValidationError, throw
from frappe.utils import flt, comma_or, nowdate, getdate, cint
from erpnext.accounts.utils import get_outstanding_invoices, get_account_currency, get_balance_on
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account
from erpnext.setup.utils import get_exchange_rate
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.hr.doctype.expense_claim.expense_claim import update_reimbursed_amount
from erpnext.accounts.doctype.bank_account.bank_account import get_party_bank_account, get_bank_account_details
from erpnext.controllers.accounts_controller import AccountsController, get_supplier_block_status
from erpnext.accounts.doctype.invoice_discounting.invoice_discounting import get_party_account_based_on_invoice_discounting
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from frappe.utils import add_to_date, now, nowdate

class FacilityTransaction(Document):
	def on_submit(self):
		self.make_journal_entry()
		self.update_facility()
		self.update_facility_total()

	def on_cancel(self):
		self.update_facility_on_cancel()
		self.update_facility_total_on_cancel()

	def make_journal_entry(self):
		if self.with_bank_commission:
			accounts = [
				{
				"doctype": "Journal Entry Account",
				"account": self.current_account,
				"credit": 0,
				"debit": self.facility_amount,
				"debit_in_account_currency": self.facility_amount,
				"user_remark": self.name
				},
				{
				"doctype": "Journal Entry Account",
				"account": self.commission_account,
				"credit": 0,
				"debit": self.commission_amount,
				"debit_in_account_currency": self.commission_amount,
				"user_remark": self.name
				},
				{
				"doctype": "Journal Entry Account",
				"account": self.facility_account,
				"credit": self.facility_amount,
				"debit": 0,
				"credit_in_account_currency": self.facility_amount,
				"user_remark": self.name
				},
				{
				"doctype": "Journal Entry Account",
				"account": self.current_account,
				"credit": self.commission_amount,
				"debit": 0,
				"credit_in_account_currency": self.commission_amount,
				"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype" : "Journal Entry",
				"voucher_type" : "Bank Entry",
				"facility_transaction" : self.name,
				"cheque_no" : self.name,
				"cheque_date" : self.posting_date,
				"posting_date" : self.posting_date,
				"accounts" : accounts

			})
			doc.insert()
			doc.submit()

		if not self.with_bank_commission:
			accounts = [
				{
				"doctype": "Journal Entry Account",
				"account": self.current_account,
				"credit": 0,
				"debit": self.facility_amount,
				"debit_in_account_currency": self.facility_amount,
				"user_remark": self.name
				},
				{
				"doctype": "Journal Entry Account",
				"account": self.facility_account,
				"credit": self.facility_amount,
				"debit": 0,
				"credit_in_account_currency": self.facility_amount,
				"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype" : "Journal Entry",
				"voucher_type" : "Bank Entry",
				"facility_transaction" : self.name,
				"cheque_no" : self.name,
				"cheque_date" : self.posting_date,
				"posting_date" : self.posting_date,
				"accounts" : accounts

			})
			doc.insert()
			doc.submit()

	def update_facility(self):
		if self.facility_type == "Landed Cost":
			current_booked = frappe.db.get_value("Facility", self.facility, "lc_booked_limit")
			new_booked = current_booked + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'lc_booked_limit', new_booked)
			current_credit = frappe.db.get_value("Facility", self.facility, "lc_credit_limit")
			new_remaining = current_credit - new_booked
			frappe.db.set_value('Facility', self.facility, 'lc_remaining_limit', new_remaining)
			if new_booked > current_credit:
				frappe.throw(_("Cannot Exceed The Credit Limit For Landed Cost Facility"))

		if self.facility_type == "OverDraft":
			current_booked = frappe.db.get_value("Facility", self.facility, "od_booked_limit")
			new_booked = current_booked + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'od_booked_limit', new_booked)
			current_credit = frappe.db.get_value("Facility", self.facility, "od_credit_limit")
			new_remaining = current_credit - new_booked
			frappe.db.set_value('Facility', self.facility, 'od_remaining_limit', new_remaining)
			if new_booked > current_credit:
				frappe.throw(_("Cannot Exceed The Credit Limit For OverDraft Facility"))

		if self.facility_type == "Assets":
			current_booked = frappe.db.get_value("Facility", self.facility, "assets_booked_limit")
			new_booked = current_booked + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'assets_booked_limit', new_booked)
			current_credit = frappe.db.get_value("Facility", self.facility, "assets_credit_limit")
			new_remaining = current_credit - new_booked
			frappe.db.set_value('Facility', self.facility, 'assets_remaining_limit', new_remaining)
			if new_booked > current_credit:
				frappe.throw(_("Cannot Exceed The Credit Limit For Assets Facility"))

	def update_facility_total(self):
		current_bg_booked = frappe.db.get_value("Facility", self.facility, "bg_booked_limit")
		current_lc_booked = frappe.db.get_value("Facility", self.facility, "lc_booked_limit")
		current_od_booked = frappe.db.get_value("Facility", self.facility, "od_booked_limit")
		current_assets_booked = frappe.db.get_value("Facility", self.facility, "assets_booked_limit")
		current_total_booked = current_bg_booked + current_lc_booked + current_od_booked + current_assets_booked
		frappe.db.set_value('Facility', self.facility, 'booked_limit', current_total_booked)
		current_total_credit = frappe.db.get_value("Facility", self.facility, "credit_limit")
		new_remaining_value = current_total_credit - current_total_booked
		frappe.db.set_value('Facility', self.facility, 'remaining_limit', new_remaining_value)

	def update_facility_on_cancel(self):
		if self.facility_type == "Landed Cost":
			booked = frappe.db.get_value("Facility", self.facility, "lc_booked_limit")
			remaining = frappe.db.get_value("Facility", self.facility, "lc_remaining_limit")
			x = booked - self.facility_amount
			y = remaining + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'lc_booked_limit', x)
			frappe.db.set_value('Facility', self.facility, 'lc_remaining_limit', y)

		if self.facility_type == "OverDraft":
			booked = frappe.db.get_value("Facility", self.facility, "od_booked_limit")
			remaining = frappe.db.get_value("Facility", self.facility, "od_remaining_limit")
			x = booked - self.facility_amount
			y = remaining + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'od_booked_limit', x)
			frappe.db.set_value('Facility', self.facility, 'od_remaining_limit', y)

		if self.facility_type == "Assets":
			booked = frappe.db.get_value("Facility", self.facility, "assets_booked_limit")
			remaining = frappe.db.get_value("Facility", self.facility, "assets_remaining_limit")
			x = booked - self.facility_amount
			y = remaining + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'assets_booked_limit', x)
			frappe.db.set_value('Facility', self.facility, 'assets_remaining_limit', y)

	def update_facility_total_on_cancel(self):
			booked = frappe.db.get_value("Facility", self.facility, "booked_limit")
			remaining = frappe.db.get_value("Facility", self.facility, "remaining_limit")
			x = booked - self.facility_amount
			y = remaining + self.facility_amount
			frappe.db.set_value('Facility', self.facility, 'booked_limit', x)
			frappe.db.set_value('Facility', self.facility, 'remaining_limit', y)

	pass
