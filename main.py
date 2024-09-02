from flask import Flask, render_template, request, redirect, url_for, flash, session
from dbservice import get_data, insert_products, insert_sales, calc_sales_per_product, calc_profit_per_product, check_email, calc_profit_per_day, register_user, check_email_password

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'alfa'
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

#home
@app.route('/home')
def home():
    return render_template('home.html')

#products
@app.route('/products')
def products():
    prods = get_data('products')
    return render_template ('products.html', product=prods)

@app.route('/add products', methods = ['POST', 'GET'])
def add_products():
    #check method
    if request.method == 'POST':
        #request data
       
        pname=request.form['product_name']
        bprice=request.form['buying_price']
        sprice = request.form['selling_price']
        squantity = request.form['stock_quantity']

    #insert products to the database
        new_prod = (pname, bprice, sprice, squantity)
        insert_products(new_prod)
        return redirect(url_for('products'))

# https methods
# techniques used to send, fetch, update, delete data from the browser
# post => send
# get => fetch
# put => update
# delete



#sales
@app.route('/sales')
def sales():
    sale = get_data('sales')
    products=get_data('products') 
    return render_template('sales.html', sell=sale, products=products)

# adding sales from the front-end
@app.route('/make sales', methods = ['POST', 'GET'])
def add_sales():
    #check method
    if request.method == 'POST':
        #request data
      
        pid=request.form['pid']
        quantity=request.form['quantity']       
        

    #insert products to the database
        new_sale = (pid, quantity)
        insert_sales(new_sale)
    return redirect(url_for('sales'))


#dashboard
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    per_product = calc_sales_per_product()
    profits = calc_profit_per_product()
   
    profit = []
    for i in profits:        
        profit.append(float(i[1]))  

    names = []
    sales = []
    for i in per_product:
        names.append(i[0])
        sales.append(float(i[1]))

    #  line chart
    profit_per_day = calc_profit_per_day()
    pro_per_day = [] 
    dates = []
    for i in profit_per_day:
        
        pro_per_day.append(float(i[1]))
        dates.append(str(i[0]))

    
        


    return render_template('dashboard.html', names=names, sales=sales, profit=profit, dates=dates, pro_per_day=pro_per_day)



# register user
@app.route('/register', methods = ['POST', 'GET'])
def register():
    #check method (query to check email existence)
    if request.method == 'POST':
        #request data
       
        fname=request.form['full_name']
        email=request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # before inserting user check if the user exists

        x = check_email(email) 
        if x==None: 
            new_user = (fname, email, hashed_password)
            register_user(new_user)
            return redirect(url_for('login'))
        else:
            flash('Email already exists')
            return redirect(url_for('login'))   
    return render_template('register.html')

# flash messages
# login.html
# route to login user
# compare email and password 
# checking details if they are the same to those  passed when registering
    
#login route
@app.route('/login', methods =['POST','GET'])
def login():
    if request.method=='POST':
        # get data form
        email = request.form['email']
        password = request.form['password']
        c_email=check_email(email)
        if c_email==None:
            flash('Email does not exist')
            return redirect(url_for('register'))
        else:
            # check password
            if bcrypt.check_password_hash(c_email[-1], password):
                flash('login successful')
                session['email']=email
                return redirect(url_for('dashboard'))          
            else:
                flash('Email or password is incorrect')
                
    return render_template('login.html')

# logout route
@app.route('/logout')
def logout():
   session.pop('email', None)
   return redirect(url_for('login'))
  

app.run(debug=True)

#create html files for each route
#products.html
# sales.html
# dashboard.html
# https://youtu.be/mqhxxeeTbu0?si=cJhiVcGFT1pXAkAM

#database to server side pycopg2
#serverside to html jinja flask

#jinja is used to pass python variables and operations to html (front-end)
#when passing variables we use {{}} inside an element 
#when passing operations we use {% if 2>1%} {% endif %} if its a while loop} endfor if its a for loop

# sales per day and profit per day we use line graph

# querry to check email existence
# select * from users where email =  'ojijoalphonce@gmail.com';

# write a query thats going to fetch the user with an email and password. => select * from users where email = %s and password=%s

# https://flask.palletsprojects.com/en/3.0.x/quickstart/

# password hashing
# import Bcrypt
# from flask_bcrypt(app) import Bcrypt
# create a Bcrypt objectbcrypt = Bcrypt(app)
# hash the check_email_password
# hashed password = bcrypt.generate_password_hash(password)