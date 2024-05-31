from flask import *
import sqlite3
from werkzeug.utils import secure_filename
from keras.models import load_model
app = Flask(__name__)
app.secret_key = "secret key"
model_path2 = 'model.h5'  # load .h5 Model

CTS = load_model(model_path2)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')
@app.route("/store",methods=["post"])
def store():
    username =request.form['user']
    name = request.form['user']
    email = request.form['email']
    number = request.form["mobile"]
    password = request.form['password']
    role="student"
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`,'role') VALUES (?, ?, ?, ?, ?,?)",(username,email,password,number,name,role))
    con.commit()
    con.close()
    return redirect("/")
@app.route("/login",methods=["post"])
def signin():
    mail1 = request.form['user']
    password1 = request.form['password']
    con = sqlite3.connect('signup.db')
    data=0
    data =con.execute("select `user`, `password`,role from info where `user` = ? AND `password` = ?",(mail1,password1,)).fetchall()  
    print(data)
    if mail1 == 'admin' and password1 == 'admin':
        session['username'] ="Admin"
        return redirect("myful")
    elif mail1 == str(data[0][0]) and password1 == str(data[0][1]):
        print(data)
        session['username'] =data[0][0]
        return redirect("myful")
    else:
        return render_template("signup.html")
@app.route("/myful")
def myful():
    return render_template("next.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/check",methods=["post"])
def check():
    print("working")
    v=open("X_test.txt","r").read()
    r=json.loads(v)
    y_pred=CTS.predict(r)
    y = (y_pred > 0.5)
    ye=[]
    for k in y:
        if k[0]:
            ye.append("attacked")
        else:
            ye.append("not attached")
    
    return json.dumps(ye)
if __name__ == '__main__':
    app.run(debug=True)


