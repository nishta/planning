from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, validate_email_add, today
import datetime
from planning.planning.myfunction import mail_format_pms,actual_date_update,close_task_update

@frappe.whitelist()
def checking_checkout(task=None,check_status=None,name=None):
	cur_date_time=frappe.utils.data.now ()
	user_name=frappe.session.user
	if(task):
		if(check_status=="0"):
			doctype="NNTask";
			#select parent,members,employee_name,parenttype from `tabNNAssign` where parenttype=%s and employee_name=%s",(doctype,user_name)
			count=frappe.db.sql("select task from `tabNNTask Check In Out` where status=1 and emp_name=%s",user_name);
			if(count):
				task=count[0][0]
				
				frappe.msgprint("Please Checkout <b>"+ task+"</b> Task")
				return "Not Valid"
			else:
				frappe.get_doc({
					"doctype":"NNTask Check In Out",
					"task":task,
					"check_in":cur_date_time,
					"status":1,
					"emp_name":user_name
					}).insert(ignore_permissions=True)
				actual_date_update(task)
		else:
			 hourly_rate=frappe.db.sql("""select hourly_rate from tabEmployee where employee_name=%s""",(user_name))
			 if(hourly_rate):
			 	hourly_cost=hourly_rate[0][0]
			 else:
			 	hourly_cost=0;
			 checkin_time=frappe.db.sql("""select check_in from `tabNNTask Check In Out` where name=%s""",name)
			 if(checkin_time):
			 	checked_intime=checkin_time[0][0];
			 else:
			 	checked_intime=0
			 time_diff_in_seconds=frappe.utils.data.time_diff_in_seconds(cur_date_time,checked_intime);
			 #frappe.msgprint(time_diff_in_seconds);
			 cost_for_seound=float(hourly_cost)/float(3600);
			 rate=(time_diff_in_seconds)*(cost_for_seound)
			 #frappe.msgprint(str(rate),raise_exception=1)
			 frappe.db.sql("""update `tabNNTask Check In Out` set check_out=%s,status=2,hourly_cost=%s,rate=%s where name=%s""",(cur_date_time,hourly_rate,rate,name))
	else:
		return "not"





@frappe.whitelist()
def getTask(doctype):
	data=[]
	user_name=frappe.session.user
	select_task=frappe.db.sql("select name,parent,members,employee_name,parenttype from `tabNNAssign` where  close_status=0 and parenttype=%s and employee_name=%s",(doctype,user_name))
	if(select_task):
		i=1;
		values="";
		for select_task_list in select_task:
			sno=i;
			assign_name=select_task_list[0];
			task_name=select_task_list[1];
			employee_id=select_task_list[2];
			employee_name=select_task_list[3];
			select_task_list=frappe.db.sql("""select task_list.project as project ,task_list.milestone as milestone,task_list.tasklist as task_list_name,task.duration as duration from `tabNNTasklist` task_list ,`tabNNTask` task  where task.name=%s and task_list.tasklist=task.tasklist""",(task_name))
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
			checkin_status=frappe.db.sql("""select * from `tabNNTask Check In Out` where status=%s and task=%s and emp_name=%s order by creation desc""",(status_che,task_name,user_name))
			if(checkin_status):
				check_status=1;
				check_status_name=checkin_status[0][0]
			else:
				check_status=0;
				check_status_name="";
			#worked_cocuation:
			total_seconds=0;
			working_hours=frappe.db.sql("""select check_in,check_out from `tabNNTask Check In Out` where status=2 and task=%s and emp_name=%s order by creation desc""",(task_name,user_name))
			for working_hours_list in working_hours:
				checkin_times=working_hours_list[0];
				checkout_times=working_hours_list[1];
				seconds=frappe.utils.data.time_diff_in_seconds(checkout_times,checkin_times);
				#frappe.msgprint(seconds);
				total_seconds=int(seconds)+int(total_seconds);
			#frappe.msgprint(total_seconds);
			worked_time=str(datetime.timedelta(seconds=total_seconds))
			rows=[project_name]+[milestone]+[task_list_name]+[task_name]+[employee_name]+[check_status]+[check_status_name]+[duration]+[worked_time]+[assign_name]
			data.append(rows)
			i=i+1;
		return data

	
@frappe.whitelist()
def close_task(assign_name=None,):
	frappe.db.sql("""Update `tabNNAssign` set close_status=1 where name=%s""",(assign_name))
	task=frappe.db.sql("""select parent from tabNNAssign where name=%s""",(assign_name))
	mode=1;
	task_name=task
	if task:
		doctype="NNTask";
		count=frappe.db.sql("""select *from tabNNAssign where close_status=0 and parent=%s and parenttype=%s""",(task_name,doctype))
		if not count:
			close_task_update(task)
	mail_format_pms(task_name,mode)
	