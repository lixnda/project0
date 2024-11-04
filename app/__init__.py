from flask import Flask             
from flask import render_template, session 
from flask import request, redirect   
import sqlite3, csv

app = Flask(__name__)

DB_FILE = "blog.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

# add other functions and db if needed

"""
#commands for database:
result = c.execute("CREATE TABLE logins(user TEXT, password TEXT, id INTEGER PRIMARY KEY)")
result = c.execute("CREATE TABLE profile(id INTEGER PRIMARY KEY, user TEXT, bio TEXT)")
result.fetchall()

#user can make multiple blogs, each blog containing more posts
result = c.execute("CREATE TABLE blog(id INTEGER PRIMARY KEY, blog_id INTEGER, name TEXT)")
result = c.execute("CREATE TABLE entry(user TEXT, blog_id INTEGER, date TEXT, title TEXT, content TEXT)")
result.fetchall()
"""

# cursor for login database
login_db = sqlite3.connect("login_db.db")
login_cursor = login_db.cursor()

profile_db = sqlite3.connect("profile_db.db")
profile_cursor = profile_db.cursor()

blog_db = sqlite3.connect("blog_db.db") # stores comments, rollback history, etc etc. Should have multiple tables in this table
blog_cursor = blog_db.cursor()


# add other functions and db if needed

@app.route("/")
def home():
    login_link = "/login"
    login_info = '''You are not logged in. Register an account '''
    if "username" in session:
        login_info = "You are logged in as user " + session["username"] + "You can logout "
        login_link = "/logout"
    return render_template("index.html", login_info = login_info, login_link = login_link)

@app.route("/profile")
def profile():
    # if "username" in session:
    return "hi"

# optional search feature at /search

@app.route("/login")
def login():
    session["username"] = "test"
    return "hi"

@app.route("/logout")
def logout():
    session.pop("username")
    return "hi"

"""
# /follow/user ID to follow user
@app.route("/follow")
def follow():
    return "hi"
"""

# create blog here
@app.route("/create")
def create():
    return "hi"

# for blogs you can make /blogs/blog ID   
# for blog editing you can make /blogs/blog ID/edit

def display_blogs():
    idx = 0
    text = ""
    user = ""
    title = ""
    date = ""
    for row in result:
        pull = row  #gets the latest row of info b/c it will loop and change pull until it gets to the end
    user = pull[0]
    idx = pull[1]
    date = pull[2]
    title = pull[3]
    content = pull[4]
    
    
