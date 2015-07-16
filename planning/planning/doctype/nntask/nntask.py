# -*- coding: utf-8 -*-
# Copyright (c) 2015, nishta and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class NNTask(Document):
	pass

@frappe.whitelist()
def employee_values_load(naming_series=None):
    return_values=frappe.db.sql("""select employee_name,hourly_rate from tabEmployee where employee=%s""",naming_series)
    return return_values

	

