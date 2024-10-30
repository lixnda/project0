from flask import Flask             
from flask import render_template   
from flask import request   
import sqlite3, csv

app = Flask(__name__)
# add other functions if needed

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return "hi"

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

if __name__ == "__main__":
    app.debug = True 
    app.run()
