// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.query_reports["Reporte de Ventas por Producto"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_default("year_start_date"),
			"width": "80"
		},

		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": get_today()
		},

		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},

		{
			"fieldname":"cliente",
			"label": __("Cliente"),
			"fieldtype": "Link",
			"options": "Customer"

		},

		{
			"fieldname":"vendedor",
			"label": __("Venderdor"),
			"fieldtype": "Link",
			"options": "User"
		},

		{
			"fieldname":"marca",
			"label": __("Producto"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"bodega",
			"label": __("Bodega"),
			"fieldtype": "Link",
			"options": "bodega"
		},


	]
}
