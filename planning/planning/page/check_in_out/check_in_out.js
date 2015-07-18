//alert(frappe.get_user());
frappe.pages['check-in-out'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Task check-in-out',
		single_column: true
	});
	frappe.call({
		method:"planning.planning.page.check_in_out.check_in_out.getTask",
		args:{"doctype":"NNTask"},
		callback:function(data){
			page.main.append(frappe.render_template('check_in_out', {data:data.message}))
		}
	});

	//load();
}
function check_in_out_status(rowid)
{
	var data=$("#v"+rowid).val().split(",");
	var task_name=data[0];
	var check_status=data[1]; 
	var name=data[2];
	var lab="";
	if(check_status==2)
	{
		lab="Check Out";
	}
    if(check_status==1)
	{
		lab="Check In";
	}
frappe.confirm(
    'Are you sure to '+lab+'?',
    function(){
        window.close();
        frappe.call({
		method:"planning.planning.page.check_in_out.check_in_out.checking_checkout",
		args:{"task":task_name,"check_status":check_status,"name":name},
		callback:function(data){
				location.reload();
		}
	})
    },
    function(){
               window.close();
    }
)

	
	
}
function close_task(task_name,check_status,name,assign_name)
{
 if(check_status==2)
 {
 	check_in_out_status(task_name,check_status,name)
 }
 lab="Close";
 frappe.confirm(
    'Are you sure to '+lab+'?',
    function(){
 frappe.call({
	method:"planning.planning.page.check_in_out.check_in_out.close_task",
		args:{"assign_name":assign_name},
		callback:function(data){
				load();
		}
	})
 },
    function(){
               window.close();
    }
    )
}
function load()
{
		frappe.call({
		method:"planning.planning.page.check_in_out.check_in_out.getTask",
		args:{"doctype":"NNTask"},
		callback:function(data){
			len_data=data.message.length;
			values=data.message;
			emp=values[0][4]
			table_start="<table border='1' width='100%'><BR><BR><tr><th colspan='9' style='text-align:center;'>"+emp+"</th>";
			table_th="<Tr><th>S.No</th><th>Project</th><th>Milestone</th><th>TaskList</th><th>Task</th><th>Scheduled Time</th><th>Worked Time</th><th>Status</th><th>Close</th><tr>";
			results=table_start+table_th;
			for(i=0;i<len_data;i++)
			{
			sno=i+1;
			project=values[i][0]
			milestone=values[i][1]
			tasklist=values[i][2]
			task=values[i][3]
			emp=values[i][4]
			chekin_status=values[i][5]
			chekin_name=values[i][6]
			duration=values[i][7]
			worked_time=values[i][8];
			assign_name=values[i][9];
			if(chekin_status==1)
			{
				che_lab="CheckOut";
				check_state=2;
			}
			else
			{
				che_lab="CheckIn";
				check_state=1;
			}

			//task_click=task.replace(" ", "~~"); 
			task_click=task.replace(/\s/g,'~~'); 
			//alert(task_click);
			status=""
			results+="<tr>";
			results+="<td>"+sno+"</td>";
			results+="<td>"+project+"</td>";
			results+="<td>"+milestone+"</td>";
			results+="<td>"+tasklist+"</td>";
			results+="<td>"+task+"</td>";
			results+="<td>"+duration+"</td>";
			results+="<td>"+worked_time+"</td>";
			results+="<td><div onclick=check_in_out_status('"+task_click+"','"+check_state+"','"+chekin_name+"');>"+che_lab+"</div></td>";
			results+="<td><div onclick=close_task('"+task_click+"','"+check_state+"','"+chekin_name+"','"+assign_name+"');>Close</div></td>";
			results+="</tr>";
			//results+="<Tr><Td>"+sno+"</td><td>"+project+"</td><td>"+milestone+"</td><td>"+tasklist+"</td><td>"+task+"</td><td><div onclick=check_in_out_status('"+task_click+"','"+check_state+"','"+chekin_name+"');>"+che_lab+"</div></td><td>Close</td><tr>";
			}
			results+="</table>";
			$("#check_grids").html(results);
		}
	})
}
function conform()
{

}//alert(frappe.get_user());
frappe.pages['check-in-out'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Task check-in-out',
		single_column: true
	});
	frappe.call({
		method:"planning.planning.page.check_in_out.check_in_out.getTask",
		args:{"doctype":"NNTask"},
		callback:function(data){
			page.main.append(frappe.render_template('check_in_out', {data:data.message}))
		}
	});

	//load();
}
function check_in_out_status(rowid)
{
	var data=$("#v"+rowid).val().split(",");
	var task_name=data[0];
	var check_status=data[1]; 
	var name=data[2];
	var lab="";
	if(check_status==1)
	{
		lab="Check Out";
	}
    if(check_status==0)
	{
		lab="Check In";
	}
frappe.confirm(
    'Are you sure to '+lab+'?',
    function(){
        window.close();
        frappe.call({
		method:"planning.planning.page.check_in_out.check_in_out.checking_checkout",
		args:{"task":task_name,"check_status":check_status,"name":name},
		callback:function(data){
				location.reload();
		}
	})
    },
    function(){
               window.close();
    }
)

	
	
}
function close_task(rowid)
{
	var data=$("#v"+rowid).val().split(",");
	var task_name=data[0];
	var check_status=data[1]; 
	var name=data[2];
	var assign_name=data[3];

 if(check_status==1)
 {
 	//check_in_out_status(rowid)
 }
 lab="Close";
 frappe.confirm(
    'Are you sure to '+lab+'?',
    function(){
 frappe.call({
	method:"planning.planning.page.check_in_out.check_in_out.close_task",
		args:{"assign_name":assign_name},
		callback:function(data){
				location.reload();
		}
	})
 },
    function(){
               window.close();
    }
    )
}
function load()
{
		frappe.call({
		method:"planning.planning.page.check_in_out.check_in_out.getTask",
		args:{"doctype":"NNTask"},
		callback:function(data){
			len_data=data.message.length;
			values=data.message;
			emp=values[0][4]
			table_start="<table border='1' width='100%'><BR><BR><tr><th colspan='9' style='text-align:center;'>"+emp+"</th>";
			table_th="<Tr><th>S.No</th><th>Project</th><th>Milestone</th><th>TaskList</th><th>Task</th><th>Scheduled Time</th><th>Worked Time</th><th>Status</th><th>Close</th><tr>";
			results=table_start+table_th;
			for(i=0;i<len_data;i++)
			{
			sno=i+1;
			project=values[i][0]
			milestone=values[i][1]
			tasklist=values[i][2]
			task=values[i][3]
			emp=values[i][4]
			chekin_status=values[i][5]
			chekin_name=values[i][6]
			duration=values[i][7]
			worked_time=values[i][8];
			assign_name=values[i][9];
			if(chekin_status==1)
			{
				che_lab="CheckOut";
				check_state=2;
			}
			else
			{
				che_lab="CheckIn";
				check_state=1;
			}

			//task_click=task.replace(" ", "~~"); 
			task_click=task.replace(/\s/g,'~~'); 
			//alert(task_click);
			status=""
			results+="<tr>";
			results+="<td>"+sno+"</td>";
			results+="<td>"+project+"</td>";
			results+="<td>"+milestone+"</td>";
			results+="<td>"+tasklist+"</td>";
			results+="<td>"+task+"</td>";
			results+="<td>"+duration+"</td>";
			results+="<td>"+worked_time+"</td>";
			results+="<td><div onclick=check_in_out_status('"+task_click+"','"+check_state+"','"+chekin_name+"');>"+che_lab+"</div></td>";
			results+="<td><div onclick=close_task('"+task_click+"','"+check_state+"','"+chekin_name+"','"+assign_name+"');>Close</div></td>";
			results+="</tr>";
			//results+="<Tr><Td>"+sno+"</td><td>"+project+"</td><td>"+milestone+"</td><td>"+tasklist+"</td><td>"+task+"</td><td><div onclick=check_in_out_status('"+task_click+"','"+check_state+"','"+chekin_name+"');>"+che_lab+"</div></td><td>Close</td><tr>";
			}
			results+="</table>";
			$("#check_grids").html(results);
		}
	})
}
function conform()
{

}