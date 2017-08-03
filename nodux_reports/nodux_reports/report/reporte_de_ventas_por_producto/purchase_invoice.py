from __future__ import unicode_literals
import frappe
import json
import copy
from frappe import throw, _
from frappe.utils import flt, cint
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _

def validate(doc, event):
    if cint(doc.no_genera_retencion):
        print "NO GENERA"

@frappe.whitelist()
def make_purchase_invoice_prueba(source_name, target_doc=None):
    def postprocess(source, target):
        set_missing_values(source, target)
        #Get the advance paid Journal Entries in Purchase Invoice Advance
        target.set_advances()

    def update_item(obj, target, source_parent):
        # target.amount = flt(obj.amount) - flt(obj.billed_amt)
        # target.base_amount = target.amount * flt(source_parent.conversion_rate)
        # target.qty = target.amount / flt(obj.rate) if (flt(obj.rate) and flt(obj.billed_amt)) else flt(obj.qty)
        target.qty = flt(obj.qty)

        # item = frappe.db.get_value("Item", target.item_code, ["item_group", "buying_cost_center"], as_dict=1)
        item = frappe.db.get_value("Item", target.item_code, ["cost_price"], as_dict=1)
        print "ITEM", item


        # target.cost_center = frappe.db.get_value("Project", obj.project, "cost_center") \
        #     or item.buying_cost_center \
        #     or frappe.db.get_value("Item Group", item.item_group, "default_cost_center")

    doc = get_mapped_doc("Purchase Order", source_name,	{
        "Purchase Order": {
            "doctype": "Purchase Invoice",
            "validation": {
                "docstatus": ["=", 1],
            }
        },

        "Purchase Order Item": {
            "doctype": "Purchase Invoice Item",
            "field_map": {
                "name": "po_detail",
                "parent": "purchase_order",
            },
            "postprocess": update_item
            # "condition": lambda doc: (doc.base_amount==0 or abs(doc.billed_amt) < abs(doc.amount))
            }
        #     "Purchase Taxes and Charges": {
        #         "doctype": "Purchase Taxes and Charges",
        #         "add_if_empty": True
        #     }
        }, target_doc, postprocess)

    return doc

def set_missing_values(source, target):
	target.ignore_pricing_rule = 1
	target.run_method("set_missing_values")
	target.run_method("calculate_taxes_and_totals")

@frappe.whitelist()
def update_taxes(refern,numero,provedor,fecha,iva1,impuesto1,base1,valor,ret_iva2,ret_imp2,tot,nombre,pagarto):
    #print nombre
    cadec="hola"
    doc = frappe.get_doc({
    	"doctype": "retenciones",
    	"referencia": refern,
        "supplier": provedor,
        "invoice_number":numero,
        "fecha_retencion":fecha,
        "base_imponible":base1,
        "impuesto":valor,
        "total":tot
    })

    lined = frappe.get_doc({
			"doctype": "Tabla Retenciones Proveedor",
			"impuestos": iva1,
			"base":base1,
			"valor":ret_iva2
    })
    linec = frappe.get_doc({
			"doctype": "Tabla Retenciones Proveedor",
			"impuestos":impuesto1,
        	"base":valor,
        	"valor":ret_imp2
    })
    doc.status=1
    doc.append('retenciones_proveedor', lined)
    doc.append('retenciones_proveedor', linec)
    doc.save()
    #
    doc = frappe.get_doc("Purchase Invoice", nombre)
    # get property
    doc.title
    # set property to the document
    doc.total_1= pagarto
    # save a document to the database
    doc.save()
    return cadec


@frappe.whitelist()
def verifica(num):
    code1 = frappe.db.sql("""select invoice_number from `tabretenciones` where referencia = %s """, num)
    return code1


@frappe.whitelist()
def verifica1(prove,nombre1,fech,totalrect,total_fact,num14,num15):

    doc = frappe.get_doc({
        "doctype": "Payment Entry",
        "payment_type": "Pay",
        "posting_date":fech ,
        "party_type":"Supplier",
        "mode_of_payment":"Efectivo",
        "party":prove,
        "paid_to":"Acreedores - ETT",
        "paid_from":"Efectivo - ETT",
        "paid_to_account_currency":"USD",
        "paid_from_account_currency":"USD",
        "paid_amount":flt(num14),
        "received_amount":flt(num14),
        })
    lined = frappe.get_doc({
			"doctype": "Payment Entry Reference",
			"reference_doctype": "Purchase Invoice",
			"reference_name":nombre1,
			"total_amount":flt(total_fact),
            "outstanding_amount":flt(total_fact),
            "allocated_amount":flt(num14)

            })
    doc.append('references', lined)
    doc.docstatus = 1
    doc.save()

    #second line
    doc1 = frappe.get_doc({
        "doctype": "Payment Entry",
        "payment_type": "Pay",
        "posting_date":fech ,
        "party_type":"Supplier",
        "mode_of_payment":"Efectivo",
        "party":prove,
        "paid_to":"Acreedores - ETT",
        "paid_from":"Efectivo - ETT",
        "paid_to_account_currency":"USD",
        "paid_from_account_currency":"USD",
        "paid_amount":flt(num15),
        "received_amount":flt(num15),
        })
    linec = frappe.get_doc({
			"doctype": "Payment Entry Reference",
			"reference_doctype": "Purchase Invoice",
			"reference_name":nombre1,
			"total_amount":flt(total_fact),
            "outstanding_amount":flt(total_fact),
            "allocated_amount":flt(num15)
            })
    doc1.append('references', linec)
    doc1.docstatus = 1
    doc1.save()

    return num15
