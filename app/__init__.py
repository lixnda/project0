from flask import Flask             
from flask import render_template   
from flask import request   
import sqlite3, csv

app = Flask(__name__)

# cursor for login database
login_db = sqlite3.connect("login_db.db")
login_cursor = login_db.cursor()

profile_db = sqlite3.connect("profile_db.db")
profile_cursor = profile_db.cursor()

blog_db = sqplite3.connect("blog_db.db") # stores comments, rollback history, etc etc. Should have multiple tables in this table
blog_cursor = blog_db.cursor()

# add other functions and db if needed


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
