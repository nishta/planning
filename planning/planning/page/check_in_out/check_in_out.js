frappe.pages['check-in-out'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Task check-in-out',
		single_column: true
	});
	page.main.append(frappe.render_template('check_in_out', {}))
	frappe.call({
		method:"planning.planning.doctype.nntask.nntask.getTask",
		args:{"doctype":"Item"},
		callback:function(data){
			
		}
	})
	
}

