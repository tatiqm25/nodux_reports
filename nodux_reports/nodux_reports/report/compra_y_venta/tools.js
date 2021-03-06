// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.provide("nodux_reports.tools");

nodux_reports.tools.downloadxml = function(data, roles, title) {
	alert("entra");
	if(roles && roles.length && !has_common(roles, user_roles)) {
		msgprint(__("Export not allowed. You need {0} role to export.", [frappe.utils.comma_or(roles)]));
		return;
	}

	var filename = title + ".csv";
	var csv_data = frappe.tools.to_csv(data);
	var a = document.createElement('a');

	if ("download" in a) {
		// Used Blob object, because it can handle large files
		var blob_object = new Blob([csv_data], { type: 'text/csv;charset=UTF-8' });
		a.href = URL.createObjectURL(blob_object);
		a.download = filename;

	} else {
		// use old method
		a.href = 'data:attachment/csv,' + encodeURIComponent(csv_data);
		a.download = filename;
		a.target = "_blank";
	}

	document.body.appendChild(a);
	a.click();

	document.body.removeChild(a);
};

frappe.markdown = function(txt) {
	if(!frappe.md2html) {
		frappe.md2html = new Showdown.converter();
	}

	while(txt.substr(0,1)==="\n") {
		txt = txt.substr(1);
	}

	// remove leading tab (if they exist in the first line)
	var whitespace_len = 0,
		first_line = txt.split("\n")[0];

	while(["\n", "\t"].indexOf(first_line.substr(0,1))!== -1) {
		whitespace_len++;
		first_line = first_line.substr(1);
	}

	if(whitespace_len && whitespace_len != first_line.length) {
		var txt1 = [];
		$.each(txt.split("\n"), function(i, t) {
			txt1.push(t.substr(whitespace_len));
		})
		txt = txt1.join("\n");
	}

	return frappe.md2html.makeHtml(txt);
}


frappe.tools.to_csv = function(data) {
	var res = [];
	$.each(data, function(i, row) {
		row = $.map(row, function(col) {
			return typeof(col)==="string" ? ('"' + col.replace(/"/g, '""') + '"') : col;
		});
		res.push(row.join(","));
	});
	return res.join("\n");
};

frappe.slickgrid_tools = {
	get_filtered_items: function(dataView) {
		var data = [];
		for (var i=0, len=dataView.getLength(); i<len; i++) {
			data.push(dataView.getItem(i));
		}
		return data;
	},
	get_view_data: function(columns, dataView, filter) {
		var col_row = $.map(columns, function(v) { return v.name; });
		var res = [];
		var col_map = $.map(columns, function(v) { return v.field; });

		for (var i=0, len=dataView.getLength(); i<len; i++) {
			var d = dataView.getItem(i);
			var row = [];
			$.each(col_map, function(i, col) {
				var val = d[col];
				if(val===null || val===undefined) {
					val = "";
				}
				row.push(val);
			});

			if(!filter || filter(row, d)) {
				res.push(row);
			}
		}
		return [col_row].concat(res);
	},
	add_property_setter_on_resize: function(grid) {
		grid.onColumnsResized.subscribe(function(e, args) {
			$.each(grid.getColumns(), function(i, col) {
				if(col.docfield && col.previousWidth != col.width &&
					!in_list(frappe.model.std_fields_list, col.docfield.fieldname) ) {
					frappe.call({
						method:"frappe.client.make_width_property_setter",
						args: {
							doc: {
								doctype:'Property Setter',
								doctype_or_field: 'DocField',
								doc_type: col.docfield.parent,
								field_name: col.docfield.fieldname,
								property: 'width',
								value: col.width,
								"__islocal": 1
							}
						}
					});
					col.previousWidth = col.width;
					col.docfield.width = col.width;
				}
			});
		});
	}
};
