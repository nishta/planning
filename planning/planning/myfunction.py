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
  frappe.db.sql("""update `tabNNTask` set actual_end_date=%s where task=%s""",(cur_date,task))

@frappe.whitelist()
def actual_date_update(task):
  #frappe.msgprint("test")
  cur_date=frappe.utils.data.nowdate()
  task_status=frappe.db.sql("""select update_status from `tabNNTask` where task=%s""",task)
  if task_status:
    task_status_val=task_status[0][0]
    if task_status_val!=1:
      frappe.db.sql("""update `tabNNTask` set actual_start_date=%s,update_status=1 where task=%s""",(cur_date,task))
  tasklist=frappe.db.get_value("NNTask", {"task":task}, "tasklist")
  if tasklist:
    tasklistvalues=frappe.db.sql("""select project,milestone from `tabNNTasklist` where tasklist=%s""",tasklist)
    #frappe.msgprint("dsd",raise_exception=1)
    if tasklistvalues:
      project=tasklistvalues[0][0]
      milestone=tasklistvalues[0][1]
      project_status=frappe.db.get_value("NNProject",{"project_name":project},"update_status")
      if project_status!=1:
        frappe.db.sql("""update `tabNNProject` set actual_start_date=%s,update_status=1 where project_name=%s""",(cur_date,project))
      milestone_status=frappe.db.get_value("NNMilestone",{"milestone":milestone},"update_status")
      if milestone_status!=1:
        frappe.db.sql("""update `tabNNMilestone` set actual_start_date=%s,update_status=1 where milestone=%s""",(cur_date,milestone))
        #milestone=tasklistvalues[0][1]
 
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
  frappe.msgprint("Test",raise_exception=1);

@frappe.whitelist()
def mail_format_pms(task_name=None,mode=None):
  rows=frappe.db.sql("""select tasklist,task,duration,expected_start_date,expected_end_date,actual_start_date,actual_end_date,description from `tabNNTask` where name=%s""",task_name)
  if rows:
    tasklist=rows[0][0];
    task_name=rows[0][1];
    schedule_hour=rows[0][2];
    #schedule_hour="";
    actual_hour="";
    if mode==1:
      actual_hour=time_calculation(task_name);
    schedule_date_start=rows[0][3];
    schedule_date_start=frappe.utils.data.formatdate (schedule_date_start, "")
    #frappe.msgprint(schedule_date_start,raise_exception=1);
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
