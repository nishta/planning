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
		,_("Project Name") + ":Link/NNProject:150"
		,_("Milstone Name")+ ":Link/NNMilestone:150"
		,_("TaskList Name")+ ":Link/NNTasklist:150"
		,_("Task Name")+ ":Link/NNTask:150"
		,_("Check In Time")+ ":datetime:130"
		,_("Check Outime")+ ":datetime:130"
		,_("Worked Time")+ ":datetime:100"
		,_("Status")+ ":Data:100"
		
		
	]

def get_task_list(filters):
	conditions = get_conditions(filters);
	conditions_tasks= conditions_tasks_filter_list(filters);
	select_checkin=frappe.db.sql("""select check_in,check_out,emp_name,task,rate,hourly_cost,status from `tabNNTask Check In Out`"""+conditions)
	data=[]
	conditions_tasks_filter=""
	i=1
	show_status="";
	total_seconds=""
	for select_checkin_list in select_checkin:
		check_in1=select_checkin_list[0]
		check_in=frappe.utils.data.format_datetime(check_in1);
		check_out1=select_checkin_list[1]
		check_out=frappe.utils.data.format_datetime(check_out1);
		employee_name=select_checkin_list[2]
		task=select_checkin_list[3];
		rate=select_checkin_list[4]
		status=select_checkin_list[6]
		if status==1:
			show_status="Check In";
			worked_time="";
		if status==2:
			show_status="Check Out";
			seconds=frappe.utils.data.time_diff_in_seconds(check_out1,check_in1);
			#frappe.msgprint(seconds);
			seconds=int(seconds);
			worked_time=str(datetime.timedelta(seconds=seconds))
			#frappe.msgprint(worked_time);
			#worked_time=str(datetime.timedelta(seconds=worked_time))
		#conditions_tasks_filter=" where task.task='%s'"%
		conditions_tasks_filter=" where task.task='%s' and task_list.tasklist=task.tasklist " % task
		conditions_tasks_filter=conditions_tasks_filter+conditions_tasks
		select_task_list=frappe.db.sql("""select task_list.project as project ,task_list.milestone as milestone,task_list.tasklist as task_list_name,task.duration as duration from `tabNNTasklist` task_list ,`tabNNTask` task """+conditions_tasks_filter)
		if(select_task_list):
			project_name=select_task_list[0][0];
			milestone=select_task_list[0][1];
			task_list_name=select_task_list[0][2];
			duration=select_task_list[0][3];
		else:
			project_name="";
			milestone="";
		rows=[employee_name]+[project_name]+[milestone]+[task_list_name]+[task]+[check_in]+[check_out]+[worked_time]+[show_status]
		data.append(rows)
		i=i+1;
	return data

def get_conditions(filters):
	conditions = ""
	count=0;
	if filters.get("Status"):
		if filters.get("Status")=="Select Status":
			conditions+= "Where status in(1,2)"
		if filters.get("Status")=="Check In":
			conditions+= "Where status in(1)"
		if filters.get("Status")=="Check Out":
			conditions+= " Where status in(2)"
  	else:
   		conditions+= "Where status in(0,1)"
   	condition_checkin=0
   	condition_checkout=0
   	if filters.get("Check In Date-From") and filters.get("Check In Date-To"):
   		checkin_form=filters.get("Check In Date-From")
   		checkin_to=filters.get("Check In Date-To")
   		conditions+= "and date(check_in) between '%s' and '%s'" % (checkin_form,checkin_to)
		condition_checkin=1;
	if condition_checkin==0:
		if filters.get("Check In Date-From"):
   			checkin_form=filters.get("Check In Date-From")
			conditions+= "and date(check_in)='%s'" % checkin_form
   		if filters.get("Check In Date-To"):
   			checkin_to=filters.get("Check In Date-To")
			conditions+= "and date(check_in) ='%s'" % checkin_to
	if filters.get("Check Out Date-From") and filters.get("Check Out Date-To"):
   		checkOut_form=filters.get("Check Out Date-From")
   		checkOut_to=filters.get("Check Out Date-To")
   		conditions+= "and date(check_out) between '%s' and '%s'" % (checkOut_form,checkOut_to)
		condition_checkout=1;
	if condition_checkout==0:
		if filters.get("Check Out Date-From"):
   			checkout_form=filters.get("Check Out Date-From")
			conditions+= "and date(check_out)='%s'" % checkout_form
   		if filters.get("Check Out Date-To"):
   			checkout_to=filters.get("Check Out Date-To")
			conditions+= "and date(check_out) ='%s'" % checkout_to
	if filters.get("Task"): 
		Task=filters.get("Task");
		conditions += " and task = '%s'" % Task
	if filters.get("Employee"): 
		Employee=filters.get("Employee");
		employees=frappe.db.sql("select employee_name from tabEmployee where name=%s",Employee)
		employees_name="";
		if(employees):
			employees_name=employees[0][0]
		#frappe.msgprint(employees_name);
		conditions += " and emp_name = '%s'" % employees_name
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

