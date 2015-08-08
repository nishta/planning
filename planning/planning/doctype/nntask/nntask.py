# -*- coding: utf-8 -*-
# Copyright (c) 2015, nishta and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, validate_email_add, today
from frappe.model.document import Document
from planning.planning.myfunction import mail_format_pms,daily_summary_mail
import datetime

class NNTask(Document):
  
  def autoname(self):
    max_no_old="0"
    max_no_result=frappe.db.sql("""select max(max_count) from `tabNNTask`""")
    if(max_no_result):
      max_no_old=max_no_result[0][0]
    if max_no_old<=0:
      max_no_old=0
    max_no_new=int(max_no_old)+int(1)
    count_zero=""
    if max_no_new<1000:
      count_zero="0"
    if max_no_new<100:
      count_zero="00"
    if max_no_new<10:
      count_zero="000"
    self.max_count=max_no_new
    new_naming=str("-")+str(count_zero)+str(max_no_new)
    self.task=self.task+new_naming
    self.name=self.task
  
  def validate(self):
    allocate_to_arr=[]
    i=1
    for d in self.assign_to:
      if d.members in allocate_to_arr:
        frappe.msgprint("Allocate to "+ str(d.members) +" Already Exists ( Row No : "+ str(i) +")",raise_exception=1)
      else:
        allocate_to_arr.append(d.members)
  
  def after_insert(self):
    task_name=self.task
    mode=0
    mail_format_pms(task_name,mode)

@frappe.whitelist()
def employee_values_load(naming_series=None):
    return_values=frappe.db.sql("""select employee_name,hourly_rate from tabEmployee where employee=%s""",naming_series)
    return return_values

	

