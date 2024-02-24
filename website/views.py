# stores roots for the website
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import sqlite3

views = Blueprint("views", __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM myDatabase')
    entries = cursor.fetchall()
    cursor.close()
    return render_template("index.html", entries=entries, show=False)

@views.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        entry = (request.form.get("fullname"), request.form.get("id"), request.form.get("points"))

        if request.form.get("fullname") and request.form.get("id") and request.form.get("points"):
            connection = sqlite3.connect('myDatabase.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO myDatabase (name, employeeID, points) VALUES (?, ?, ?)", entry)
            connection.commit()
            cursor.close()
            flash("User added successfully", category="success")
            return redirect("/")

    return render_template("add.html")

@views.route('/edit', methods=['GET', 'POST'])
def edit():
    entries = []
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM myDatabase')
        entries = cursor.fetchall()
        cursor.close()
    elif request.method == 'POST':
        entry = (request.form.get("fullname"), request.form.get("e_id"), request.form.get("points"), request.form.get("id"))
        print(entry)
        cursor.execute("UPDATE myDatabase SET name=?, employeeID=?, points=? WHERE id=?", entry)
        connection.commit()
        cursor.close()
        return redirect("/")

    return render_template("edit.html", entries=entries, show=False)

@views.route('/search', methods=['GET'])
def searchEntry():
    entries = []
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()

    # stores all elements in db
    cursor.execute('SELECT * FROM myDatabase')
    entries = cursor.fetchall()
    query = request.args.get("search")

    cursor.execute("SELECT * FROM myDatabase WHERE LOWER(name) LIKE ?", ('%' + query.lower() + '%',))
    query = cursor.fetchall()
    connection.close()

    return render_template("index.html", entries=entries, results=query, show=True)


@views.route('/delete-entry', methods=['POST'])
def delEntry():
    data = request.get_json()
    ID = data.get('ID')

    if ID is not None:
        connection = sqlite3.connect('myDatabase.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM myDatabase WHERE id = ?", (ID,))
        connection.commit()
        cursor.close()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    else:
        return jsonify({'error': 'ID parameter is missing'}), 400


