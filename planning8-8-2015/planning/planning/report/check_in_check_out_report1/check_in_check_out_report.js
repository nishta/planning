// Copyright (c) 2013, nishta and contributors
// For license information, please see license.txt

frappe.query_reports["Check IN Check Out Report"] = {
	"filters": [
		{
			"fieldname":"Employee",
			"label": __("Employee Name"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"fieldname":"Project",
			"label": __("Project Name"),
			"fieldtype": "Link",
			"options": "NNProject",
		},
		{
			"fieldname":"Milestone",
			"label": __("Milestone Name"),
			"fieldtype": "Link",
			"options": "NNMilestone",
		},
		{
			"fieldname":"TaskList",
			"label": __("TaskList Name"),
			"fieldtype": "Link",
			"options": "NNTasklist",
		},
		{
			"fieldname":"Task",
			"label": __("Task Name"),
			"fieldtype": "Link",
			"options": "NNTask",
		},
		
		{
			"fieldname":"Status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nSelect Status\nCheck In\nCheck Out",
			"default":"Select Status"

		},
		{
			"fieldname":"Check In Date-From",
			"label": __("Check In Date-From"),
			"fieldtype": "Date",
			"options": "NNTask",
		},
		{
			"fieldname":"Check In Date-To",
			"label": __("Check In Date-To"),
			"fieldtype": "Date",
			"options": "NNTask",
		},
		{
			"fieldname":"Check Out Date-From",
			"label": __("Check Out Date-From"),
			"fieldtype": "Date",
			"options": "NNTask",
		},
		{
			"fieldname":"Check Out Date-To",
			"label": __("Check Out Date-To"),
			"fieldtype": "Date",
			"options": "NNTask",
		},
	]
}
