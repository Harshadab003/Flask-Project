from flask import Flask,render_template,redirect,request,session
from werkzeug.utils import secure_filename
import mysql.connector

app = Flask(__name__)
app.secret_key = "Firstbit"

@app.route("/AdminLogin",methods=["GET","POST"])
def AdminLogin():
    if(request.method == "GET"):
        return render_template("AdminLogin.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
        cursor = mydb.cursor()
        sql = "select count(*) from userinfo where username=%s and password=%s and role='Admin';"
        val = (uname,pwd)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        if(int(record[0]) == 1):
            session["uname"] = uname
            return  redirect("/AdminHome")
        else:
            return redirect("/AdminLogin")

@app.route("/AdminHome")
def AdminHome():
    if("uname" in session):
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="harshada",
                database = "flask"
                )
        cursor = mydb.cursor()
        sql = "select * from burger"
        cursor.execute(sql)
        records = cursor.fetchall() #This is fetch all records.
        return render_template ("AdminHome.html",burgers=records)
    else:
        return redirect("/AdminLogin")

@app.route("/Remove/<id>")
def Remove(id):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    sql = "delete from burger where bid=%s"
    val = (id,)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect ("/AdminHome")

@app.route("/edit/<id>",methods=["GET","POST"])
def edit(id):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    
    if(request.method=="GET"):
        sql = "select * from burger where bid=%s"
        val = (id,)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        return render_template("Edit.html",burger=record)
    else:
        bname = request.form["bname"]
        price = request.form["price"]
        image = request.form["image"]
        qty = request.form["qty"]
        sql = ''' Update burger set burger_name=%s,
                price=%s,image_url=%s,qty=%s
                where bid=%s;'''
        val = (bname,price,image,qty,id)
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/AdminHome")

@app.route("/addRecord",methods = ["GET","POST"])
def AddRecord():
    if("uname" not in session):
        return redirect("/AdminLogin")
    
    else:
        if(request.method == "GET"):
            return render_template("AddRecord.html")
        else:
            bname = request.form["bname"]
            price = request.form["price"]
            qty = request.form["qty"]
            f = request.files['image']
            #file will get uploaded to the server
            f.save("static\\images\\"+secure_filename(f.filename))
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="harshada",
                database = "flask"
                )
            cursor = mydb.cursor()
            sql = '''insert into burger (burger_name,price,qty,image_url)
                    value (%s,%s,%s,%s)'''
            val = (bname,price,qty,f.filename)
            cursor.execute(sql,val)
            mydb.commit()
            mydb.close()
            return redirect("/AdminHome")

def showAllBurgers():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    sql = "select * from burger"
    cursor.execute(sql)
    records = cursor.fetchall() #This is fetch all records.
    return render_template ("showAllBurgers.html",burgers=records)

def ViewDetails(id):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    sql = "select * from burger where bid=%s"
    val = (id,)
    cursor.execute(sql,val)
    burger = cursor.fetchone()

    return render_template("ViewDetails.html",burger= burger)

def SignUp():
    if(request.method == "GET"):
        return render_template("SignUp.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        email = request.form["email"]
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )   
    cursor = mydb.cursor()
    sql = "insert into userinfo values (%s,%s,%s,'User');"
    val = (uname,pwd,email)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect("/Login")

def SignOut():
    session.clear()
    return redirect("/")

def Login():
    if (request.method == "GET"):
        return render_template("Login.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    sql = "select count(*) from userinfo where username=%s and password=%s;"
    val = (uname,pwd)
    cursor.execute(sql,val)
    record = cursor.fetchone()
    if(int(record[0]) == 1):
        session["uname"] = uname
        return  redirect("/")
    else:
        return redirect("/Login")
    
def addToCart():
    if("uname" not in session):
        return redirect("/Login")
    else:
        #addtocart
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
        cursor = mydb.cursor()
        uname = session["uname"]
        bid = request.form["bid"]
        qty = request.form["qty"] 
        sql = "select count(*) from Mycart where username=%s and bid=%s"
        val = (uname,bid)
        cursor.execute(sql,val)
        result = cursor.fetchone()
        if (result[0] == 0):   
            sql = "insert into Mycart(bid,qty,username) values(%s,%s,%s)"
            val = (bid,qty,uname)
            cursor.execute(sql,val)
            mydb.commit()
            mydb.close()
            return redirect ("/showAllCartItems")
        else:
            return "Item already present in a cart..."
         
def showAllCartItems():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    sql = '''select b.bid, b.burger_name,b.price,
            b.image_url,m.qty from burger b 
            inner join mycart m on b.bid = m.bid 
            and m.username = %s'''
    val = (session["uname"],)
    cursor.execute(sql,val)
    records = cursor.fetchall()
    sql = "select sum(price*qty) from cartitems_vw where username=%s;"
    val = (session["uname"],)
    cursor.execute(sql,val)
    sum = cursor.fetchone()[0]
    session["total"] = sum
    return render_template("showAllCartItems.html",burgers = records)

def RemoveItem(id):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    sql = "delete from mycart where username =  %s and bid = %s;"
    val = (session["uname"],id)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect("/showAllCartItems")

def UpdateItem():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshada",
            database = "flask"
            )
    cursor = mydb.cursor()
    uname = session["uname"]
    bid = request.form["bid"]
    qty = request.form["qty"]
    sql = "update mycart set qty=%s where bid=%s and username=%s"
    val = (qty,bid,uname)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect("/showAllCartItems")

def MakePayment():
    if(request.method == "GET"):
        return render_template("MakePayment.html")
    else:
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form ["expiry"]
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="harshada",
                database = "flask"
                )
        cursor = mydb.cursor()
        sql = '''select count(*) from carddetails 
                where cardno=%s and
                cvv=%s and
                expiry = %s'''
        val = (cardno,cvv,expiry)
        cursor.execute(sql,val)
        record = cursor.fetchone() #This is fetch all records    
        if(int(record[0]) == 1):
            amount = session["total"]
            sql1 = "update carddetails set amount = amount - %s where cardno=%s"
            sql2 = "update carddetails set amount = amount + %s where cardno=222"
            val1 = (amount,cardno)
            val2 = (amount,)
            cursor.execute(sql1,val1)
            cursor.execute(sql2,val2)
            mydb.commit()
            return redirect("/")

app.add_url_rule("/",'',showAllBurgers)
app.add_url_rule("/ViewDetails/<id>",'abc',ViewDetails)
app.add_url_rule("/SignUp",'signup',SignUp,methods = ["GET","POST"])
app.add_url_rule("/Login",'login',Login,methods = ["GET","POST"])
app.add_url_rule("/SignOut",'signout',SignOut)
app.add_url_rule("/addToCart",'addToCart',addToCart,methods = ["GET","POST"])
app.add_url_rule("/showAllCartItems",'showAllCartItems',showAllCartItems,methods = ["GET","POST"])
app.add_url_rule("/RemoveItem/<id>",'RemoveItem',RemoveItem)
app.add_url_rule("/UpdateItem",'UpdateItem',UpdateItem,methods = ["GET","POST"])
app.add_url_rule("/MakePayment",'MakePayment',MakePayment,methods = ["GET","POST"])

if(__name__=="__main__"):
    app.run(debug=True)