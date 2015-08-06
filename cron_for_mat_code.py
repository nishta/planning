from __future__ import unicode_literals
import frappe, json

from frappe.utils import cstr, flt, getdate
from frappe import _
from frappe.utils.file_manager import save_file
from frappe.translate import (set_default_language, get_dict,
	get_lang_dict, send_translations, get_language_from_code)
from frappe.geo.country_info import get_country_info

@frappe.whitelist()
def product_code_gen():
	prodcut_lists=frappe.db.sql("""select*from tabItem where material_type=%s and prefix='' limit 0,25""",material_type,as_dict=True)
	for product_list in prodcut_lists:
		name=product_list['name']
		item_group=product_list['item_group']
		item_division=product_list['item_division']
		customer_name=product_list['customer_name']
		product_short_name=product_list['product_short_name']
		item_groups=item_group.split(" ")
		if(len(item_groups)>=2):
			item_groups_one=item_groups[0];
			item_groups_two=item_groups[1];
			item_group_first_letter = item_groups_one[0]
			item_group_second_letter = item_groups_two[0]
		if(len(item_groups)<2):
			tem_groups_one=item_groups[0];
			item_group_first_letter = item_groups_one[0]
			item_group_second_letter = item_groups_one[1]
		item_group_letters=str(item_group_first_letter)+str(item_group_second_letter)
		auto_number_div= frappe.db.get_value("Item Division", item_division, "auto_number")
		if auto_number_div==None:
			auto_number_div=0;
		short_cust= frappe.db.get_value("Customer", customer_name, "short_name")
		prefix=str(item_group_letters)+str(auto_number_div)+str(short_cust)+str(product_short_name)
		count_rows=frappe.db.count("Item",filters={'prefix':prefix,'material_type':"Product"})
		count_rows=count_rows+1;
		if(count_rows>=0 and count_rows<10):
			str_num="0";
		else:
			str_num="";
		prefix=prefix.upper();
		item_code=prefix+str_num+str(count_rows);
		item_code=item_code.upper();
		barcode=item_code
		frappe.db.sql("""update tabItem set item_code=%s,barcode=%s,name=%s,prefix=%s where name=%s""",(item_code,item_code,item_code,prefix,name))
		frappe.msgprint(item_code+"--"+name+"--"+prefix)

@frappe.whitelist()
def today_cron():
	date="2015-08-05"
	item_lists=frappe.db.sql("""select * from tabItem where material_type=%s and has_variants='1' and variant_of is Null and date(creation)=%s""",material_type,as_dict=True)
	for item_list in item_lists:
		name=item_list['name']
		frappe.msgprint(name)

@frappe.whitelist()
def prefix_set():
	material_type="Item"
	item_lists=frappe.db.sql("""select * from tabItem where material_type=%s and has_variants='1' and variant_of is Null and prefix=''""",material_type,as_dict=True)
	for item_list in item_lists:
		name=item_list['name']
		prefix=name[0:13]
		frappe.msgprint(prefix+"--"+name)
		frappe.db.sql("Update tabItem set prefix=%s where name=%s",(prefix,name))
		variant_lists=frappe.db.sql("""select *from tabItem where variant_of=%s""",name,as_dict=True)
		for variant_list in variant_lists:
			name_variants=variant_list['name']
			name_variants_split=name_variants.split("-")
			new_name=name_variants_split[1]
			prefix_variant=prefix+new_name
			frappe.db.sql("""update tabItem set prefix=%s where name=%s""",(prefix_variant,name_variants))
		

@frappe.whitelist()
def item_code_for_active():
	frappe.msgprint("test")
	material_type="Item"
	item_lists=frappe.db.sql("""select * from tabItem where material_type=%s and has_variants='0' and variant_of is Null and prefix=''""",material_type,as_dict=True)
	for item_list in item_lists:
		name=item_list['name']
		item_group=item_list['item_group']
		item_group_first = item_group[0]
		item_division=item_list['item_division']
		auto_number_div= frappe.db.get_value("Item Division", item_division, "auto_number")
		if auto_number_div==None:
			auto_number_div=0;
		customer_name=item_list['customer_name']
		short_cust= frappe.db.get_value("Customer", customer_name, "short_name")
		#short_product=item_list['item_division']
		pro_name=item_list['product']
		if(pro_name!=""):
			short_product= frappe.db.get_value("Item", pro_name, "product_short_name")
		else:
			short_product=""
		if short_product == None:
			frappe.msgprint("Product Short Name Not Set for "+name+" So Please Set Product Short Name",raise_exception=1);
			#
		package_category=item_list['package_category']
		if package_category!="":
			package_category_letter = package_category[0]
		else:
			frappe.msgprint("package_category Missing for "+name)
		category=item_list['item_category']
		if(category!=""):
			#frappe.msgprint(category,raise_exception=1)
			auto_number_cat= frappe.db.get_value("Item Category", category, "auto_number")
			if auto_number_cat==None:
				auto_number_cat=0;
				auto_number_cat=int(auto_number_cat);
			if(auto_number_cat<10):
				auto_number_cat="0"+str(auto_number_cat)
		else:
			auto_number_cat="00"
		subcategory=item_list['item_sub_category']
		if(subcategory!=""):
			auto_number_sub= frappe.db.get_value("Item Subcategory", subcategory, "auto_number")
			if auto_number_sub==None:
				auto_number_sub=0;
				auto_number_sub=int(auto_number_sub);
			if(auto_number_sub<10):
				auto_number_sub="0"+str(auto_number_sub)
		else:
			auto_number_sub="00"
		prefix=str(item_group_first)+str(auto_number_div)+str(short_cust)+str(short_product)+str(package_category_letter)+str(auto_number_cat)+str(auto_number_sub)
		count_rows=frappe.db.count("Item",filters={'prefix':prefix,'material_type':"Item"})
		count_rows=count_rows+1;
		if(count_rows>=0 and count_rows<10):
			str_num="000";
		elif(count_rows>=10 and count_rows<100):
			str_num="00"
		elif(count_rows>=100 and count_rows<1000):
			str_num="0"
		else:
			str_num="";
		item_code=prefix+str_num+str(count_rows);
		item_code=item_code.upper();
		prefix=prefix.upper();
		#frappe.msgprint(prefix+"--"+name+"--"+item_code)
		frappe.db.sql("""update tabItem set item_code=%s,barcode=%s,name=%s,prefix=%s where name=%s""",(item_code,item_code,item_code,prefix,name))

@frappe.whitelist()
def item_code_for_template():
	material_type="Item"
	item_lists=frappe.db.sql("""select * from tabItem where material_type=%s and has_variants='1'  and prefix='' and  order by name asc""",material_type,as_dict=True)
	for item_list in item_lists:
		name=item_list['name']
		item_group=item_list['item_group']
		item_group_first = item_group[0]
		item_division=item_list['item_division']
		auto_number_div= frappe.db.get_value("Item Division", item_division, "auto_number")
		if auto_number_div==None:
			auto_number_div=0;
		customer_name=item_list['customer_name']
		short_cust= frappe.db.get_value("Customer", customer_name, "short_name")
		#short_product=item_list['item_division']
		pro_name=item_list['product']
		if(pro_name!=""):
			short_product= frappe.db.get_value("Item", pro_name, "product_short_name")
		else:
			short_product=""
		if short_product == None:
			frappe.msgprint("Product Short Name Not Set for "+name+" So Please Set Product Short Name",raise_exception=1);
			#
		package_category=item_list['package_category']
		if package_category!="":
			package_category_letter = package_category[0]
		else:
			frappe.msgprint("package_category Missing for "+name)
		category=item_list['item_category']
		if(category!=""):
			#frappe.msgprint(category,raise_exception=1)
			auto_number_cat= frappe.db.get_value("Item Category", category, "auto_number")
			if auto_number_cat==None:
				auto_number_cat=0;
				auto_number_cat=int(auto_number_cat);
			if(auto_number_cat<10):
				auto_number_cat="0"+str(auto_number_cat)
		else:
			auto_number_cat="00"
		subcategory=item_list['item_sub_category']
		if(subcategory!=""):
			auto_number_sub= frappe.db.get_value("Item Subcategory", subcategory, "auto_number")
			if auto_number_sub==None:
				auto_number_sub=0;
				auto_number_sub=int(auto_number_sub);
			if(auto_number_sub<10):
				auto_number_sub="0"+str(auto_number_sub)
		else:
			auto_number_sub="00"
		prefix=str(item_group_first)+str(auto_number_div)+str(short_cust)+str(short_product)+str(package_category_letter)+str(auto_number_cat)+str(auto_number_sub)
		count_rows=frappe.db.count("Item",filters={'prefix':prefix,'material_type':"Item"})
		count_rows=count_rows+1;
		if(count_rows>=0 and count_rows<10):
			str_num="000";
		elif(count_rows>=10 and count_rows<100):
			str_num="00"
		elif(count_rows>=100 and count_rows<1000):
			str_num="0"
		else:
			str_num="";
		item_code=prefix+str_num+str(count_rows);
		item_code=item_code.upper();
		prefix=prefix.upper();
		frappe.msgprint(prefix+"--"+name+"--"+item_code)
		variant_lists=frappe.db.sql("""select *from tabItem where variant_of=%s""",name,as_dict=True)
		for variant_list in variant_lists:
			name_variants=variant_list['name']
			name_variants_split=name_variants.split("-")
			new_name=name_variants_split[1]
			variant_code=item_code+'-'+new_name
			prefix_variant=prefix+new_name
			variant_code=str(variant_code)
			#count=frappe.db.sql("""select tabItem from name=%s""",(variant_code));
			frappe.db.sql("""update tabItem set item_code=%s,barcode=%s,name=%s,prefix=%s where name=%s""",(variant_code,variant_code,variant_code,prefix_variant,name_variants))
		#frappe.msgprint(prefix+"--"+name+"--"+item_code)
		frappe.db.sql("""update tabItem set item_code=%s,barcode=%s,name=%s,prefix=%s where name=%s""",(item_code,item_code,item_code,prefix,name))

@frappe.whitelist()
def customer_code_cron():
	customer_lists=frappe.db.sql("""select *from `tabCustomer` where counting_number='0'""",as_dict=True)
	for customer_list in customer_lists:
		name=customer_list['customer_name'];
		customer_category=customer_list['customer_category']
		if customer_category:
			customer_category_first_letter=customer_category[0]
		else:
			frappe.msgprint("Customer Category Not Not Set For --"+name)
			customer_category_first_letter=""
		name_first_letter= name[0]
		cust_prefix="C"+customer_category_first_letter+name_first_letter;
		count_rows=frappe.db.count("Customer",filters={'customer_category':customer_category})
		if(count_rows==0):
			count_rows=count_rows+101;
		else:
			max_count=frappe.db.sql("""select max(counting_number) from tabCustomer where customer_category=%s """,customer_category)
			if (max_count):
				max_num=(max_count[0][0]);
				if(max_num>0):
					#frappe.msgprint(max_num+"max")
					count_rows=int(max_num)+101
				else:
					count_rows=101;
			else:
				count_rows=101;
		if(count_rows>=100 and count_rows<1000):
			str_num="0"
		else:
			str_num="";
		counting_number=int(count_rows)-100;
		customer_code=cust_prefix+str_num+str(count_rows)
		customer_code=customer_code.upper();
		customer_code=customer_code
		frappe.db.sql("""update `tabCustomer` set customer_code=%s,counting_number=%s where name=%s""",(customer_code,counting_number,name))
		frappe.msgprint(customer_code+"--"+name+"--"+str(counting_number))

@frappe.whitelist()
def supplier_code_cron():
	frappe.msgprint("TESTSfds");
	supplier_lists=frappe.db.sql("""select *from `tabSupplier` where counting_number='0'""",as_dict=True)
	for supplier_list in supplier_lists:
		supplier_category=supplier_list['supplier_category']
		name=supplier_list['name']
		supplier_category_first_letter=supplier_category[0];
		supplier_division=supplier_list['supplier_division']
		if not supplier_division:
			supplier_division="Common";
			frappe.db.sql("Update `tabSupplier` set supplier_division=%s",supplier_division)
		auto_number_div= frappe.db.get_value("Item Division", supplier_division, "auto_number")
		supplier_name=supplier_list['supplier_name'];
		supplier_name_first_letter=supplier_name[0];
		max_count=frappe.db.sql("""select max(counting_number) from tabSupplier where supplier_category=%s and supplier_division=%s """,(supplier_category,supplier_division))
		if max_count:
			max_num=(max_count[0][0]);
		else:
			max_num=0
		if max_num<1:
			count_rows=0
		else:
			count_rows=max_num
		count_rows=int(count_rows)+int(101);
		if(count_rows>=100 and count_rows<1000):
			str_num="0"
		else:
			str_num="";
		counting_number=count_rows-100
		prefix="S"+supplier_category_first_letter+str(auto_number_div)+supplier_name_first_letter
		supplier_code=prefix+str_num+str(count_rows)
		supplier_code=supplier_code.upper()
		supplier_code=supplier_code
		frappe.db.sql("""update tabSupplier set supplier_code=%s,counting_number=%s where name=%s""",(supplier_code,counting_number,name))
		frappe.msgprint(supplier_code+"--"+str(count_rows)+"--"+supplier_name+"-//-"+supplier_division)