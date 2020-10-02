import mysql.connector as sql
from tkinter import *
from tkinter import messagebox
import random
import functions as func
from functions import spc, not_spc1, not_spc2, not_spc3


try:
    conn = sql.connect(host="127.0.0.1", user="root", passwd="12345678", database="passwordmanager")
    cur = conn.cursor()
except:
    messagebox.showerror("Connection Problem", "The Application Is Unable To Connect To The Database")
    sys.exit(0)


##################------------------------DASHBOARD PAGE FUNCTIONS----------------------####################

def password_generator():
	pg = Tk()
	pg.geometry("350x150")
	pg.title("Password Generator (P-Protect)")
	pg.iconbitmap("icons/list.ico")
	pg.resizable(0,0)
	def pass_gen():
		pass_entry_text = ""
		generated = ""
		choice_lst = []
		length = random.randint(9,10)
		for i in range(length+1):
			special = random.choice(spc)
			number = random.choice(not_spc1)
			non_special = random.choice(not_spc2)
			non_special2 = random.choice(not_spc3)
			choice_lst.append(special)
			choice_lst.append(number)
			choice_lst.append(non_special)
			choice_lst.append(non_special2)
			choice = random.choice(choice_lst)
			generated += str(choice)
		pass_entry.delete(0, END)
		pass_entry_text = generated
		pass_entry.insert(END, pass_entry_text)
		# print(generated)
	empty = Label(pg, text="        ")
	empty.pack()
	pass_label = Label(pg, text="GENERATE PASSWORD", font=('bold',14), fg="red")
	pass_label.pack()
	empty = Label(pg, text="         ")
	empty.pack()
	global pass_entry_text
	pass_entry_text = StringVar()
	global pass_entry
	pass_entry = Entry(pg, textvariable=StringVar)
	pass_entry.pack()
	empty = Label(pg, text="         ")
	empty.pack()
	pass_btn = Button(pg, text="GENERATE", font=5, fg="black", bg="yellow", command=pass_gen)
	pass_btn.pack()
	pg.mainloop()



## ADD Button Function --> This function will add data to the database and then populates the list-box
def add():
	main_util = main_utility_entry.get().strip()
	sub_util = sub_utility_entry.get().strip()
	pass_util = pass_utility_entry.get().strip()
	sub_util = "        " if sub_util.strip() == "" else sub_util
	if main_util == "" or pass_util == "":
		messagebox.showerror("Empty", "These Fields Cannot Be Empty")
		return
	q = "INSERT INTO UTILITIES VALUES ({},'{}','{}','{}')".format(func.next_id(), main_util, sub_util, pass_util)
	cur.execute(q)
	conn.commit()
	clear()
	populate_list_data()


## DELETE Button Function --> In The Dashboard Page
def delete():
	if selected_item[0] != 1:
		func.sort_insert_id()
		print(selected_item[0])
		q = "DELETE FROM UTILITIES WHERE ID={}".format(selected_item[0])
		cur.execute(q)
		conn.commit()
		clear()
		populate_list_data()
		return
	else:
		clear()
		messagebox.showinfo("Cannot Delete", "You Cannot Delete The First Column")
		return

	

## UPDATE Button Function --> In The Dashboard Page
def update():
	if selected_item[0] != 1:
		main_util = main_utility_entry.get().strip()
		sub_util = sub_utility_entry.get().strip()
		pass_util = pass_utility_entry.get().strip()
		if main_util == "":
			messagebox.showerror("Empty", "Utility-Name Cannot Be Empty")
			return
		if pass_util == "":
			messagebox.showerror("Empty", "Utility-Password Cannot Be Empty")
			return
		sub_util = "       " if sub_util.strip() == "" else sub_util
		q1 = "UPDATE UTILITIES SET UTILITY_NAME='{}' WHERE ID={}".format(main_util, selected_item[0])
		cur.execute(q1)
		q2 = "UPDATE UTILITIES SET UTILITY_SUB_NAME='{}' WHERE ID={}".format(sub_util, selected_item[0])
		cur.execute(q2)
		q3 = "UPDATE UTILITIES SET UTILITY_PASSWORD='{}' WHERE ID={}".format(pass_util, selected_item[0])
		cur.execute(q3)
		conn.commit()
		clear()
		populate_list_data()
		return
	else:
		clear()
		messagebox.showinfo("Cannot Update", "You Cannot Update The First Column")
		return


## CLEAR Button Function --> This function clears the data from the entry fields in the dashboard page
def clear():
	main_utility_entry.delete(0, END)
	sub_utility_entry.delete(0, END)
	pass_utility_entry.delete(0, END)


## This Function Is Responsible For Filling The List-Box of the Dashboard Page with The Appropriate Data Of The User, whenever called.
def populate_list_data():
	func.sort_insert_id()
	data_list.delete(0, END)
	for row in func.fetch_data():
		data_list.insert(END, row)


## This Function Will select the Record in the Listbox which the user selects and then populates the entries
def select_item(event):  
	# To avoid tuple index out of range error we used try and except
	try:
		global selected_item
		index = data_list.curselection()[0]
		selected_item = data_list.get(index)
		print(selected_item)
		main_utility_entry.delete(0, END)
		main_utility_entry.insert(END, selected_item[1])

		sub_utility_entry.delete(0, END)
		sub_utility_entry.insert(END, selected_item[2])

		pass_utility_entry.delete(0, END)
		pass_utility_entry.insert(END, selected_item[3])
	except:
		pass



#####################--------------------------DASHBOARD PAGE --------------------------######################


def dashboard():
	try:
		log.destroy()
	except:
		pass
	global dash ## to be used to reload after the data manipulation
	dash = Tk()
	dash.title("Dashboard (P-Protect)")
	dash.iconbitmap("icons/list.ico")
	dash.geometry("1010x500")
	dash.resizable(0,0)

	# List Box
	global data_list  ## Declared on top to use it in populate_user_data() function
	data_list = Listbox(dash, border=3, height=10, width=55, font=("bold", 15)) ## font can manipulate the width and height of this list-box
	data_list.place(x=20, y=200)

	# Scroll Bar
	scrollbar = Scrollbar(dash)
	scrollbar.place(x=800, y=200)

	# Set Scrollbar to Listbox
	data_list.configure(yscrollcommand=scrollbar.set)
	scrollbar.configure(command=data_list.yview)

	# Bind Select
	data_list.bind('<<ListboxSelect>>', select_item)

	populate_list_data()

	qa = Button(dash, text="Save-n-Quit", font=4, fg="black", bg="orange", command=lambda : sys.exit(0))
	qa.place(x=0, y=0)
	pg = Button(dash, text="Password-Generator", font=4, fg="black", bg="yellow", command=password_generator)
	pg.place(x=100, y=0)

	empty = Label(dash, text="                                                 ")
	empty.place(x=0, y=35)

	main_utility_label = Label(dash, text="Utility-Name : ", font=('bold', 14), fg="red")
	main_utility_label.place(x=10, y=50)

	global main_utility_entry
	main_utility_entry = Entry(dash, width=26) 
	main_utility_entry.place(x=145, y=55)

	sub_utility_label = Label(dash, text="Sub-Utility-Name : ", font=('bold', 14), fg="red")
	sub_utility_label.place(x=315, y=50)

	global sub_utility_entry
	sub_utility_entry = Entry(dash, width=26)
	sub_utility_entry.place(x=490, y=55)

	pass_utility_label = Label(dash, text="Utility-Password : ", font=('bold', 14), fg="red")
	pass_utility_label.place(x=660, y=50)

	global pass_utility_entry
	pass_utility_entry = Entry(dash, width=26)
	pass_utility_entry.place(x=835, y=55)

	empty = Label(dash, text="                        ")
	empty.place(x=0, y=130)

	add_btn = Button(dash, text="ADD", padx=28, pady=4, font=5, fg="black", bg="aqua", command=add)
	add_btn.place(x=150, y=110)

	update_btn = Button(dash, text="UPDATE", padx=15, pady=4, font=5, fg="black", bg="aqua", command=update)
	update_btn.place(x=350, y=110)

	delete_btn = Button(dash, text="DELETE", padx=15, pady=4, font=5, fg="black", bg="aqua", command=delete)
	delete_btn.place(x=550, y=110)

	clear_btn = Button(dash, text="CLEAR", padx=15, pady=4, font=5, fg="black", bg="aqua", command=clear)
	clear_btn.place(x=750, y=110)

	empty = Label(dash, text="                          ")
	empty.place(x=0, y=160)

	dash.mainloop()


### >>>>>>>>>>>>>>>>>------------------------THE LOGGER AND CREATOR-------------------------->>>>>>>>>>>>>>>>>>>  ###

def logger():
	global log
	log = Tk()	
	log.resizable(0,0)
	log.geometry("380x180")
	log.title("Log-In (P-Protect)")
	log.iconbitmap("icons/list.ico")
	empty = Label(log, text="     ")
	empty.pack()
	password_label = Label(log, text="ENTER YOUR PASSWORD : ", font=10, fg='blue')
	password_label.pack()
	empty = Label(log, text="     ")
	empty.pack()
	global password_entry_log
	password_entry_log = Entry(log, show="*", width=35)
	password_entry_log.pack()
	empty = Label(log, text="     ")
	empty.pack()
	btn = Button(log, text="LOG-IN", font=10, fg='black', bg='pink', command=log_in)
	btn.pack()
	log.mainloop()


def creator():
    global password_entry
    global retype_entry
    global create
    create = Tk()
    create.title("Create Password (P-Protect)")
    create.geometry("560x180")
    create.iconbitmap("icons/list.ico")
    create.resizable(0,0)
    initial_empty = Label(create, text=" ")
    initial_empty.grid(row=1, column=0)
    initial_empty = Label(create, text=" ")
    initial_empty.grid(row=3, column=0)
    empty1 = Label(create, text="            ", font=20)
    empty1.grid(row=0,column=0)
    password = Label(create, text="Enter A Password : ", fg="blue", font=20)
    password.grid(row=1,column=1)
    global password_entry
    password_entry = Entry(create, show="*", width=30)
    password_entry.grid(row=1, column=2)
    empty2 = Label(create, text="             ", font=20)
    empty2.grid(row=2,column=0)
    retype = Label(create, text="Retype The Password : ", fg="blue", font=20)
    retype.grid(row=3, column=1)
    retype_entry = Entry(create,show="*", width=30)
    retype_entry.grid(row=3, column=2)
    empty3 = Label(create, text="                        ")
    empty3.grid(row=4, column=1)
    createbtn = Button(create, text="Create Password", padx=2, fg="black", bg="yellow", font=3, command=create_password)
    createbtn.grid(row=5, column=2)
    create.mainloop()


def create_password():
    password = password_entry.get().strip()
    retype = retype_entry.get().strip()
    if password.strip() == "" or retype.strip() == "":
        messagebox.showinfo("Unfilled Form", "Fields Cannot Be Empty")
        return
    if password != retype:
        messagebox.showinfo("Passwords Don't Match", "The Inputted Passwords Don't Match")
        return
    if func.pass_check(password) == False:
        messagebox.showinfo("Password Problem", "The Password Should Be Between 6 to 20 characters and The Password Cannot Be NULL")
        return
    if func.pass_check(password) == True:
        if password == retype:
            q = "UPDATE PASSWORDTABLE SET PASSWORD='{}'".format(password)
            cur.execute(q)
            conn.commit()
            messagebox.showinfo("Password Created", "Restart The App And Log-In With Password To Use The App")
            sys.exit(0)
    
    
def log_in():
    q = "SELECT PASSWORD FROM PASSWORDTABLE"
    cur.execute(q)
    data = cur.fetchall()
    password = password_entry_log.get()
    password = password.strip()
    for i in data:
        if i[0] == password:
            dashboard()
        else:
            messagebox.showinfo("Error", "Passwords Don't Match")



## Code To Check Whether The User Has Already Created His/Her Password or Not
q = "SELECT PASSWORD FROM PASSWORDTABLE;"
cur.execute(q)
data = cur.fetchall()
# print(data)
for i in data:
    if i[0].strip() == "NULL":
        creator()
    else:
        logger()
        # dashboard()

conn.commit()
conn.close()
