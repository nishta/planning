# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils import getdate, validate_email_add, today
import datetime

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_task_list(filters)

	return columns, data

def get_columns():
	return [
		_("Employee Name") + ":Data:120"
		,_("Project Name") + ":Link/NNProject:120"
		,_("Milstone Name")+ ":Link/NNMilestone:120"
		,_("TaskList Name")+ ":Link/NNTasklist:120"
		,_("Task Name")+ ":Link/NNTask:120"
		,_("Scheduled Time")+ ":datetime:100"
		,_("Worked Time")+ ":datetime:100"
		,_("Status")+ ":data:100"
		
		
	]

def get_task_list(filters):
	conditions = get_conditions(filters);
	data=[]
	select_task=frappe.db.sql("""select name,parent,members,employee_name,parenttype,close_status from `tabNNAssign`"""+conditions)
	if(select_task):
		i=1;
		values="";
		for select_task_list in select_task:
			sno=i;
			assign_name=select_task_list[0];
			task_name=select_task_list[1];
			employee_id=select_task_list[2];
			employee_name=select_task_list[3];
			close_status=select_task_list[5];
			if(close_status==0):
				close_status_show="Open"
			else:
				close_status_show="Closed";
			conditions_tasks = conditions_tasks_filter_list(filters);
			conditions_tasks_filter=" where task.task='%s'" % task_name
			conditions_tasks_filter=conditions_tasks_filter+conditions_tasks
			#frappe.msgprint(conditions_tasks_filter);
			select_task_list=frappe.db.sql("""select task_list.project as project ,task_list.milestone as milestone,task_list.tasklist as task_list_name,task.duration as duration from `tabNNTasklist` task_list ,`tabNNTask` task """+conditions_tasks_filter)
			if(select_task_list):
				project_name=select_task_list[0][0];
				milestone=select_task_list[0][1];
				task_list_name=select_task_list[0][2];
				duration=select_task_list[0][3];
			else:
				project_name="";
				milestone="";
			status="Status";
			close="Status";
			status_che=1
			checkin_status=frappe.db.sql("""select * from `tabNNTask Check In Out` where status=%s and task=%s and emp_name=%s order by creation desc""",(status_che,task_name,employee_name))
			if(checkin_status):
				check_status=1;
				check_status_name=checkin_status[0][0]
			else:
				check_status=0;
				check_status_name="";
			#worked_cocuation:
			total_seconds=0;
			working_hours=frappe.db.sql("""select check_in,check_out from `tabNNTask Check In Out` where status=2 and task=%s and emp_name=%s order by creation desc""",(task_name,employee_name))
			for working_hours_list in working_hours:
				checkin_times=working_hours_list[0];
				checkout_times=working_hours_list[1];
				seconds=frappe.utils.data.time_diff_in_seconds(checkout_times,checkin_times);
				total_seconds=int(seconds)+int(total_seconds);
			worked_time=str(datetime.timedelta(seconds=total_seconds))
			rows=[employee_name]+[project_name]+[milestone]+[task_list_name]+[task_name]+[duration]+[worked_time]+[close_status_show]
			data.append(rows)
			i=i+1;
	return data

def get_conditions(filters):
	conditions = ""
	count=0;
	doctype="NNTask";
	conditions += " Where   parenttype = '%s'" % doctype
	if filters.get("Status"):
		if filters.get("Status")=="Select Status":
			conditions+= " and close_status in(0,1)"
		if filters.get("Status")=="Closed":
			conditions+= " and close_status in(1)"
		if filters.get("Status")=="Open":
			conditions+= " and close_status in(0)"
	if filters.get("Task"): 
		Task=filters.get("Task");
		conditions += " and parent = '%s'" % Task
	if filters.get("Employee"): 
		Employee=filters.get("Employee");
		employees=frappe.db.sql("select employee_name from tabEmployee where name=%s",Employee)
		employees_name="";
		if(employees):
			employees_name=employees[0][0]
		#frappe.msgprint(employees_name);
		conditions += " and employee_name = '%s'" % employees_name
	conditions+=" order by creation desc";
	return conditions

def conditions_tasks_filter_list(filters):
	conditions_tasks_valuse=""
	if filters.get("Project"):
		project=filters.get("Project")
		conditions_tasks_valuse+=" and  task_list.project='%s'" % project
	if filters.get("Milestone"):
		Milestone=filters.get("Milestone")
		conditions_tasks_valuse+=" and task_list.milestone='%s'" % Milestone
	if filters.get("TaskList"):
		TaskList=filters.get("TaskList")
		conditions_tasks_valuse+=" and task_list.tasklist='%s'" % TaskList
	return conditions_tasks_valuse

