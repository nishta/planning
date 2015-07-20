# -*- coding: utf-8 -*-
# Copyright (c) 2015, nishta and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, validate_email_add, today
from frappe.model.document import Document

class NNTask(Document):

	def validate(self):
		#frappe.msgprint(self.name)
		task_name=self.task;
		tasklist=self.tasklist;
		schedule_hour=self.duration;
		actual_hour="";
		schedule_date_start=self.expected_start_date;
		schedule_date_start=frappe.utils.data.formatdate (schedule_date_start, "")
		schedule_date_end=self.expected_end_date;
		schedule_date_end=frappe.utils.data.formatdate (schedule_date_end, "")
		actual_hour="";
		task_list_values=frappe.db.sql("""Select project,milestone from tabNNTasklist where tasklist=%s""",tasklist)
		prioct_name=task_list_values[0][0]
		milestone=task_list_values[0][1]
		description=self.description;
		if not description:
			description=" ";
		body_email_members="";
		for d in self.assign_to:
			member_id=d.members
			frappe.msgprint(member_id);
			value=frappe.db.get_value("Employee", {"name":member_id}, "company_email")
    		body_email_members=body_email_members+"<ul style='line-height:25px;'><li>"+member_id+"</li></ul>"
		#frappe.msgprint(body_email_members)
		body_email="""<body style="font-family:Arial, Helvetica, sans-serif; font-size:90%;">
	<table width="100%" border="1" cellpadding="5" cellspacing="0" bordercolor="#eee">
  	<tr style="background:#0066FF; color:#fff;">
    <td rowspan="2"><strong>Task Name:"""+task_name+"""</strong></td>
    <td><strong>Schedule Hour : """+schedule_hour+"""</strong></td>
 	 </tr>
  <tr style="background:#0066FF; color:#fff;">
    <td><strong>Actual Hours : """+actual_hour+"""</strong></td>
  </tr>
  <tr>
    <td>Schedule Start Date : <strong>"""+schedule_date_start+"""</strong></td>
    <td>Schedule End Date : <strong>"""+schedule_date_end+"""</strong></td>
  </tr>
  <tr>
    <td>Actual Start Date : <strong>DD/MM/YYYY</strong></td>
    <td>Actual End Date : <strong>DD/MM/YYYY</strong></td>
  </tr>
  <tr>
    <td colspan="2"><strong>Project Name:"""+prioct_name+"""</strong></td>
  </tr>
  <tr>
    <td colspan="2">Milestone:"""+milestone+"""</td>
  </tr>
  <tr>
    <td colspan="2">Task List:"""+tasklist+"""</td>
  </tr>
  <tr>
    <td colspan="2" align="left" valign="top"><p>Description : <strong>:"""+description+"""</strong></p>
    <p>&nbsp;</p></td>
  </tr>
  <tr><td align="left" valign="top"><p><strong>Members :</strong></p>"""+body_email_members+"""</td>
	</tr>
	</table>
	</body>"""
		'''frappe.sendmail(recipients="rengaraj.nishta@gmail.com",
                        subject="[NISHTA-PMS] [{frequency}] {name}".format(
                            frequency="test by rengaraj", name="test by rengaraj"),
                        message=body_email, bulk=True)'''
		frappe.msgprint(body_email)
			


@frappe.whitelist()
def employee_values_load(naming_series=None):
    return_values=frappe.db.sql("""select employee_name,hourly_rate from tabEmployee where employee=%s""",naming_series)
    return return_values

	

