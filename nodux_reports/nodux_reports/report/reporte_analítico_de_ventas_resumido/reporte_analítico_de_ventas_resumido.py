# Copyright (c) 2013, NODUX and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = [("Fecha")+"::130",("Cliente")+"::180","Forma de Pago"+"::100","Sub Total","Impuesto","Monto Total","Vendedor"+"::180"]
	return columns, data
