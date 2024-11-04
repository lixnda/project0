from flask import Flask             
from flask import render_template, session 
from flask import request, redirect   
import sqlite3, csv, os

app = Flask(__name__)
secret_hehe = os.urandom(32)
app.secret_key = secret_hehe

database = sqlite3.connect("database.db") # stores everything
@app.route("/")
def home():
    login_link = "/login"
    login_info = '''You are not logged in. Register an account '''
    if "username" in session:
        login_info = "You are logged in as user " + session["username"] + ". You can logout "
        login_link = "/logout"
    # cur = database.cursor()
    # cur.execute("SELECT * FROM Posts") #subject to change
    # rows = cur.fetchall() # [Post ID, UNIX TIMESTAMP, Title, Content, Blog ID, Author]
    
    rows = [1, 123, "This is a Title", "These are the contents ", 123, "Bob"]

    return render_template("index.html", login_info = login_info, login_link = login_link)

@app.route("/profile")
def profile():
    if "username" in session:
        user = session["username"]
        return render_template("profile.html", user=user)
    else:
        return redirect("/login")
    

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

def blogs():
    return "hi"

if __name__ == "__main__":
    app.debug = True 
    app.run()
