# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import time
from frappe import utils
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import flt
from frappe import msgprint, _
from datetime import datetime

def execute(filters=None):
	conditions = get_conditions(filters)
	print conditions
	columns, data = [], []
	columns = ["Fecha","Vence","Num Dias","Num Factura","Estado",("Item")+"::180","Total Factura","Pagos","Total Restante Por Pagar ",("Vendedor")+"::180",("Cliente")+"::180"]
	invoice_list = consulta_general(filters)
	for inv in invoice_list:
		row = [ inv.posting_date,inv.due_date,inv.tiempo,inv.name,inv.status,inv.item_name,inv.grand_total,inv.allocated_amount,inv.outstanding_amount,inv.vendedor,inv.customer]
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
	hora=frappe.utils.nowdate()
	ahora="(convert('"+hora+"',DATE))"
	conditions = get_conditions(filters)

	if not conditions:
		return frappe.db.sql(""" SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.due_date,allocated_amount,`tabSales Invoice`.name,`tabSales Invoice`.status,vendedor,
						customer,`tabSales Invoice Item`.item_code,`tabSales Invoice Item`.item_name,`tabSales Invoice`.outstanding_amount,grand_total,amount,
						`tabSales Invoice`.due_date-(CONVERT(%s, DATE)) as tiempo
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						LEFT JOIN `tabPayment Entry Reference` ON `tabPayment Entry Reference`.reference_name=`tabSales Invoice`.name
						order by `tabSales Invoice`.name
						""",hora,as_dict=1)
	if conditions:
		return frappe.db.sql("""SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.due_date,allocated_amount,`tabSales Invoice`.name,`tabSales Invoice`.status,vendedor,
						customer,`tabSales Invoice Item`.item_code,`tabSales Invoice Item`.item_name,`tabSales Invoice`.outstanding_amount,grand_total,amount,
						`tabSales Invoice`.due_date-"""+ahora+ """ as tiempo
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						LEFT JOIN `tabPayment Entry Reference` ON `tabPayment Entry Reference`.reference_name=`tabSales Invoice`.name
						where qty>0 %s
						order by `tabSales Invoice`.name""" %
						conditions,filters, as_dict=1)
