from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, validate_email_add, today
import datetime
from planning.planning.myfunction import mail_format_pms,actual_date_update,close_task_update

@frappe.whitelist()
def report_in_out(doctype=None,date1=None,date2=None):
    filter = ""
    date1="2015-08-01"
    date2="2015-08-31"
    if date1 and not date2:
        date2=date1
    if date2 and not date1:
        date1=date2;
    if not date1 and not date2:
        date1=frappe.utils.data.nowdate ()
        date2=frappe.utils.data.nowdate ()
    user_name=frappe.session.user
    if date1==date2:
        no_days=1
    else:
        no_days=frappe.utils.data.date_diff(date2,date1)+1
    outer_loop={}
    return_list=[];
    for num in range(0,no_days):
        date_loop=frappe.utils.data.add_days(date1,num)
        date_lists=frappe.db.sql("""select t1.name as name,t1.expected_start_date as date from `tabNNTask` t1,`tabNNAssign` t2 where  t1.name=t2.parent and t2.employee_name=%s  and date(t1.expected_start_date)=%s """+filter,(user_name,date_loop),as_dict=True)
        i=0
        innner_loop=[]
        for date_list in date_lists:
            task=date_list['name']
            task_list_value=['task','schedule_time','worked_time','status','']
            innner_loop.append(task_list_value)
            i=i+i;
        outer_loop[date_loop]=innner_loop
    #return_list.append(outer_loop)   #date_lists=frappe.db.sql("""select t1.name as name,t1.expected_start_date as date from `tabNNTask` t1,`tabNNAssign` t2 where  t1.name=t2.parent and t2.employee_name=%s  and date(t1.expected_start_date) between %s and %s """+filter,(user_name,date1,date2),as_dict=True)
    return outer_loop