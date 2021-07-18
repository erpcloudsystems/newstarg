import frappe
from frappe import _
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from frappe.desk.doctype.todo.todo import ToDo
from frappe import _, msgprint, throw

def test(self):
    self.commercial_no = 12

SalesInvoice.validate = test