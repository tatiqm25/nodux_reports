# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate, get_first_day, get_last_day, date_diff, add_days
from lxml import etree

@frappe.whitelist()
def execute(filters=None):
    columns, data = [], []
    columns = ["Codigo","Nombre Cuenta"+"::180","Tipo","Debito","Credito"]
    accont=suma_accounts(filters)
    suma=suma_total(filters)
    consulta = ext_comp(filters)
    for lista in accont:
        data += [{"Nombre Cuenta":lista["nombre"],"Debito":lista["debit"], "Credito":  lista["credit"]}]

    data += [{},{"Nombre Cuenta":"Total","Debito":suma, "Credito":  suma}]
    return columns,data


@frappe.whitelist()
def xml():
	ats = etree.Element('iva')
	etree.SubElement(ats, 'TipoIDInformante').text = 'R'
	etree.SubElement(ats, 'IdInformante').text = "1103085471001"
	etree.SubElement(ats, 'razonSocial').text = "NODUX CIA LTDA"
	etree.SubElement(ats, 'Anio').text = "2017"
	etree.SubElement(ats, 'Mes').text = "08"

	file_ats = etree.tostring(ats, xml_declaration=True, encoding="utf-8")

	return file_ats

def get_conditions(filters):
	conditions=""
	# if filters.get("month"): conditions += " and posting_date>=%(from_date)s"
	# if filters.get("to_date"): conditions += " and posting_date<=%(to_date)s"
	return conditions

def ext_comp(filters):
    # desde=""
    from_date = get_first_day(filters["month"])
    to_date = get_last_day(filters["month"] )


    desde = str(from_date)
    hasta = str(to_date)
    compras =  frappe.db.sql(""" SELECT name
								 FROM `tabPurchase Invoice`
								 where  posting_date >=(convert (%s,DATE))
                                 """,desde,as_dict=1)
    print desde
    print compras
    return compras

def ext_account(filters):
	# conditions=get_conditions(filters)
	# print ">>>", conditions
	acconts1 =  frappe.db.sql(""" SELECT posting_date,account,debit,credit
								 FROM `tabGL Entry`
								 where voucher_type="Sales Invoice"
								 """,as_dict=1)
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
	# print cuentas_totales
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
