"""
auth: AJ Boyd
date: 2/14/24
desc: sample CRUD app using the Flask framework
file: app.py
"""
from flask import Flask
import sqlite3

connection = sqlite3.connect("myDatabase.db")
cursor = connection.cursor()

# Check if the employees table already exists and is not empty
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='myDatabase'")
table_exists = cursor.fetchone()

if not table_exists:
    # define schema for DB table
    schema = '''
        CREATE TABLE IF NOT EXISTS myDatabase (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            employeeID INTEGER NOT NULL,
            points INTEGER NOT NULL
            )
    '''
    cursor.execute(schema)

    # create starting sample data
    sampleData = [
        ("Steve Smith", 211, 80),
        ("Jian Wong", 122, 92),
        ("Chris Peterson", 213, 91),
        ("Sai Patel", 524, 94),
        ("Andrew Whitehead", 425, 99),
        ("Lynn Roberts", 626, 90),
        ("Robert Sanders", 287, 75)
    ]

    cursor.executemany("INSERT INTO myDatabase (name, employeeID, points) VALUES (?, ?, ?)", sampleData)
    connection.commit()
connection.close()

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "asdf asdfasdfasfasdfasdfasdgdfh"
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # db.init_app(app)

    from .views import views

    # reg blueprint
    app.register_blueprint(views, url_prefix='/')
    return app
