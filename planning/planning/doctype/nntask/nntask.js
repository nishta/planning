
//frappe.provide("planning.planning");

var frm=""
cur_frm.cscript.members = function(doc, cdt, cdn) {
    var d = locals[cdt][cdn];
    var members = d.members;
    d.category = null;
    cur_frm.call({
        method : "employee_values_load",
        args : {
            naming_series : members
        },
        callback : function(r) {
            if (!r.exc) {
                var doclist = frappe.model.sync(r.message);
                var s = locals[cdt][cdn];
                employee_name = doclist[0][0];
                hourly_rate = doclist[0][1];            
                s.employee_name = employee_name;
                s.hourly_rate = hourly_rate;
                cur_frm.refresh_fields();
            }

        }
    });

}
 
   
    cur_frm.fields_dict['assign_to'].grid.get_field('members').get_query = function(doc,cdt, cd) {
        //alert(doc.tasklist)
       tasklist=doc.tasklist
        return{
        query: "planning.planning.myfunction.load_employee_name",
        filters: {
            "taskList":tasklist
        }
    }
}

frappe.ui.form.on("NNTask","expected_start_date",function(frm)
{   
if (frm.doc.expected_start_date <get_today() ) 
  {    frm.doc.expected_start_date=""
        frm.refresh_field("expected_start_date")
        msgprint("You can not select Past date in Start Date");
        validated = false;
  }

});
frappe.ui.form.on("NNTask","expected_end_date",function(frm)
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
