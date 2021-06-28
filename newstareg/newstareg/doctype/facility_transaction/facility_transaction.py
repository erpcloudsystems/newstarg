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

	def make_journal_entry(self):
		if self.commission_based_on:
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

		if not self.commission_based_on:
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

	pass
