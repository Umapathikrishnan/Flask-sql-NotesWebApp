from flask import Flask, render_template, request
from flask_mysqldb import MySQL  # to use db
import MySQLdb.cursors
from decouple import config

#API_USERNAME = config('USER')
#API_KEY = config('KEY')
app = Flask(__name__)
app.config['MYSQL_HOST'] = "remotemysql.com"  # remote.mysql
# if remotemysql give user 📛 *see credentials while creating db
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config(
    'MYSQL_PASSWORD')  # if remotemysql give password🙇
app.config['MYSQL_DB'] = config('MYSQL_DB')  # db name

mysql = MySQL(app)


@app.route('/')
def welcome():
    return render_template("notes.html")


@app.route('/addnote', methods=["POST"])
def addnote():
    if request.method == 'POST':
        category = request.form["category"]
        task = request.form['task']
        # a = [name, email, mobile, stream, address]
        # to connect to db
        cursor = mysql.connection.cursor()
        print("connected to remotemysql")
        cursor.execute('INSERT INTO note VALUES(NULL,%s,%s)', (category, task))
        mysql.connection.commit()
        msg = "note added sucessfully"
    return render_template("notes.html", category=category, task=task, msg=msg)


@app.route('/display')
def display():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM note')
    mysql.connection.commit()
    mynotes = cursor.fetchall()
    # for i in mynotes:
    #   print(i[1])
    #  print(i[2])
    return render_template('notes.html', mynotes=mynotes)
# SELECT * FROM `note` WHERE category = "coding"
# DELETE FROM MySQL_table WHERE id=10;


@app.route('/deletebycategory', methods=["POST"])
def delete_by_category():
    if request.method == "POST":
        category1 = ""
        category1 = request.form["del_category"]
        print(category1)
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM note WHERE category = %s",  (category1,))
        mysql.connection.commit()
        msg = "deleted succesfully"
        print(msg)
    return render_template("notes.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)  # debug true will automatically re run the server 😇
