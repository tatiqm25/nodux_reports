// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.query_reports["Anexo de Costo de Venta"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Desde"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_default("year_start_date"),
			"width": "80"
		},

		{
			"fieldname":"date",
			"label": __("Hasta"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname":"marca",
			"label": __("Producto"),
			"fieldtype": "Link",
			"options": "Item"
		},
	]
}
