import mysql.connector as sql

try:
    conn = sql.connect(host="127.0.0.1", user="root", passwd="12345678", database="passwordmanager")
    cur = conn.cursor()
except:
	pass

spc = ['@','#','$','%','&']
not_spc1 = [0,1,2,3,4,5,6,7,8,9]
not_spc2 = ['@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
not_spc3 = ['_','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

## This Function Checks and Validates The Password While Creating The Password For The App
def pass_check(password):
    password = password.replace(" ","")
    if len(password) >= 6 and len(password) <= 20:
        if password != "NULL" or password != "null":
            return True
    else:
        return False


## This Function is used by the populate_list_data() to insert all the data
def fetch_data():
	q = "SELECT * FROM UTILITIES WHERE ID != 0"
	cur.execute(q)
	data = cur.fetchall()
	return data


## This Function Is Responsible for sorting the id's of all the UTILITIES table in a sequence after every add(), update(), especially delete()
def sort_insert_id():
	row_count = 0
	replacer_count = 0 ## for mapping the elements (for l)
	to_be_replaced_count = 0 ## for mapping the elements (for l_id)
	l_id = []
	l = []
	q = "SELECT ID FROM UTILITIES;"
	cur.execute(q)
	data = cur.fetchall()
	# if len(data) != 0:
	for row in data:
		row_count += 1
	else:
		# print(row_count)
		l = [el for el in range(1,row_count+1)]
		# print(l)
	if row_count > 0:
		cur.execute("SELECT ID FROM UTILITIES")
		for i in range(row_count): 
			row = cur.fetchone()
			id_table_val = row[0]
			l_id.append(id_table_val)

		# print(l, "--->" ,l_id)

		for i in range(row_count):
			replacer = l[replacer_count]
			to_be_replaced = l_id[to_be_replaced_count]
			print(replacer, "-->" , to_be_replaced)
			q = "UPDATE UTILITIES SET ID={} WHERE ID={} ".format(replacer, to_be_replaced)
			cur.execute(q)
			conn.commit()
			replacer_count += 1	
			to_be_replaced_count += 1

		
def next_id():
	sort_insert_id()
	id = 0
	q = "SELECT max(ID) FROM UTILITIES;"
	cur.execute(q)
	data = cur.fetchone()
	val = data[0]
	if val == None:
		id = 1
	else:
		id = val+1
	print(id)
	return id

