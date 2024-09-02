import psycopg2  #import whenever you want to use it. it is basically use to connect database to the server site

conn = psycopg2.connect(
    dbname = 'myduka1',
    password = '1234',
    user = 'postgres',
    host = 'localhost',
    port = 5432
)
 
#define the cursor (cursor performs database operation)

curr=conn.cursor()

# #to view products

# curr.execute('select * from products') #execute is used to execute specific query
# prods = curr.fetchall() #empty to fetch everything
# print(prods)

# #create a function
# def get_products():
#     querry = 'select * from products'
#     curr.execute(querry)
#     prods = curr.fetchall()
#     return prods



# #fetch sales

# # curr.execute('select * from sales')
# # sales = curr.fetchall()
# # print(sales)

# # function to fetch sales
# # def get_sales():
# #     querry = 'select * from products'
# #     curr.execute(querry)
# #     sales = curr.fetchall()
# #     return sales
# # sales = get_sales()
# # print(sales)

# # create one function that will always fetch data from the database

# # the only difference is the querry therefore the para

def get_data(table_name):
    querry = f'select * from {table_name}'
    curr.execute(querry)
    data = curr.fetchall()
    return data
prods =  get_data('products')

#sales
def insert_sales(values):
    query = 'insert into sales (pid, quantity, created_at) values (%s, %s, now())'
    curr.execute(query, values)
    conn.commit()



sales = get_data('sales')
# print(sales)

def insert_products(values):
    querry = 'insert into products(name, buying_price, selling_price, stock_quantity) values (%s, %s, %s, %s)'
    curr.execute(querry, values)
    conn.commit()

# profit per day
def calc_profit_per_day():
    query = 'select date(created_at), sum((selling_price - buying_price )* quantity) as profit from products join sales on products.id =sales.pid group by created_at;'
    curr.execute(query)
    results = curr.fetchall()
    return results


# profit per product
def calc_profit_per_product():
    query = 'select date(created_at), sum((selling_price - buying_price )* quantity) as profit from products join sales on products.id =sales.pid group by created_at;'
    curr.execute(query)
    results = curr.fetchall()
    return results



#write a query and a function to get sales per product
#psql =>dbservice
#sales = select name, sum(selling_price*quantity) as sales from products join sales on products.productid =sales.productid group by name


def calc_sales_per_product():
    query = 'select name, sum(selling_price*quantity) as sales from products join sales on products.id =sales.pid group by name;'
    curr.execute(query)
    data = curr.fetchall()
    return data

# inserting users
def register_user(values):
    query = 'insert into users(full_name, email, password) values (%s, %s, %s)'
    curr.execute(query, values)
    conn.commit()

# function to check email
def check_email(email):
    query = 'select * from users where email =  %s'
    curr.execute(query, (email, ))
    data = curr.fetchone()
    if data:
        return data

def check_email_password(email, password):
    query = 'select * from users where email = %s and password=%s'
    curr.execute(query, (email, password,))
    data = curr.fetchall()
    return data