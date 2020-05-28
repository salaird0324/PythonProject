#import mysql connector and pygal
import mysql.connector
import pymongo
import pygal
import json

##################### SETUP  DATABASE CONNECTIONS ###############

#connect to your mysql datbase
mydb = mysql.connector.connect(
  host="localhost",
  user="spencer",
  passwd="324S@l1998",
  database="classicmodels"
)

#connect to the mongo database
mongo_client = pymongo.MongoClient(host = "mongodb://localhost:27017/",
serverSelectionTimeoutMS = 3000,
username="spencer",
password='324S@l1998')

#Select mongo datacbase and collections
mongo_db = mongo_client["finalproject"]
employee_collection = mongo_db["employees"]
product_collection = mongo_db["products"]
customer_collection = mongo_db["customers"]
orders_collection = mongo_db["orders"]

#The cursor will execute queries on your MySql Datbase
mycursor = mydb.cursor()

################# QUERIES TO POPULATE EMPLOYEE COLLECTION  ####################

#sql query generates a list of managers. People who have other employees report to them
sql_query = '''select employeeNumber, firstName, lastName
from employees
where employeeNumber IN (select reportsTo from employees);'''

#Execute the query
mycursor.execute(sql_query)

#Get the query result
query_result = mycursor.fetchall()

#Create managers dictionary
managers = {}

'''query_result is a list of tuples. The loop below converts the list of tuples into
a dictionary where the dictionary key is the employeeNumber and the value is the 
first and last name'''
for result in query_result:
    managers[result[0]] = result[1] + " " + result[2]

#Select all data from the employees and offices tables
sql_query = '''SELECT *
FROM employees e, offices o
WHERE e.officeCode = o.officeCode;'''

#Execute the query
mycursor.execute(sql_query)

#Get the query results
query_result = mycursor.fetchall()

#################### WRITE DOCUMENTS TO INSERT INTO EMPLOYEE COLLECTIONS ################

#list to store employee documents
employees = []
#loop through tuples in query_result. Write data to json format to store in our json file
for record in query_result:
    office_document = {
    "officeCode": record[8],
    "city": record[9],
    "phone": record[10],
    "addressLine1": record[11],
    "addressLine2": record[12],
    "state": record[13],
    "country" : record[14],
    "postalCode": record[15],
    "territory": record[16]
    }
    
    '''for employees who don't report to anyone, set the reportsTo value to N/A
    for other employees with a manager get the manager name from the managers dictionary
    using the the employeeNumber as the dictionary key'''
    if record[6] == None:
        manager = "N/A"
    else:
        manager = managers[int(record[6])]

    employee_document = {
    "_id": record[0],
    "lastName": record[1],
    "firstName": record[2],
    "extension": record[3],
    "email": record[4],
    "reportsTo": manager,
    "jobTitle": record[7],
    "office": office_document
    }
    employees.append(employee_document)

#insert employee documents into the employees collection in the mongo database
employee_collection.drop()
employee_collection.insert_many(employees)

#write to mongo formated data to a json file
json_file = open("employees.json", "w") #open the file
json_file.write("[\n") #write the opening bracket forthe list
counter = 1 #use counter to determine id the last document is being written

#loop through the list of employee documents
for employee_doc in employees:
    json_file.write(json.dumps(employee_doc)) #convert a python dictionary to a json object
    #write a comma after the document if it is not the last in the list
    if counter != len(employees):
        json_file.write(",\n")
        counter += 1
    else: #don't write a comma after the document if it is the last in the list
        json_file.write("\n")

json_file.write("]\n")
json_file.close()

print("\nScript executed successfully for employees")
###GET customer table
sql_query = '''SELECT * FROM customers;'''
mycursor.execute(sql_query)
query_result = mycursor.fetchall()

customers = []

for record in query_result:
	payments = []
	payments_query = '''SELECT * FROM payments WHERE customerNumber =''' + str(record[0]) + ";"
	mycursor.execute(payments_query)
	payments_result = mycursor.fetchall()

	for payment in payments_result: 
		
		payments_document = {
		"checkNumber": payment[1],
		"paymentDate": payment[2].strftime("%b %d %Y"),
		"amount": float(payment[3])
		}
		payments.append(payments_document)
	
	customer_document = {
	"_id": record[0],
	"customerName": record[1],
	"contactLastName": record[2],
	"contactFirstName": record[3],
	"phone": record[4],
	"addressLine1": record[5],
	"addressLine2": record[6],
	"city": record[7],
	"state": record[8],
	"postalCode": record[9],
	"country": record[10],
	"salesRepEmployeeNumber": record[11],
	"creditLimit": float(record[12]),
	"payments": payments
	}
	customers.append(customer_document)


customer_collection.drop()
customer_collection.insert_many(customers)

json_file = open("customers.json", "w")
json_file.write("[\n")
counter = 1

for customer_doc in customers:
	json_file.write(json.dumps(customer_doc))
	if counter != len(customers):
		json_file.write(",\n")
		counter += 1
	else:
		json_file.write("\n")

json_file.write("]\n")
json_file.close()

print("Query completed successfully for customers")
###GET PRODUCTS TABLE

sql_query = '''SELECT * FROM products p, productlines l WHERE p.productLine = l.productLine;'''

mycursor.execute(sql_query)

query_result = mycursor.fetchall()

products = []

for record in query_result:

	product_document = {
	"_id": record[0],
	"productName": record[1],
	"productScale": record[3],
	"productVendor": record[4],
	"productDescription": record[5],
	"quantityInStock": record[6],
	"buyPrice": float(record[7]),
	"MSRP": float(record[8]),
	"productLine": [{
		"line": record[9],
		"textDescription": record[10],
		"htmlDescription": record[11],
		"image": record[12]
	}]
	}
	products.append(product_document)


product_collection.drop()
product_collection.insert_many(products)

json_file = open("products.json", "w")
json_file.write("[\n")
counter = 1

for product_doc in products:
	json_file.write(json.dumps(product_doc))

	if counter != len(products):
		json_file.write(",\n")
		counter += 1
	else:
		json_file.write("\n")

json_file.write("]\n")
json_file.close()

print("Script executed successfully for products")

### ORDERS COLLECTION

sql_query = '''select * from orders;'''

mycursor.execute(sql_query)

query_result = mycursor.fetchall()

orders = []

x = 0
for record in query_result:
	orderDetails = []
	real_employee_name = ""
	customerName_query = '''select * from customers where customerNumber = ''' + str(record[6]) + ";"
	mycursor.execute(customerName_query)
	customerName_result = mycursor.fetchall()
	for name in customerName_result:
		customerName = name[1]
		employeeNumber = name[0]

		employeeName_query = '''select firstName, lastName from employees e, customers c where e.employeeNumber =''' + str(name[11]) + ";"
		mycursor.execute(employeeName_query)
		employeeName_result = mycursor.fetchall()
		for plz in employeeName_result:
			real_employee_name = plz[0] + " " + plz[1]

	orderDetails_query = '''select * from orderdetails where orderNumber = ''' + str(record[0]) + ";"
	mycursor.execute(orderDetails_query)
	orderDetails_result = mycursor.fetchall()
	for order in orderDetails_result:
#		print(order)
#		print(order[1])
#		productName_query = '''select productName from products where productCode =''' + str(order[1]) + ";"
#		mycursor.execute(productName_query)
#		productName_result = mycursor.fetchall()
#		for productName in productName_result:
#			product_name = productName[1]
		orderDetails_doc = {
		"productName": order[1],
		"quantityOrdered": order[2],
		"priceEach": float(order[3])
		}
		orderDetails.append(orderDetails_doc)

	if record[3] == None:
		order1_doc = {
		"_id": record[0],
		"orderDate": record[1].strftime("%b %d %Y"),
		"requiredDate": record[2].strftime("%b %d %Y"),
		"status": record[4],
		"comments": record[5],
		"customerName": real_employee_name,
		"orderDetails": orderDetails
		}
		orders.append(order1_doc)
	else:
		order_document = {
		"_id": record[0],
		"orderDate": record[1].strftime("%b %d %Y"),
		"requiredDate": record[2].strftime("%b %d %Y"),
		"shippedDate": record[3].strftime("%b $d %Y"),
		"status": record[4],
		"comments": record[5],
		"customerName": customerName,
		"employeeName": real_employee_name,
		"orderDetails":  orderDetails
		}

		orders.append(order_document)
orders_collection.drop()
orders_collection.insert_many(products)

json_file = open("orders.json", "w")
json_file.write("[\n")
counter = 1

for order_doc in orders:
    json_file.write(json.dumps(order_doc))

    if counter != len(orders):
        json_file.write(",\n")
        counter += 1
    else:
        json_file.write("\n")

json_file.write("]\n")
json_file.close()

print("Script executed successfully for orders")

