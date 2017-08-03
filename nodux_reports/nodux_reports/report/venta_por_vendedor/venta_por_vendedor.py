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
	columns = ["Fecha","Vence","Num Dias de Retraso","Num Factura","Estado",("Item")+"::180","Total Factura","Total Abonado","Total Pendiente ",("Vendedor")+"::180",("Cliente")+"::180"]
	invoice_list = consulta_general(filters)
	for inv in invoice_list:
		row = [ inv.posting_date,inv.due_date,inv.tiempo,inv.name,inv.status,inv.item_name,inv.grand_total,inv.abono,inv.outstanding_amount,inv.vendedor,inv.customer]
		data.append(row)
	return columns, data

def get_conditions(filters):
	conditions=""

	if filters.get("cliente"): conditions += " and customer=%(cliente)s"
	if filters.get("vendedor"): conditions += " and vendedor=%(vendedor)s"
	if filters.get("status"): conditions += " and status=%(status)s"
	if filters.get("date"): conditions += " and posting_date<=%(date)s"
	if filters.get("marca"): conditions += " and `tabSales Invoice Item`.item_code_1=%(marca)s"

	return conditions

def consulta_general(filters):
	conditions = get_conditions(filters)
	hora=frappe.utils.nowdate()
	ahora="(convert('"+hora+"',DATE))"
	if not conditions:
		return frappe.db.sql(""" SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.due_date,`tabSales Invoice`.name,`tabSales Invoice`.status,vendedor,grand_total,
						customer,`tabSales Invoice Item`.item_name,amount,outstanding_amount,
						(grand_total-outstanding_amount)as abono,
						`tabSales Invoice`.due_date-(CONVERT(%s, DATE)) as tiempo
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						order by `tabSales Invoice`.name
						""",hora, as_dict=1)
	if conditions:
		return frappe.db.sql("""SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.due_date,`tabSales Invoice`.name,`tabSales Invoice`.status,vendedor,grand_total,
						customer,`tabSales Invoice Item`.item_name,amount,outstanding_amount,(grand_total-outstanding_amount)as abono,
						`tabSales Invoice`.due_date-"""+ahora+ """ as tiempo
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						where qty>0 %s
						order by `tabSales Invoice`.name""" %
						conditions, filters, as_dict=1)
