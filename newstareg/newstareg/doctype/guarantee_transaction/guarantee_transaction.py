# Copyright (c) 2021, erpcloud.systems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe, json
from frappe.model.document import Document
from frappe import _
from frappe.desk.search import sanitize_searchfield
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from frappe.utils import add_to_date, now, nowdate

class GuaranteeTransaction(Document):
	def on_submit(self):
		self.make_journal_entry()

	def make_journal_entry(self):

		# Account From - Account To - Without Fees
		if not self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and not self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.acc_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# Account From - Account To - With Fees
		if not self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and not self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.acc_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Party - Account To - Without Fees
		if self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and not self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.acc_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"party_type": self.party_type_from,
					"party": self.party_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Party - Account To - With Fees
		if self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and not self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.acc_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"party_type": self.party_type_from,
					"party": self.party_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Bank - Account To - Without Fees
		if not self.paid_from_party and self.paid_from_bank and not self.paid_to_party and not self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.acc_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Bank - Account To - With Fees
		if not self.paid_from_party and self.paid_from_bank and not self.paid_to_party and not self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.acc_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# Account From - To Party - Without Fees
		if not self.paid_from_party and not self.paid_from_bank and self.paid_to_party and not self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"party_type": self.party_type_to,
					"party": self.party_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# Account From - To Party - With Fees
		if not self.paid_from_party and not self.paid_from_bank and self.paid_to_party and not self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"party_type": self.party_type_to,
					"party": self.party_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Party - To Party - Without Fees
		if self.paid_from_party and not self.paid_from_bank and self.paid_to_party and not self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"party_type": self.party_type_to,
					"party": self.party_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"party_type": self.party_type_from,
					"party": self.party_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Party - To Party - With Fees
		if self.paid_from_party and not self.paid_from_bank and self.paid_to_party and not self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"party_type": self.party_type_to,
					"party": self.party_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"party_type": self.party_type_from,
					"party": self.party_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},

				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Bank - To Party - Without Fees
		if not self.paid_from_party and self.paid_from_bank and self.paid_to_party and not self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"party_type": self.party_type_to,
					"party": self.party_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Bank - To Party - With Fees
		if not self.paid_from_party and self.paid_from_bank and self.paid_to_party and not self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"party_type": self.party_type_to,
					"party": self.party_to,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# Account From - To Bank - Without Fees
		if not self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_to_acc,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# Account From - To Bank - With Fees
		if not self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_to_acc,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.account_from,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Party - To Bank - Without Fees
		if self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_to_acc,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"party_type": self.party_type_from,
					"party": self.party_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Party - To Bank - With Fees
		if self.paid_from_party and not self.paid_from_bank and not self.paid_to_party and self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_to_acc,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"party_type": self.party_type_from,
					"party": self.party_from,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.party_account_from,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Bank - To Bank - Without Fees
		if not self.paid_from_party and self.paid_from_bank and not self.paid_to_party and self.paid_to_bank and not self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_to_acc,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

		# From Bank - To Bank - With Fees
		if not self.paid_from_party and self.paid_from_bank and not self.paid_to_party and self.paid_to_bank and self.fees:
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_to_acc,
					"debit": self.paid_amount,
					"credit": 0,
					"debit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.fees_account,
					"debit": self.fees_amount,
					"credit": 0,
					"debit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.paid_amount,
					"credit_in_account_currency": self.paid_amount,
					"user_remark": self.name
				},
				{
					"doctype": "Journal Entry Account",
					"account": self.bank_account_from_acc,
					"debit": 0,
					"credit": self.fees_amount,
					"credit_in_account_currency": self.fees_amount,
					"user_remark": self.name
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"gur": self.name,
				"company": self.company,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"user_remark": self.notes,
				"remark": _('Guarantee Transaction  {0}').format(self.name)

			})
			doc.insert()
			doc.submit()

	pass
