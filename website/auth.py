from flask import Blueprint, request, flash, redirect, url_for
import flask
from flask.templating import render_template
from .models import Product
from datetime import date
import sqlite3
mydb = sqlite3.connect("website.db",check_same_thread=False)


login_flag = False
user_email = None

auth = Blueprint('auth',__name__)
@auth.route('/',methods=['GET','POST'])

def home():
    if request.method == "POST":

        if request.form.get("store")=="store":
            
            return redirect(url_for('auth.store'))
            
        elif request.form.get("order")=="order":
            if login_flag == True:
                return redirect(url_for('auth.orders'))
            else:
                flash("login into your account", category="error")
            

    return render_template("home.html", user = user_email)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        my_cursor = mydb.cursor()
        query = "select password,name from user where email = ? ;"
        my_cursor.execute(query, (email,))
        z=my_cursor.fetchall()
        if len(z)>0:
            x = z[0]
            username = x[1]
            print("printing")
            print(x)
            if x[0] == password:
                global login_flag
                login_flag = True
                global user_email
                user_email = email
                return redirect(url_for('auth.home'))
            elif len(email) < 4:
                flash("Email is incorrect", category='error')
            elif len(password) < 7:
                flash("Password is incorrect", category='error')
            else:
                flash("Email or password incorrect", category='error')
        else:
            flash("Email id not registered", category= 'error')
        my_cursor.close()
    return render_template("login.html", user=user_email)

@auth.route('/logout')
def logout():
    global login_flag
    login_flag= False
    global user_email
    user_email= None
    return redirect(url_for('auth.login'))

@auth.route('/sigh-up', methods=['GET', 'POST'])
def sigh_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email)<4:
            flash('Email should be greater than 4 characters', category='error')
        elif len(first_name)<2:
            flash('First name should be greater than 2 characters', category='error')
        elif len(password1)<7:
            flash('Password should be greater than 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            my_cursor = mydb.cursor()
            query = "INSERT INTO user (name,email,password) values (?,?,?);"
            val = (first_name, email, password1)
            my_cursor.execute(query, val)
            print(my_cursor)
            mydb.commit()
            my_cursor.close()
            global login_flag
            login_flag= True
            global user_email
            user_email = email
            return redirect(url_for('auth.home'))
    return render_template("sighup.html", user = user_email)

@auth.route('/store', methods=['GET','POST'])
def store():
    
    # item = Product()

    my_cursor = mydb.cursor()
    my_cursor.execute("select * from storages;")
    x = my_cursor.fetchall()

    my_cursor.execute("select name from user where email = ?;", (user_email,))
    y=my_cursor.fetchone()
    
    if request.method == "POST":
        item = request.form.get("buy")
        
        if login_flag==True:
            
            my_cursor.execute("INSERT INTO orders(user_email,product_id,purchase_date) values (?,?,?);",(user_email,item,date.today()))
            mydb.commit()
            my_cursor.close()
            return redirect(url_for('auth.orders'))
            
        else:
            return redirect(url_for('auth.login'))
    return render_template('store.html', lists = x, user = y)
    

@auth.route('/orders', methods=['GET','POST'])
def orders():
    my_cursor=mydb.cursor()
    my_cursor.execute("select storages.id,storages.product,storages.brand,storages.rating,storages.model,storages.picture,storages.price,storages.details,orders.purchase_date from storages inner join orders on orders.product_id = storages.id and orders.user_email= ?;",(user_email,))
    x = my_cursor.fetchall()
    if request.method == "POST":
        productid = request.form.get("delete")
        my_cursor.execute("delete from orders where product_id=?;",(productid,))
        mydb.commit()
        my_cursor.execute("select storages.id,storages.product,storages.brand,storages.rating,storages.model,storages.picture,storages.price,storages.details,orders.purchase_date from storages inner join orders on orders.product_id = storages.id and orders.user_email= ?;",(user_email,))
        x = my_cursor.fetchall()
        my_cursor.close()
        return render_template('orders.html', item = x)
    return render_template('orders.html', item = x)

