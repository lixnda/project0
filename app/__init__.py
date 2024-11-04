from flask import Flask             
from flask import render_template   
from flask import request   
import sqlite3, csv

app = Flask(__name__)

# cursor for database
DB_FILE = "blog.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

# add other functions and db if needed

"""
commands for database:
c.execute("CREATE TABLE logins(user TEXT, password TEXT, id INTEGER)")
c.execute("CREATE TABLE profile(id INTEGER, name TEXT)")

#user can make multiple blogs, each blog containing more posts
c.execute("CREATE TABLE blog(id INTEGER, blog_id INTEGER, name TEXT, bio TEXT)")
c.execute("CREATE TABLE post(blog_id INTEGER, date TEXT, title TEXT, content TEXT)")
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

# optional search feature at /search

@app.route("/login")
def login():
    return "hi"

@app.route("/logout")
def logout():
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

@app.route("/addPost")
def addPost():
    return "hi"

@app.route("/editPost")
def editPost():
    return "hi"
# for blogs you can make /blogs/blog ID   
# for blog editing you can make /blogs/blog ID/edit

def blogs():
    return "hi"

#allowing users to like, comment, follow, track those numbers
def like():
    like_count = 0
    return "hi"

def comment():
    comments_num = 0
    return "hi"

def follow():
    follow_count = 0
    return "hi"


if __name__ == "__main__":
    app.debug = True 
    app.run()
