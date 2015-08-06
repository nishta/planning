from __future__ import unicode_literals
import datetime

from frappe import _
import frappe
import frappe.database
import frappe.utils
import frappe.utils.user
from frappe import conf
from frappe.sessions import Session, clear_sessions, delete_session
from frappe.modules.patch_handler import check_session_stopped
from frappe.utils import getdate, validate_email_add, today
from urllib import quote

@frappe.whitelist(allow_guest=True)
def test_curl(mydoc_type=None,value=None):
  return "test"+mydoc_type

@frappe.whitelist()
def close_task_update(task):
  cur_date=frappe.utils.data.nowdate()
  frappe.db.sql("""update `tabNNTask` set status='Closed',actual_end_date=%s where task=%s""",(cur_date,task))

@frappe.whitelist()
def actual_date_update(task):
  cur_date=frappe.utils.data.nowdate()
  task_status=frappe.db.sql("""select update_status from `tabNNTask` where task=%s""",task)
  if task_status:
    task_status_val=task_status[0][0]
    if task_status_val!=1:
      frappe.db.sql("""update `tabNNTask` set actual_start_date=%s,update_status=1,status='InProgress' where task=%s""",(cur_date,task))
  tasklist=frappe.db.get_value("NNTask", {"task":task}, "tasklist")
  if tasklist:
    tasklistvalues=frappe.db.sql("""select project,milestone from `tabNNTasklist` where tasklist=%s""",tasklist)
    #frappe.msgprint("dsd",raise_exception=1)
    if tasklistvalues:
      project=tasklistvalues[0][0]
      milestone=tasklistvalues[0][1]
      project_status=frappe.db.get_value("NNProject",{"project_name":project},"update_status")
      if project_status!=1:
        frappe.db.sql("""update `tabNNProject` set actual_start_date=%s,update_status=1,status='InProgress' where project_name=%s""",(cur_date,project))
      milestone_status=frappe.db.get_value("NNMilestone",{"milestone":milestone},"update_status")
      if milestone_status!=1:
        frappe.db.sql("""update `tabNNMilestone` set actual_start_date=%s,update_status=1,status='InProgress' where milestone=%s""",(cur_date,milestone))
        #milestone=tasklistvalues[0][1]

@frappe.whitelist()
def time_calculation_employee(task_name,employee_name):
  user_name=frappe.session.user
  worked_time="";
  total_seconds=0
  cur_date_time=frappe.utils.data.now ()
  working_hours=frappe.db.sql("""select check_in,check_out from `tabNNTask Check In Out` where  task=%s and emp_name=%s order by creation desc""",(task_name,employee_name))
  for working_hours_list in working_hours:
    checkin_times=working_hours_list[0];
    checkout_times=working_hours_list[1];
    if checkout_times==None:
      checkout_times=cur_date_time
    seconds=frappe.utils.data.time_diff_in_seconds(checkout_times,checkin_times);
        #frappe.msgprint(seconds);
    total_seconds=int(seconds)+int(total_seconds);
      #frappe.msgprint(total_seconds);
  worked_time=str(datetime.timedelta(seconds=total_seconds))
  return worked_time;
 
@frappe.whitelist()
def time_calculation(task_name):
  user_name=frappe.session.user
  worked_time="";
  total_seconds=0
  working_hours=frappe.db.sql("""select check_in,check_out from `tabNNTask Check In Out` where status=2 and task=%s and emp_name=%s order by creation desc""",(task_name,user_name))
  for working_hours_list in working_hours:
    checkin_times=working_hours_list[0];
    checkout_times=working_hours_list[1];
    seconds=frappe.utils.data.time_diff_in_seconds(checkout_times,checkin_times);
        #frappe.msgprint(seconds);
    total_seconds=int(seconds)+int(total_seconds);
      #frappe.msgprint(total_seconds);
  worked_time=str(datetime.timedelta(seconds=total_seconds))
  return worked_time;

@frappe.whitelist()
def daily_summary_mail():
  cur_date=frappe.utils.data.nowdate()
  body_content="""<body style="font-family: Arial, Helvetica, sans-serif; font-size: 90%;">
  <table width="100%" border="1" cellpadding="5" cellspacing="0" bordercolor="#eee">"""
  employees=frappe.db.sql("""select emp_name,creation from `tabNNTask Check In Out` where date(creation)=%s group by emp_name""",cur_date)
  for employees_values in employees:
    employee_name=employees_values[0]
    employee_content="""<tr style="background: #0066FF; color: #fff;">
      <td colspan="8"><strong>Employee Name:{employee_name}</strong></td>
    </tr>
    <tr><th>S.No</th>
            <th>Project Name</th>
            <th>Milestone Name</th>
            <th>TaskList Name</th>
            <th>TasK Name</th>
            <th>Scheduled Hour</th>
            <th>Worked Hour</th>
            <th>Status</th>
          </tr>""".format(employee_name=employee_name)
    task=frappe.db.sql("""select task from `tabNNTask Check In Out` where date(creation)=%s and emp_name=%s group by task""",(cur_date,employee_name))
    i=0
    total_worked_hour="0"
    total_scheduled_hour="0"
    task_content=""
    total_duration_seconds=0
    total_worked_seconds=0
    for task_val in task:
      task_name=task_val[0]
      nnassign=frappe.db.sql("""select name,close_status,members from `tabNNAssign` where  employee_name=%s and parent=%s group by parent order by creation desc""",(employee_name,task_name))
      close_status=nnassign[0][1]
      members=nnassign[0][2]
      mail_id=frappe.db.get_value("Employee", {"name":members}, "company_email")
      if close_status==0:
        close_status_show="Open"
      if close_status==1:
        close_status_show="Closed"
      tasklist_name=task_list_name(task_name)
      project_name=task_project_name(tasklist_name)
      milestone_name=task_milestone_name(tasklist_name)
      duration=frappe.db.get_value("NNTask",{"task":task_name},"duration")
      total_duration_seconds+=int(hms_to_seconds(duration))
      worked_time_cal=time_calculation_employee(task_name,employee_name)
      total_worked_seconds+=int(hms_to_seconds(worked_time_cal))
      sno=i+1;
      task_content+="""
       <tr><td>{sno}</td>
            <td>{project_name}</td>
            <td>{milestone_name}</td>
            <td>{tasklist_name}</td>
            <td>{task_name}</td>
            <td>{duration}</td>
            <td>{worked_time_cal}</td>
            <td>{close_status_show}</td>
          </tr>""".format(sno=sno,project_name=project_name,milestone_name=milestone_name,tasklist_name=tasklist_name,task_name=task_name,duration=duration,worked_time_cal=worked_time_cal,close_status_show=close_status_show)
      i=i+1;
    total_scheduled_hour=str(datetime.timedelta(seconds=total_duration_seconds))
    total_worked_hour=str(datetime.timedelta(seconds=total_worked_seconds))
    total_scheduls="""<tr><td colspan="8" align="right">Total Scheduled Hours:{total_scheduled_hour}</td><tr>""".format(total_scheduled_hour=total_scheduled_hour)
    total_works="""<tr><td colspan="8" align="right">Total Scheduled Hours:{total_scheduled_hour}</td><tr>""".format(total_worked_hour=total_worked_hour)
    closed_table="""</table></table></body>"""
    new_body=body_content+employee_content+task_content+total_scheduls+total_works+closed_table
    frappe.sendmail(recipients=mail_id,
                        subject="Nishta PMS {name}".format(
                            name="Daily Summary"),
                        message=new_body, bulk=True)
    #frappe.msgprint(new_body)
  
@frappe.whitelist()
def task_list_name(task_name):
  task_list_name=frappe.db.get_value("NNTask",{"task":task_name},"tasklist")
  return task_list_name

def task_milestone_name(tasklist_name):
  milestone_name=frappe.db.get_value("NNTasklist",{"tasklist":tasklist_name},"milestone")
  return milestone_name

def task_project_name(tasklist_name):
  project_name=frappe.db.get_value("NNTasklist",{"tasklist":tasklist_name},"project")
  return project_name

@frappe.whitelist()
def load_employee_name(octype, txt, searchfield, start, page_len, filters):
  #return "EMP/002"
  if filters.get('taskList'):
    taskList=filters['taskList']
    project=frappe.db.sql("""select project from `tabNNTasklist` where taskList=%s""",taskList)
    project_name=project[0]
    if project_name:
      return frappe.db.sql(""" Select tabEmployee.name,tabEmployee.employee_name from `tabNNAssign`,`tabEmployee`  where  tabNNAssign.members=tabEmployee.name and tabNNAssign.parenttype='NNProject' and tabNNAssign.parent=%s""",project_name)
    
@frappe.whitelist()
def hms_to_seconds(t):
    t=str(t)
    h, m, s = [int(i) for i in t.split(':')]
    return 3600*h + 60*m + s

@frappe.whitelist()
def mail_format_pms(task_name=None,mode=None):
  rows=frappe.db.sql("""select tasklist,task,duration,expected_start_date,expected_end_date,actual_start_date,actual_end_date,description from `tabNNTask` where name=%s""",task_name)
  if rows:
    tasklist=rows[0][0];
    task_name=rows[0][1];
    schedule_hour=rows[0][2];
    actual_hour="";
    if mode==1:
      actual_hour=time_calculation(task_name);
    schedule_date_start=rows[0][3];
    schedule_date_start=frappe.utils.data.formatdate (schedule_date_start, "")
    schedule_date_end=rows[0][4];
    schedule_date_end=frappe.utils.data.formatdate (schedule_date_end, "")
    actual_start_date=rows[0][5];
    actual_start_date=frappe.utils.data.formatdate (actual_start_date, "")
    actual_end_date=rows[0][6];
    actual_end_date=frappe.utils.data.formatdate (actual_end_date, "")
    description=rows[0][7]
    body_email_members="";    
    task_list_values=frappe.db.sql("""Select project,milestone from `tabNNTasklist` where tasklist=%s""",tasklist)
    prioct_name=task_list_values[0][0]
    milestone=task_list_values[0][1]
    results_members=frappe.db.sql("""select members from `tabNNAssign` where parent=%s and parenttype='NNTask'""",task_name)
    email_ids=[]
    members_id=""
    for values_members in results_members:
      members=values_members[0]
      email_ids.append(frappe.db.get_value("Employee", {"name":members}, "company_email"))
      members_name=frappe.db.get_value("Employee", {"name":members}, "employee_name")
      members_id +='<li>'+members_name+'</li>'
    body_email="""<body style="font-family:Arial, Helvetica, sans-serif; font-size:90%;">
          <table width="100%" border="1" cellpadding="5" cellspacing="0" bordercolor="#eee">
            <tr style="background:#0066FF; color:#fff;">
            <td rowspan="2"><strong>Task :"""+task_name+"""</strong></td>
            <td><strong>Schedule Hours : """+str(schedule_hour)+"""</strong></td>
           </tr>
          <tr style="background:#0066FF; color:#fff;">
            <td><strong>Actual Hours : """+str(actual_hour)+"""</strong></td>
          </tr>
          <tr>
            <td>Schedule Start Date : <strong>"""+str(schedule_date_start)+"""</strong></td>
            <td>Schedule End Date : <strong>"""+str(schedule_date_end)+"""</strong></td>
          </tr>
          <tr>
            <td>Actual Start Date : <strong>"""+str(actual_start_date)+"""</strong></td>
            <td>Actual End Date : <strong>"""+str(actual_end_date)+"""</strong></td>
          </tr>
           <tr>
            <td colspan="2">Project Name : """+prioct_name+"""</td>
          </tr>
          <tr>
            <td colspan="2">Milestone : """+milestone+"""</td>
          </tr>
          <tr>
            <td colspan="2">Task List : """+tasklist+"""</td>
          </tr>
          <tr>
            <td colspan="2" align="left" valign="top"><p>Description : """+str(description)+"""</p>
            <p>&nbsp;</p></td>
          </tr>
          <tr><td align="left" valign="top" colspan="2" ><p><strong>Members :</strong></p><ol>"""+members_id+"""</ol></td>
          </tr>
          </table>
          </body>"""
    frappe.sendmail(recipients=email_ids,
                        subject="Nishta-Pms {name}".format(
                            name="Task ("+task_name+")"),
                        message=body_email, bulk=True)
    #frappe.msgprint(body_email)
