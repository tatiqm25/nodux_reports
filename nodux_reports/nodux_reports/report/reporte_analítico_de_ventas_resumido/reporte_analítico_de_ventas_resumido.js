// Copyright (c) 2016, NODUX and contributors
// For license information, please see license.txt

frappe.query_reports["Reporte Analitico de Ventas Resumido"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"from_date",
			"label": __("Desde"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_default("year_start_date"),
			"width": "80"
		},

		{
			"fieldname":"vendedor",
			"label": __("Vendedor"),
			"fieldtype": "Link",
			"options":"User",
			"width": "80"
		},

		{
			"fieldname":"cliente",
			"label": __("Cliente"),
			"fieldtype": "Link",
			"options":"Customer",
			"width": "80"
		},

	]
}
