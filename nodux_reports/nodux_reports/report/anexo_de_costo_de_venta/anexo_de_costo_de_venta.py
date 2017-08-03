# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt
# item-costo-precio de venta-diferencia-utilidad-costo-costo-venta%-venta
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
	columns = ["Fecha",("Num Factura")+"::100",("Item")+"::250","Costo","Precio Venta","Diferencia ","Utilidad %","Costo ","Costo 0%","Venta ","Venta 0%"]
	invoice_list = traer_pro(filters)
	data = []

	for inv in invoice_list:
			row = [ inv.posting_date,inv.name,inv.item_code_1,inv.costo1,inv.venta1,inv.dif,inv.para,inv.cero,inv.uno,inv.cero1,inv.uno1]
			data.append(row)

	return columns, data

def get_conditions(filters):
	conditions=""
	if filters.get("marca"): conditions += " and `tabSales Invoice Item`.item_code_1=%(marca)s"
	if filters.get("date"): conditions += " and `tabSales Invoice`.posting_date <=%(date)s"

	return conditions

def traer_pro(filters):
	conditions = get_conditions(filters)
	if not conditions:
		return frappe.db.sql(""" SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.name,`tabSales Invoice Item`.item_code_1 ,`tabItem Price`.price_list_rate as costo1,
						`tabSales Invoice Item`.rate as venta1,(`tabSales Invoice Item`.rate-`tabItem Price`.price_list_rate)as dif,
						`tabSales Invoice Item`.item_name,amount,`tabSales Taxes and Charges`.rate ,
						(((`tabSales Invoice`.grand_total-qty*cost_price)*100)/(qty*cost_price)) as para,
						case WHEN `tabSales Taxes and Charges`.rate > 0
						THEN `tabItem Price`.price_list_rate
						ELSE ' '
						END as uno1,
						case WHEN `tabSales Invoice`.grand_total = `tabSales Invoice`.total
						THEN `tabItem Price`.price_list_rate
						ELSE  ' '
						END as cero1,
						case WHEN `tabSales Invoice`.grand_total = `tabSales Invoice`.total
						THEN `tabSales Invoice Item`.rate
						ELSE ' '
						END as uno,
						case WHEN `tabSales Invoice`.grand_total > `tabSales Invoice`.total
						THEN `tabSales Invoice Item`.rate
						ELSE ' '
						END as cero
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`	ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						left JOIN `tabItem Tax`	ON `tabItem Tax`.tax_type = `tabSales Invoice`.name
						INNER JOIN `tabItem Price` on `tabItem Price`.item_code=`tabSales Invoice Item`.item_code_1
						INNER JOIN `tabItem` on `tabItem`.item_code=`tabSales Invoice Item`.item_code_1
						LEFT JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
						order by `tabSales Invoice`.name
						""", as_dict=1)
	if conditions:
		return frappe.db.sql(""" SELECT `tabSales Invoice`.posting_date,`tabSales Invoice`.name,`tabSales Invoice Item`.item_code_1 ,`tabItem Price`.price_list_rate as costo1,
						`tabSales Invoice Item`.rate as venta1,(`tabSales Invoice Item`.rate-`tabItem Price`.price_list_rate)as dif,
						`tabSales Invoice Item`.item_name,amount,`tabSales Taxes and Charges`.rate ,
						(((`tabSales Invoice`.grand_total-qty*cost_price)*100)/(qty*cost_price)) as para,
						case WHEN `tabSales Taxes and Charges`.rate > 0
						THEN `tabItem Price`.price_list_rate
						ELSE ' '
						END as uno,
						case WHEN `tabSales Invoice`.grand_total = `tabSales Invoice`.total
						THEN `tabItem Price`.price_list_rate
						ELSE  ' '
						END as cero,
						case WHEN `tabSales Invoice`.grand_total = `tabSales Invoice`.total
						THEN `tabSales Invoice Item`.rate
						ELSE ' '
						END as uno1,
						case WHEN `tabSales Invoice`.grand_total > `tabSales Invoice`.total
						THEN `tabSales Invoice Item`.rate
						ELSE ' '
						END as cero1
						FROM `tabSales Invoice`
						INNER JOIN `tabSales Invoice Item`	ON `tabSales Invoice Item`.parent = `tabSales Invoice`.name
						left JOIN `tabItem Tax`	ON `tabItem Tax`.tax_type = `tabSales Invoice`.name
						INNER JOIN `tabItem Price` on `tabItem Price`.item_code=`tabSales Invoice Item`.item_code_1
						INNER JOIN `tabItem` on `tabItem`.item_code=`tabSales Invoice Item`.item_code_1
						LEFT JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
						 where `tabItem Price`.price_list_rate >= 0 %s
						"""% conditions,filters, as_dict=1)
