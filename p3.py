from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
import requests


def f0():
	root.withdraw()
	aw.deiconify()

def f2():

	aw.withdraw()
	root.deiconify()

#     ADD DATA
	
def add_data():
	con=None
	try:
		con=connect("ems")
		cursor=con.cursor()
		sql="insert into emp values('%d','%s','%f')"
		id=int(aw_ent_id.get())
		name=aw_ent_name.get()
		salary=float(aw_ent_salary.get())
		
		cursor.execute(sql%(id,name,salary))
		if len(name)== 0:
			showerror("Message","name can't be empty")
		elif any(ch.isdigit() for ch in  name):
			showerror("Message","Name can't have numbers")
		elif len(name)<2:
			showerror("Message","name is too short.")
		elif len(name)>20:
			showerror("Message","name is too long ")
		elif id<1:
			showerror("Message", "id should have only positive integers")

		elif salary<=5000:
			showerror("Message", "salary should be minimum 500")		

		else:			
			con.commit()
			showinfo("Success","Data Saved Successfully")
			
	except Exception as e:
		if con is not None:
			con.rollback()
		showerror("issue: ",e)
	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0,END)                            
		aw_ent_name.delete(0,END)
		aw_ent_salary.delete(0,END)
		aw_ent_id.focus()


#                          	VIEW DATA -FUNCTION
def view_data():
	
	root.withdraw()
	vw.deiconify()
	vw_sc.delete(1.0,END)
	con=None
	try:
		con=connect("ems")
		cursor=con.cursor()
		sql="select * from emp order by id"
		cursor.execute(sql)
		data=cursor.fetchall()	
		info=""	
		for d in data:
			info=info+"\nid="+str(d[0])+"\nname="+str(d[1])+"\nsalary="+str(d[2])+"\n"+("-"*10)+"\n"
		vw_sc.insert(INSERT,info)
	except Exception as e:
		print(e)
	
	finally:
		if con is not None:
			con.close()

def f4(): 
	vw.withdraw()
	root.deiconify()


	

def f5():
	
	root.withdraw()
	up.deiconify()

def f6():
	up.withdraw()
	root.deiconify()

def f7():
	root.withdraw()
	dele.deiconify()

	
def f8():
	dele.withdraw()
	root.deiconify()

#                               DELETE FUNCTION

	
def delete_data():
	con=None
	try:
		con=connect("ems")
		cursor=con.cursor()
		sql="delete from emp where id=%d"
		id=int(dele_ent_id.get())
		cursor.execute(sql%(id))
		if cursor.rowcount==1:
			con.commit()
			showinfo("Success","Data deleted successfully")
		else:
			showerror("Error","record dosen't exists")
	except Exception as e:
		con.rollback()
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
		dele_ent_id.delete(0,END)
		dele_ent_id.focus()

#            UPDATE DATA
def update_data():
	con=None
	try:
		con=connect("ems")
		cursor=con.cursor()
		sql="update emp SET name='%s',salary='%f' WHERE id='%d'"
		id=int(up_ent_id.get())
		name=up_ent_name.get()
		salary=float(up_ent_salary.get())
		data=(name,salary,id)
		cursor.execute(sql%(data))
		if len(name)== 0:
			showerror("message","name can't be empty")
		elif any(ch.isdigit() for ch in  name):
			showerror("message","Name can't have numbers")
		elif len(name)<2:
			showerror("message","name is short.")
		elif len(name)>20:
			showerror("message","name is too long ")

		elif salary<=8000:
			showerror("message", "salary should be minimum 8k")		

		elif cursor.rowcount==1:
			con.commit()
			showinfo("Success","Data updated successfully")
		else:
			showerror("Error","record dosen't exists")
	except Exception as e:
		con.rollback()
		showerror("issue: ",e)
	finally:
		if con is not None:
			con.close()
		up_ent_id.delete(0,END)
		up_ent_name.delete(0,END)
		up_ent_salary.delete(0,END)
		up_ent_id.focus()

#     CHART
def chart():
	con=None
	try:
		con=connect("ems")
		sql="select name,salary from emp group by salary order by salary desc limit 5 "
		data =pd.read_sql(sql,con)
		plt.bar(data.name,data.salary,color="lightblue")
		plt.xlabel("Name of employees")
		plt.ylabel("salary of employees")
		plt.title("Salary graph of Employees")
		plt.show()
		con.commit()
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()

def f13():
	root.withdraw()
	crt.deiconify()

def f14():
	crt.withdraw()
	root.deiconify()

root=Tk()
root.title("Employee Managment System")
root.geometry("1000x600+100+100")
root.iconbitmap("list.ico")
root.configure(bg="linen")

f=("Simsun",30,"bold")
f1=("FreeSerif",20,"bold")

add_btn=Button(root,text=" Add ",font=f,command=f0,bg="DarkOliveGreen1")
view_btn=Button(root,text=" View ",font=f,command=view_data,bg="peach puff")
up_btn=Button(root,text="Update",font=f,command=f5,bg="SteelBlue1")
del_btn=Button(root,text="Delete",font=f,command=f7,bg="indian red")
crt_btn=Button(root,text="Charts",font=f,command=f13,bg="azure")

add_btn.pack(pady=10)
view_btn.pack(pady=10)
up_btn.pack(pady=10)
del_btn.pack(pady=10)
crt_btn.pack(pady=10)

#Add Window

aw=Toplevel(root)
aw.title("Add Employee")
aw.geometry("1000x500+100+100")
aw.iconbitmap("list.ico")
aw.configure(bg="linen")
aw_lab_id=Label(aw,text="Enter id",font=f)
aw_ent_id=Entry(aw,font=f)
aw_lab_name=Label(aw,text="Enter name",font=f)
aw_ent_name=Entry(aw,font=f)
aw_lab_salary=Label(aw,text="Entre salary",font=f)
aw_ent_salary=Entry(aw,font=f)

aw_btn_save=Button(aw,text="Save",font=f,command=add_data,bg="old lace")
aw_btn_back=Button(aw,text="Back",font=f,command=f2,bg="hot pink")


aw_lab_id.pack()
aw_ent_id.pack()

aw_lab_name.pack()
aw_ent_name.pack()

aw_lab_salary.pack()
aw_ent_salary.pack()

aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

aw.withdraw()


#View Window


vw=Toplevel(root)
vw.title("View Employee data")
vw.geometry("1000x600+50+50")
vw.iconbitmap("list.ico")
vw.configure(bg="linen")
vw_sc=ScrolledText(vw,font=f,width=20,height=10)
vw_btn=Button(vw,text="Back",font=f,command=f4,bg="orange")

vw_sc.pack()
vw_btn.pack()

vw.withdraw()



#Update Window

up=Toplevel(root)
up.title("Update Employee data")
up.geometry("1000x600+50+50")
up.iconbitmap("list.ico")
up.configure(bg="linen")
up_lab_id=Label(up,text="Enter id",font=f)
up_ent_id=Entry(up,font=f)
up_lab_name=Label(up,text="Enter name",font=f)
up_ent_name=Entry(up,font=f)
up_lab_salary=Label(up,text="Enter salary",font=f)
up_ent_salary=Entry(up,font=f)

up_btn_save=Button(up,text="Update",font=f,command=update_data,bg="light coral")
up_btn_back=Button(up,text="Back",font=f,command=f6,bg="cadet blue")

up_lab_id.pack()
up_ent_id.pack()
up_lab_name.pack()
up_ent_name.pack()
up_lab_salary.pack()
up_ent_salary.pack()
up_btn_save.pack(pady=10)
up_btn_back.pack(pady=10)

up.withdraw()

#Delete window

dele=Toplevel(root)
dele.title("Delete Employee data")
dele.geometry("1000x500+100+100")
dele.iconbitmap("list.ico")
dele.configure(bg="linen")

dele_lab_id=Label(dele,text="Enter id",font=f)
dele_ent_id=Entry(dele,font=f)


dele_btn_del=Button(dele,text="Delete",font=f,command=delete_data,bg="blanched almond")
dele_btn_back=Button(dele,text="Back",command=f8,font=f,bg="lavender")


dele_lab_id.pack(pady=10)
dele_ent_id.pack(pady=10)
dele_btn_del.pack(pady=10)
dele_btn_back.pack(pady=10)

dele.withdraw()


#chart


crt=Toplevel(root)
crt.title("Chart")
crt.geometry("1000x500+100+100")
crt.iconbitmap("list.ico")
crt.configure(bg="linen")


crt_lab=Label(crt,text="Employee Salary Chart",font=f)
crt_btn=Button(crt,text="Create Chart",font=f,command=chart,bg="dark salmon")
crt_btn_back=Button(crt,text="Go Back",font=f,command=f14,bg="SteelBlue1")

crt_lab.pack(pady=20)
crt_btn.pack(pady=20)
crt_btn_back.pack(pady=20)

crt.withdraw()


#location 
lab_loc1 = Label(root,text="Location=",font=f1,bg="LightSkyBlue1",fg="DodgerBlue4")
wa="https://ipinfo.io/"
res=requests.get(wa)
data= res.json()
city=data["city"]
lab_loc2 = Label(root,text=str(city),font=f1,bg="LightSkyBlue1",fg="DodgerBlue4")

#temperature
lab_temp1 = Label(root,text="Temperature=",font=f1,bg="LightSkyBlue1",fg="DodgerBlue4")

a1 = "https://api.openweathermap.org/data/2.5/weather?"
a2 = "q=" +str(city)
a3 = "&appid=" + "7f9879e9039f9047b7221233b173e305"
a4 = "&units=" + "metric"
	
wa = a1 + a2 + a3 + a4
res = requests.get(wa)	
data = res.json()
	
p =int(data["main"]["temp"])
tem=str(p)

lab_temp2 = Label(root,text=str(p),font=f1,bg="LightSkyBlue1",fg="DodgerBlue4")
lab_temp3 = Label(root,text=" ℃",font=f1,bg="LightSkyBlue1",fg="DodgerBlue4")

lab_loc1.place(x=100,y=500)
lab_loc2.place(x=230,y=500)
lab_temp1.place(x=650,y=500)
lab_temp2.place(x=840,y=500)
lab_temp3.place(x=875,y=500)

root.mainloop()