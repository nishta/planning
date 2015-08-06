frappe.listview_settings['Item'] = {
	add_fields: ["item_name", "stock_uom", "item_group", "image", "variant_of",
		"has_variants", "end_of_life", "is_sales_item"],

	get_indicator: function(doc) {
		if(doc.end_of_life && doc.end_of_life < frappe.datetime.get_today()) {
			return [__("Expired"), "grey", "end_of_life,<,Today"]
		} else if(doc.has_variants) {
			return [__("Template"), "blue", "has_variant,=,1"]
		} else if(doc.variant_of) {
			return [__("Variant"), "green", "variant_of,=," + doc.variant_of]
		} else {
			return [__("Active"), "blue", "end_of_life,>=,Today"]
		}
	}
};

frappe.help.youtube_id["Item"] = "qXaEwld4_Ps";
//today_cron();
function product_list()
{
	frappe.call({
            method:"erpnext.stock.doctype.item.cron_for_mat_code.product_code_gen",
            callback: function (data) {
			}
		})
}
function item_code_for_active()
{
	frappe.call({
            method:"erpnext.stock.doctype.item.cron_for_mat_code.item_code_for_active",
            callback: function (data) {
			}
		})
}
function item_code_for_template()
{
	frappe.call({
            method:"erpnext.stock.doctype.item.cron_for_mat_code.item_code_for_template",
            callback: function (data) {
			}
		})
}
function prefix_set()
{
	frappe.call({
            method:"erpnext.stock.doctype.item.cron_for_mat_code.prefix_set",
            callback: function (data) {
			}
		})
}
function today_cron()
{
	frappe.call({
            method:"erpnext.stock.doctype.item.cron_for_mat_code.today_cron",
            callback: function (data) {
			}
		})
}