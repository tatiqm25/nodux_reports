# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _


def execute(filters=None):
	columns = ["Fecha",("Num Factura")+"::100",("Item")+"::250","Cantidad","Precio Unitario","Total ","Utilidad",("Vendedor")+"::250",("Cliente")+"::200"]
	invoice_list = get_item(filters)
	data = []

	for inv in invoice_list:
		row = [ inv.posting_date,inv.name,inv.item_code_1,inv.qty,inv.rate,inv.grand_total,inv.para,inv.vendedor,inv.customer]
		data.append(row)


	return columns, data


def get_conditions(filters):
	conditions=""

	if filters.get("cliente"): conditions += " and customer=%(cliente)s"
	if filters.get("vendedor"): conditions += " and vendedor=%(vendedor)s"
	if filters.get("marca"): conditions += " and `tabSales Invoice Item`.item_code_1=%(marca)s"
	return conditions

@frappe.whitelist()
def get_item(filters):
	conditions = get_conditions(filters)
	print conditions
	if not conditions:
		return frappe.db.sql(""" SELECT posting_date,vendedor,`tabSales Invoice`.name,grand_total, customer,qty,`tabSales Invoice Item`.item_code_1,`tabSales Invoice Item`.item_name,rate,amount,(((grand_total-qty*cost_price)*100)/(qty*cost_price)) as para
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						INNER JOIN `tabItem` on `tabItem`.item_code=`tabSales Invoice Item`.item_code_1
						order by `tabSales Invoice`.name
						""", as_dict=1)
	if conditions:
		return frappe.db.sql("""SELECT posting_date,`tabSales Invoice`.name,vendedor,grand_total, customer,qty,`tabSales Invoice Item`.item_code_1,`tabSales Invoice Item`.item_name,rate,amount,(((grand_total-qty*cost_price)*100)/(qty*cost_price)) as para
			from `tabSales Invoice`
			INNER JOIN `tabSales Invoice Item`
			ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
			INNER JOIN `tabItem` on `tabItem`.item_code=`tabSales Invoice Item`.item_name
			where qty>0 %s
			order by `tabSales Invoice`.name""" %
			conditions, filters, as_dict=1)
