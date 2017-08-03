# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Codigo","Nombre Cuenta"+"::180","Tipo","Debito","Credito"]
	accont=suma_accounts(filters)
	suma=suma_total(filters)
	print suma
	for lista in accont:
		data += [{"Nombre Cuenta":lista["nombre"],"Debito":lista["debit"], "Credito":  lista["credit"]}]
	# for lista1 in suma:
	data += [{},{"Nombre Cuenta":"Total","Debito":suma, "Credito":  suma}]

	return columns, data
def get_conditions(filters):
	conditions=""

	if filters.get("from_date"): conditions += " and posting_date>=%(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date<=%(to_date)s"
	return conditions

def ext_account(filters):
	conditions=get_conditions(filters)
	# print ">>>", conditions
	acconts1 =  frappe.db.sql(""" SELECT posting_date,account,debit,credit
								 FROM `tabGL Entry`
								 where voucher_type="Sales Invoice" %s
								 """% conditions,filters,as_dict=1)
	# print "sentencia>>",acconts1

	return acconts1
def suma_accounts(filters):
	# conditions = condition(filters)
	q=ext_account(filters)
	lista_cuentas = []
	cuentas_totales = []
	# total_cuentas = {}
	# print "obtencio>>>",q
	for cuentas in q:
		#  print cuentas['account']
		if cuentas['account'] in cuentas_totales:
			pass
		else:
			cuentas_totales.append(cuentas['account'])
	print cuentas_totales
	# print c
	for i in cuentas_totales:
		total_debit=0
		total_credit=0
		total_cuentas={}
		for total in q:
			if total['account'] == i:
				total_debit += total['debit']
				total_credit += total['credit']
		total_cuentas = {
			"nombre" : i,
			"debit" : total_debit,
			"credit" : total_credit
		}
		lista_cuentas.append(total_cuentas)

	return lista_cuentas

def suma_total(filters):
	suma=suma_accounts(filters)
	deb=0
	total=0
	cre=0
	for r in suma:
		if r["credit"]>0:
			cre =cre+r["credit"]
		if r["debit"]:
			deb=deb+r["debit"]
	if deb == cre:
		total=deb
	else:total=23
	return total
	# print cre
