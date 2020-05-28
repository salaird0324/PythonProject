
import mysql.connector
import pygal

#connect to your datbase
mydb = mysql.connector.connect(
  host="localhost",
  user="spencer",
  passwd="324S@l1998",
  database="classicmodels"
)

#The cursor will execute  queries on your MySql Datbase
mycursor = mydb.cursor()

#Create sql query. The backslash \  is a line continuation character and will allow the query to execute as one string
sql_query = '''SELECT e.firstName, e.lastName, COUNT(c.salesRepEmployeeNumber) AS "NumCustomers"
 FROM employees e, customers c
 WHERE e.employeeNumber = c.salesRepEmployeeNumber
 GROUP BY c.salesRepEmployeeNumber
 ORDER BY COUNT(c.salesRepEmployeeNumber) DESC;'''

#Execute the query
mycursor.execute(sql_query)

#Get the query result
query_result = mycursor.fetchall()
#Each record will be returned in the form of a tuple so we will need to access each tuple item
employee_names = []
number_of_customers = []

for record in query_result:
    employee_names.append(record[0] + " " + record[1]) #The first 2 items in the tuple are first and last names
    number_of_customers.append(record[2]) #the third item is the number of customers

#Export the data in a chart to an SVG file
bar_chart = pygal.Bar(x_label_rotation=45)
bar_chart.title = "Customers per Employee"
bar_chart.x_labels = map(str, employee_names) #set x axis labels to the employee names
bar_chart.add('Number of Customers', number_of_customers) # add number of customers
bar_chart.render_to_file('images/q1.svg') #render the chart to an SVG file

#If program is successful print this
print("Program executed successfully")

### Write your queries and create your charts below

### 2

sql_query2 = ''' select p.productName, COUNT(o.orderNumber) FROM products p, orderdetails o WHERE p.productCode = o.productCode GROUP BY o.productCode ORDER BY COUNT(o.orderNumber) DESC LIMIT 10;'''

mycursor.execute(sql_query2)

query_result = mycursor.fetchall()

product_names = []
num_of_orders = []

for record in query_result:
    product_names.append(record[0])
    num_of_orders.append(record[1])

bar_chart2 = pygal.Bar(x_label_rotation=45)
bar_chart2.title = "2"
bar_chart2.x_labels = map(str, product_names)
bar_chart2.add('Number of Orders', num_of_orders)
bar_chart2.render_to_file("images/q2.svg")

print("Query 2 finished successfully")
sql_query3 = '''select p.productName, o.priceEach FROM products p, orderdetails o WHERE p.productCode = o.productCode GROUP BY p.productName, o.priceEach ORDER BY o.priceEach DESC LIMIT 10;'''

mycursor.execute(sql_query3)

query_result = mycursor.fetchall()

product_names = []
highest_prices = []

for record in query_result:
    product_names.append(record[0])
    highest_prices.append(record[1])

bar_chart3 = pygal.Bar(x_label_rotation=45)
bar_chart3.title = "3"
bar_chart3.x_labels = map(str, product_names)
bar_chart3.add("Price per Order", highest_prices)
bar_chart3.render_to_file("images/q3.svg")                                                                                                                                                                 
print("Query 3 finished successfully")


### 4
sql_query4 = '''select orderNumber, priceEach from orderdetails GROUP BY orderNumber, priceEach ORDER BY priceEach DESC LIMIT 10;'''
mycursor.execute(sql_query4)

query_result4 = mycursor.fetchall()

order_numbers = []
price_each = []

for record in query_result4:
    order_numbers.append(record[0])
    price_each.append(record[1])

bar_chart4 = pygal.Bar(x_label_rotation = 45)
bar_chart4.title = "4"
bar_chart4.x_labels = map(str, order_numbers)
bar_chart4.add("Price per Order", price_each)
bar_chart4.render_to_file("images/q4.svg")

print("Query 4 finished successfully")


### 5
sql_query5 = '''select c.customerName, COUNT(o.orderNumber) FROM customers c, orders o WHERE c.customerNumber = o.customerNumber GROUP BY c.customerName ORDER BY COUNT(o.orderNumber) DESC LIMIT 10;'''
mycursor.execute(sql_query5)
query_result = mycursor.fetchall()

customer_names = []
total_orders = []

for record in query_result:
    customer_names.append(record[0])
    total_orders.append(record[1])

bar_chart5 = pygal.HorizontalBar()
bar_chart5.title = "5"
bar_chart5.x_labels = map(str, customer_names)
bar_chart5.add("total Orders", total_orders)
bar_chart5.render_to_file("images/q5.svg")

print("Query 5 finished successfully")
### 6
sql_query6 = '''select SUM(amount) as totalAmount, YEAR(paymentDate) from payments GROUP BY YEAR(paymentDate) ORDER BY YEAR(paymentDate) DESC;'''

mycursor.execute(sql_query6)

query_result = mycursor.fetchall()

total_payments = []
years= []

for record in query_result:
    total_payments.append(record[0])
    years.append(record[1])

pie_chart6 = pygal.Pie()
pie_chart6.title = "6"
pie_chart6.add("2005", total_payments[0])
pie_chart6.add("2004", total_payments[1])
pie_chart6.add("2003", total_payments[2])
pie_chart6.render_to_file("images/q6.svg")
print("Query 6 finished successfully")

### 7

sql_query7 = '''select SUM(amount) as totalAmount, MONTH(paymentDate) from payments WHERE YEAR(paymentDate) = 2004 GROUP BY MONTH(paymentDate) ORDER BY MONTH(paymentDate) ASC;'''
mycursor.execute(sql_query7)
query_result = mycursor.fetchall()

total_payments = []
months = []

for record in query_result:
    total_payments.append(record[0])
    months.append(record[1])

bar_graph7 = pygal.Bar()
bar_graph7.title = "7"
bar_graph7.x_labels = map(int, months)
bar_graph7.add("Payments per Month", total_payments)
bar_graph7.render_to_file("images/q7.svg")

print("Query 7 executed successfully")
sql_query8 = '''select count(customerNumber), DAY(paymentDate) from payments WHERE MONTH(paymentDate) = 12 AND YEAR(paymentDate) = 2004 GROUP BY DAY(paymentDate) ORDER BY DAY(paymentDate) ASC;'''

mycursor.execute(sql_query8)

query_result = mycursor.fetchall()

payments = []
days = []

for record in query_result:
    payments.append(record[0])
    days.append(record[1])

line_chart8 = pygal.Line()
line_chart8.title = "8"
line_chart8.x_labels = map(int, days)
line_chart8.add("Payments per Day", payments)
line_chart8.render_to_file("images/q8.svg")

print("Query 8 finished successfully")

### 9
sql_query9 = '''select c.customerName, COUNT(p.customerNumber) from customers c, payments p WHERE c.customerNumber = p.customerNumber GROUP BY p.customerNumber ORDER BY COUNT(p.customerNumber) DESC LIMIT 10;'''

mycursor.execute(sql_query9)

query_result = mycursor.fetchall()
customers = []
payments = []

for record in query_result:
    customers.append(record[0])
    payments.append(record[1])

bar_graph9 = pygal.Bar()
bar_graph9.title = "9"
bar_graph9.x_labels = map(str, customers)
bar_graph9.add("Payments", payments)
bar_graph9.render_to_file("images/q9.svg")

print("Query 9 finished successfully")

sql_query10 = '''select COUNT(customerName) as customerNames, state from customers GROUP BY state ORDER BY state;'''

mycursor.execute(sql_query10)
query_result = mycursor.fetchall()

customers = []
states = []

for record in query_result:
    customers.append(record[0])
    states.append(record[1])

pie_chart10 = pygal.Pie()
pie_chart10.title = "10"
pie_chart10.add("BC", customers[1])
pie_chart10.add("CA", customers[2])
pie_chart10.add("Co. Cork", customers[3])
pie_chart10.add("CT", customers[4])
pie_chart10.add("Isle of Wight", customers[5])
pie_chart10.add("MA", customers[6])
pie_chart10.add("NH", customers[7])
pie_chart10.add("NJ", customers[8])
pie_chart10.add("NSW", customers[9])
pie_chart10.add("NV", customers[10])
pie_chart10.add("NY", customers[11])
pie_chart10.add("Osaka", customers[12])
pie_chart10.add("PA", customers[13])
pie_chart10.add("Pretoria", customers[14])
pie_chart10.add("Quebec", customers[15])
pie_chart10.add("Queensland", customers[16])
pie_chart10.add("Tokyo", customers[17])
pie_chart10.add("Victoria", customers[18])
pie_chart10.render_to_file("images/q10.svg")

print("Query 10 finished successfully")

### 11

sql_query11 = '''select reportsTo, COUNT(reportsTO) as valueOccurance from employees GROUP BY reportsTo ORDER BY valueOccurance DESC LIMIT 6;'''

mycursor.execute(sql_query11)

query_result = mycursor.fetchall()

employees = []
manages = []
for record in query_result:
	employees.append(record[0])
	manages.append(record[1])
bar_graph11 = pygal.Bar()
bar_graph11.title = "11"
bar_graph11.x_labels = map(int, employees)
bar_graph11.add("Number of Employees Managed", manages)
bar_graph11.render_to_file("images/q11.svg")

print("Query 11 finished successfully")

### 12
sql_query12 = '''select e.firstName, e.lastName, COUNT(o.orderNumber) from employees e, customers c, orders o WHERE c.salesRepEmployeeNumber = e.employeeNumber GROUP BY e.firstName, e.lastName ORDER BY COUNT(o.orderNumber) DESC;'''
mycursor.execute(sql_query12)
query_result = mycursor.fetchall()

employees = []
orders = []

for record in query_result:
	employees.append(record[0] + " " + record[1])
	orders.append(record[2])

pie_chart12 = pygal.Pie()
pie_chart12.title ="12"
for x, y in zip(employees, orders):
    pie_chart12.add(x, y)
pie_chart12.render_to_file("images/q12.svg")

print("Query 12 finished successfully")

### 13

query_13 = '''select c.country, count(p.customerNumber) from customers c, payments p where c.customerNumber = p.customerNumber group by c.country;'''
mycursor.execute(query_13)
query_result = mycursor.fetchall()

countries = []
payments = []
for record in query_result:
    countries.append(record[0])
    payments.append(record[1])
bar_graph13 = pygal.Bar()
bar_graph13.title = "13"
bar_graph13.x_labels = map(str, employees)
bar_graph13.add("Number of payments per country", payments)
bar_graph13.render_to_file("images/q13.svg")

print("query 13 completed successfully")
### 14

query_14 = '''select e.firstName, e.lastName, SUM(od.priceEach) from employees e, customers c, orders o, orderdetails od WHERE e.employeeNumber = c.salesRepEmployeeNumber AND c.customerNumber = o.customerNumber AND o.orderNumber = od.orderNumber GROUP BY e.firstName, e.lastName;'''
mycursor.execute(query_14)
query_result = mycursor.fetchall()

names = []
totalPrice = []

for result in query_result:
	names.append(result[0] + " " + result[1])
	totalPrice.append(result[2])

bar_graph14 = pygal.Bar()
bar_graph14.title = "14"
bar_graph14.x_labels = map(str, names)
bar_graph14.add("Total Price of orders per Employee", totalPrice)
bar_graph14.render_to_file("images/q14.svg")

print("query 14 completed successfully")













