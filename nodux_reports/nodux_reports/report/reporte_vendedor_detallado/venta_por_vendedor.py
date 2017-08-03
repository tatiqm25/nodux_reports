# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import time
from frappe.utils import flt
from frappe import msgprint, _


def execute(filters=None):
	conditions = get_conditions(filters)
	print conditions
	columns, data = [], []
	columns = ["Fecha","Vence","Num Factura","Estado",("Item")+"::180","Tiempo De Retraso","Precio Unitario","Total ",("Vendedor")+"::180",("Cliente")+"::180"]
	invoice_list = consulta_general(filters)
	# columns = get_columns(invoice_list)
	for inv in invoice_list:
		row = [ inv.posting_date,inv.due_date,inv.name,inv.status,inv.item_name,inv.amount,inv.allocated_amount,inv.outstanding_amount,inv.vendedor,inv.customer]
		data.append(row)
	return columns, data

def get_conditions(filters):
	conditions=""

	if filters.get("cliente"): conditions += " and customer=%(cliente)s"
	if filters.get("vendedor"): conditions += " and vendedor=%(vendedor)s"
	if filters.get("status"): conditions += " and status=%(status)s"
	# if filters.get("from_date"): conditions += " and posting_date >=%(from_date)s"
	if filters.get("date"): conditions += " and posting_date<=%(date)s"

	return conditions

def consulta_general(filters):
	conditions = get_conditions(filters)
	ahora =time.strftime("%d,%m,%y")
	# hoy = datetime.now()
	# # set otr=1
	# print ahora
	# q=frappe.db.sql(""" SELECT  (qty+1) as tiempo
	# 				FROM `tabSales Invoice Item` where `tabSales Invoice Item`.name ="SINV-00001"
	# 				""", as_dict=1)
	# print "asd",q
	# print conditions
	if not conditions:
		return frappe.db.sql(""" SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.due_date,allocated_amount,`tabSales Invoice`.name,`tabSales Invoice`.status,vendedor,
						customer,`tabSales Invoice Item`.item_code,`tabSales Invoice Item`.item_name,`tabSales Invoice`.outstanding_amount,amount
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						LEFT JOIN `tabPayment Entry Reference` ON `tabPayment Entry Reference`.reference_name=`tabSales Invoice`.name
						order by `tabSales Invoice`.name
						""", as_dict=1)
	if conditions:
		return frappe.db.sql("""SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.due_date,allocated_amount,`tabSales Invoice`.name,`tabSales Invoice`.status,vendedor,
						customer,`tabSales Invoice Item`.item_code,`tabSales Invoice Item`.item_name,`tabSales Invoice`.outstanding_amount,amount
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						LEFT JOIN `tabPayment Entry Reference` ON `tabPayment Entry Reference`.reference_name=`tabSales Invoice`.name
						where qty>0 %s
						order by `tabSales Invoice`.name""" %
						conditions, filters, as_dict=1)

# def get_columns(invoice_list):
# 	"""return columns based on filters"""
# 	columns = [
# 		_("Falta") + ":Link/Sales Invoice One:120", _("Posting Date") + ":Date:80",
# 		_("Customer Name") + "::120"]
#
# 	columns = columns + [_("Grand Total") + ":Currency/currency:120",
# 		_("Payment Amount") + ":Currency/currency:120",
# 		_("Pending Amount") + ":Currency/currency:120"]
#
# 	return columns
