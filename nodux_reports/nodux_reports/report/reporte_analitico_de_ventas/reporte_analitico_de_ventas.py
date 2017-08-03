# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None,x=None):
	columns, data = [], []
	columns = [("Fecha")+"::130",("Cliente")+"::180","Forma de Pago"+"::100","Sub Total","Impuesto","Monto Total","Vendedor"+"::180"]
	invoice_list = consulta_general(filters)
	p = get_total1(filters)
	j = get_total2(filters)
	k = get_total3(filters)
	l = suma_dias(filters)
	h = suma_iva(filters)


	for inv in invoice_list:
		row = [ inv.posting_date,inv.customer,inv.forma,inv.total,inv.tax_amount,inv.grand_total,inv.vendedor]
		data.append(row)
	data += [{}]
	data += [{ "Forma de Pago":  "" + _("Total") + "", "Sub Total":  p, "Impuesto":  j, "Monto Total":  k},{}]

	data += [{ "Fecha":"Resumen "}]
	for lista in l:
		data += [{"Fecha":"Credito "+str(lista)+" dias", "Cliente":  l[lista]}]

	data += [{},{ "Fecha":"Resumen Iva "}]
	for lista2 in h:
		data += [{"Fecha":"Impuesto "+str(lista2)+" %", "Cliente":  h[lista2]}]

	return columns, data


def get_conditions(filters):
	conditions=""

	if filters.get("cliente"): conditions += " and customer=%(cliente)s"
	if filters.get("vendedor"): conditions += " and vendedor=%(vendedor)s"
	if filters.get("status"): conditions += " and status=%(status)s"
	if filters.get("to_date"): conditions += " and posting_date<=%(to_date)s"
	if filters.get("from_date"): conditions += " and posting_date>=%(from_date)s"
	if filters.get("marca"): conditions += " and `tabSales Invoice Item`.item_name=%(marca)s"
	# if filters.get("forma"): conditions += " and forma=%(forma)s"

	return conditions

def consulta_general(filters):
	hora=frappe.utils.nowdate()
	conditions = get_conditions(filters)
	nomr=" 'Creidto' "
	if not conditions:
		return frappe.db.sql(""" SELECT `tabSales Invoice`.posting_date,customer,vendedor,`tabSales Invoice`.total,grand_total,tax_amount,vendedor,
						(net_total-outstanding_amount)as abono,
						CASE WHEN `tabSales Invoice`.due_date-`tabSales Invoice`.posting_date=0
						THEN 'Contado'
						ELSE 'Credito'
						END AS forma
						FROM `tabSales Invoice`
						left JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
						order by `tabSales Invoice`.name
						""", as_dict=1)
	if conditions:
		return frappe.db.sql("""SELECT `tabSales Invoice`.posting_date,customer,vendedor,`tabSales Invoice`.total,grand_total,tax_amount,vendedor,
						(net_total-outstanding_amount)as abono,
						CASE WHEN `tabSales Invoice`.due_date-`tabSales Invoice`.posting_date=0
						THEN 'Contado'
						ELSE 'Credito'
						END AS forma
						FROM `tabSales Invoice`
						left JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
						where `tabSales Invoice`.posting_date>=0 %s
						order by `tabSales Invoice`.name""" %
						conditions, filters, as_dict=1)
def get_total1(filters):
	conditions=get_conditions(filters)
	if not conditions:
		m = frappe.db.sql("""SELECT sum(total)
	 				from `tabSales Invoice`""" )

	if conditions:
		m = frappe.db.sql("""SELECT sum(total)
	 				from `tabSales Invoice`
					where total>=0 %s""" % conditions,filters )

	return m


def get_total2(filters):
	conditions=get_conditions(filters)
	if not conditions:
		n=frappe.db.sql("""SELECT sum(tax_amount)
	 				from `tabSales Taxes and Charges`""" )
	if  conditions:
		n=frappe.db.sql("""SELECT sum(tax_amount)
	 				from `tabSales Invoice`
					left JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
					where tax_amount>=0 %s""" % conditions,filters )
	return n


def get_total3(filters):
	conditions=get_conditions(filters)
	if not conditions:
		b=frappe.db.sql("""SELECT sum(grand_total)
	 				from `tabSales Invoice`	""" )
	if conditions:
		b=frappe.db.sql("""SELECT sum(grand_total)
	 				from `tabSales Invoice`
					where grand_total>=0 %s""" % conditions,filters )
	return b


def get_total4(filters):
	conditions=get_conditions(filters)
	if not conditions:
		b = frappe.db.sql(""" SELECT due_date-posting_date
							FROM `tabSales Invoice`	""" )
	if conditions:
		b = frappe.db.sql(""" SELECT due_date-posting_date
							FROM `tabSales Invoice`
							where grand_total>=0 %s""" % conditions,filters )

	return b

def suma_dias(filters):
	q=get_total4(filters)
	dias_totales = []
	dias_sumados = {}
	for dias in q:
		if dias in dias_totales:
			pass
		else:
			dias_totales.append(dias)
	for d in dias_totales:
		d1= int(d[0])
		x=frappe.db.sql("""SELECT total FROM `tabSales Invoice` where `tabSales Invoice`.due_date-`tabSales Invoice`.posting_date = %s """,d1,as_dict=1)
		total_dia = 0
		for total in x:
			total_dia += total['total']

		dias_sumados[d1]= total_dia
	return dias_sumados

def get_total6(filters):
	conditions=get_conditions(filters)
	if not conditions:
		t = frappe.db.sql(""" SELECT tax_amount , rate
					FROM `tabSales Invoice`
					INNER JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
					""" ,as_dict=1)

	if conditions:
		t = frappe.db.sql(""" SELECT tax_amount , rate
					FROM `tabSales Invoice`
					INNER JOIN `tabSales Taxes and Charges`  ON `tabSales Taxes and Charges`.parent=`tabSales Invoice`.name
					where `tabSales Invoice`.total>=0 %s """ % conditions,filters, as_dict=1)
	return t

def suma_iva(filters):
	q=get_total6(filters)
	ivas_totales = []
	total_impuesto = {}

	for iva in q:
		# print iva['rate']
		if iva['rate'] in ivas_totales:
			pass
		else:
			ivas_totales.append(iva['rate'])

	# print ivas_totales
	for i in ivas_totales:
		total_iva=0
		for impuesto in q:
			if impuesto['rate'] == i:
				total_iva += impuesto['tax_amount']
				total_impuesto[i]=total_iva
	print total_impuesto
	return total_impuesto
