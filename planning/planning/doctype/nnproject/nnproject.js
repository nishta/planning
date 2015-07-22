
//frappe.provide("planning.planning");


cur_frm.cscript.members = function(doc, cdt, cdn) {
    var d = locals[cdt][cdn];
    var members = d.members;
    d.category = null;
    
    // //alet("sdfdsf:");
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

