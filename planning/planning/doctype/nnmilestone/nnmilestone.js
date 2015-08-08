frappe.ui.form.on("NNMilestone","expected_start_date",function(frm)
{   
if (frm.doc.expected_start_date <get_today() ) 
  {    frm.doc.expected_start_date=""
        frm.refresh_field("expected_start_date")
        msgprint("You can not select Past date in Start Date");
        validated = false;
  }

});
frappe.ui.form.on("NNMilestone","expected_end_date",function(frm)
{   
if (frm.doc.expected_end_date <get_today() ) 
  {
        frm.doc.expected_end_date=""
        frm.refresh_field("expected_end_date")
        msgprint("You can not select Past date in End Date");
        validated = false;
  }
 if (frm.doc.expected_start_date >frm.doc.expected_end_date ) 
  {   frm.doc.expected_end_date=""
        frm.refresh_field("expected_end_date")
        msgprint("Please Select Vaild Expected End Date");
        validated = false;
  }
});

frappe.ui.form.on("NNMilestone","actual_start_date",function(frm)
{   
if (frm.doc.actual_start_date <get_today() ) 
  {    frm.doc.actual_start_date=""
        frm.refresh_field("actual_start_date")
        msgprint("You can not select Past date Actual Start Date");
        validated = false;
  }

});
frappe.ui.form.on("NNMilestone","actual_end_date",function(frm)
{   
if (frm.doc.actual_end_date <get_today() ) 
  {
        frm.doc.actual_end_date=""
        frm.refresh_field("actual_end_date")
        msgprint("You can not select Past date in Actual End Date");
        validated = false;
  }
 if (frm.doc.actual_start_date >frm.doc.actual_end_date ) 
  {   frm.doc.actual_end_date=""
        frm.refresh_field("actual_end_date")
        msgprint("Please Select Vaild Actual End Date");
        validated = false;
  }
});