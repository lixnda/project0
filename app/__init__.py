from flask import Flask             
from flask import render_template, session 
from flask import request, redirect   
import sqlite3, csv, os

app = Flask(__name__)
secret_hehe = os.urandom(32)
app.secret_key = secret_hehe

app = Flask(__name__)

# cursor for database
DB_FILE = "blog.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

# add other functions and db if needed

"""
#commands for database:
c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS profile(id INTEGER, user TEXT, bio TEXT, blog_id TEXT)")

#user can make multiple blogs, each blog containing more posts
c.execute("CREATE TABLE IF NOT EXISTS blog(blog_id INTEGER, blog_name TEXT, entry_id INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS entry(entry_id INTEGER, date TEXT, title TEXT, content TEXT)")

SELECT profile.id, profile.user, profile.bio, blog.blog_id;
FROM profile;
RIGHT JOIN blog ON profile.blog_id=blog.blog_id;
"""
c.execute("CREATE TABLE IF NOT EXISTS logins(user TEXT, password TEXT, id INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS profile(id INTEGER, user TEXT, bio TEXT, blog_id TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS blog(blog_id INTEGER, blog_name TEXT, entry_id INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS entry(entry_id INTEGER, date TEXT, title TEXT, content TEXT)")

db.commit() #save changes
db.close()  #close database

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
    
    
