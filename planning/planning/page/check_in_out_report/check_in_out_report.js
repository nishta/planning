var page = "";

frappe.pages['Check In Out Report'].on_page_load = function(wrapper) {
	page = frappe.ui.make_app_page({
		parent : wrapper,
		title : 'Check In Out Report',
		single_column : true
	});
	page.main.append(frappe.render_template('check_in_out_report', {
		data : {}
	}));

	page.$project = wrapper.page.add_field({
		fieldname : "Project",
		fieldtype : "Link",
		options : "NNProject",
		label : __("Project Name")
	}).$input.change(function() {
		alert("test")
	});

	page.$employee = wrapper.page.add_field({
		fieldname : "Employee",
		fieldtype : "Link",
		options : "Employee",
		label : __("Employee Name")
	}).$input.change(function() {
		alert("test")
	});

	page.$from_date = wrapper.page.add_field({
		fieldname : "From Date",
		fieldtype : "Date",
		label : __("From Date ")
	}).$input.change(function() {

	});
	page.$to_date = wrapper.page.add_field({
		fieldname : "To Date",
		fieldtype : "Date",
		label : __("To Date ")
	}).$input.change(function() {

	});

}