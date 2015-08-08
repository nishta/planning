// Copyright (c) 2013, nishta and contributors
// For license information, please see license.txt

frappe.query_reports["Closed Task List"] = {
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
			"options": "\nSelect Status\nClosed\nOpen",
			"default":"Select Status"

		},
	]
}
