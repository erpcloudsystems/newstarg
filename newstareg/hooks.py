# -*- coding: utf-8 -*-
from __future__ import unicode_literals
app_name = "newstareg"
app_title = "Newstareg"
app_publisher = "erpcloud.systems"
app_description = "some ERPNext Customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mg@erpcloud.systems"
app_license = "MIT"

#override_doctype_class = {
#    'SalesInvoice': 'newstareg.newstareg.overrides.sales_invoice.CustomSalesInvoice',
#    'ToDo': 'newstareg.newstareg.overrides.sales_invoice.CustomToDo'
#}

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

