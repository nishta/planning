var page = "";
var $project="";
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
		
	});;
	page.$employee = wrapper.page.add_field({
		fieldname : "Employee",
		fieldtype : "Link",
		options : "Employee",
		label : __("Employee Name"),
	}).$input.change(function() {
		
	});
	page.$from_date = wrapper.page.add_field({
		fieldname : "From Date",
		fieldtype : "Date",
		label : __("From Date "),
		default: get_today()
	}).$input.ready(function() {
		
	});
	page.$to_date = wrapper.page.add_field({
		fieldname : "To Date",
		fieldtype : "Date",
		label : __("To Date "),
		default: get_today()
	}).$input.ready(function() {
		
	});
	page.$to_date = wrapper.page.add_field({
		fieldname : "Search",
		fieldtype : "Button",
		label : __("Search")
	}).$input.click(function() {
		load_report_in_out();
	});

var load_report_in_out = function() {	
	to_date=page.$to_date.val();
	from_date=page.$from_date.val();
	project=page.$project.val();
	employee=page.$employee.val();
frappe.call({
	method : "planning.planning.page.check_in_out_report.check_in_out_report.report_in_out",
	args : {
		"doctype" : "NNTask"
		},
		callback : function(data) {
			alert(data.message.length)
			page.main.append(frappe.render_template('check_in_out_report', {
				data : data.message
			}))
		}
});

}
load_report_in_out();
}