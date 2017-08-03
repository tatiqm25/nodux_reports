// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.query_reports["Reporte Vendedor Detallado"] = {
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
			"fieldname":"vendedor",
			"label": __("Venderdor"),
			"fieldtype": "Link",
			"options": "User"
		},

		{
			"fieldname":"status",
			"label": __("Estado de Factura"),
			"fieldtype": "Link",

		},

		{
			"fieldname":"cliente",
			"label": __("Cliente"),
			"fieldtype": "Link",
			"options": "Customer"

		},

		{
			"fieldname":"marca",
			"label": __("Producto"),
			"fieldtype": "Link",
			"options": "Item"
		},

	]
}
