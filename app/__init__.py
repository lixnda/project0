from flask import Flask
from flask import render_template, session
from flask import request, redirect
import sqlite3, csv, os
from datetime import datetime

app = Flask(__name__)
secret_hehe = os.urandom(32)
app.secret_key = secret_hehe

DB_FILE = "blog.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS logins(id INTEGER PRIMARY KEY, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS profile(id INTEGER PRIMARY KEY, bio TEXT, blog_id TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS blog(blog_id INTEGER PRIMARY KEY, blog_name TEXT, id INTEGER, FOREIGN KEY(id) REFERENCES profile(id))")
c.execute("CREATE TABLE IF NOT EXISTS entry(entry_id INTEGER PRIMARY KEY, date TEXT, title TEXT, content TEXT, blog_id INTEGER, FOREIGN KEY(blog_id) REFERENCES blog(blog_id))")

"""
------------------READ THIS----------------
to see all blogs a user has:

execute:
"SELECT blog.blog_id, blog.blog_name
FROM blog
WHERE blog.id=<profile_you_want_to_list_blogs_for>;"

-------------------------------------------
similarly,
to see all the entries a blog has:

"SELECT entry.entry_id, entry.date, entry.title
FROM entry
WHERE blog_id=<blog_you_want_to_list_entries_for>
"""

@app.route("/")
def home():
    login_link = "/login"
    login_info = '''You are not logged in. Register an account '''
    username = "?"
    if "username" in session:
        login_info = "You are logged in as user " + session["username"] + ". You can logout "
        login_link = "/logout"
        username = session["username"]
    # cur = database.cursor()
    # cur.execute("SELECT * FROM Posts") #subject to change
    # rows = cur.fetchall() # [Post ID, UNIX TIMESTAMP, Title, Content, Blog ID, Author]

    # FOR TESTING
    rows = [
        (1, 123, "This is a Title", "These are the contents ", 1, "Bob"),
        (2, 321, "This is a Title For Blog 2",
         "Lorem ipsum odor amet, consectetuer adipiscing elit. Montes iaculis auctor magnis sagittis maecenas egestas class velit. Hac odio erat tellus penatibus, nunc dis litora. Odio egestas est dignissim sodales nec tempor parturient massa. Class ultricies torquent himenaeos sit libero dignissim libero. Vel facilisi mollis morbi ad magna cursus sollicitudin fringilla. Vel pharetra interdum at varius integer habitasse. Molestie curabitur euismod in viverra blandit sociosqu id. Litora aptent volutpat posuere porttitor fringilla.",
         2, "Joe")
    ]

    rows.sort(key=lambda x: x[1], reverse=True)

    to_display = []  # [Counter, Post ID, UNIX TIMESTAMP, Title, Content, Blog ID, Author, BLOG TITLE]
    for i in range(min(10, len(rows))):
        to_display.append([i + 1] + list(rows[i]))
        to_display[i][2] = datetime.utcfromtimestamp(to_display[i][2]).strftime('%Y-%m-%d %H:%M:%S')
        if len(to_display[i][4]) > 300:
            to_display[i][4] = to_display[i][4][:300] + "..."

        # cur = database.cursor()
        # cur.execute("SELECT * FROM Blog WHERE BlogID = " + str(to_display[5])
        # item = cur.fetchone() [blogID, data published, name, description, author]
        # to_display[i].append(item[2])

        to_display[i].append("skibidi " + str(i)) # FOR TESTING

    return render_template("index.html",
                           user=username,
                           login_info=login_info,
                           login_link=login_link,
                           posts=to_display
                           )


@app.route("/profile/<username>")
def profile(username):
    # make sure you are logged in
    if "username" not in session:
        return redirect("/login")

    # cur = database.cursor()
    # cur.execute("SELECT * FROM Profile WHERE username = "+username)
    # rows = cur.fetchone() [ID, username, followers]
    rows = [1, "bob", 323]

    # cur = database.cursor()
    # cur.execute("SELECT * FROM Blogs WHERE Author = "+username)
    # blog_rows = cur.fetchall()

    blog_rows = [
        (1, "Blog 1", 3123, "Hi this is a description", "Bob"),
        (2, "Blog 2", 323, "Hi this is a description 2", "Bob")
    ]
    to_display = []
    for i in range(len(blog_rows)):
        to_display.append(list(blog_rows[i]))
        to_display[i][2] = datetime.utcfromtimestamp(to_display[i][2]).strftime('%Y-%m-%d %H:%M:%S')
    blog_rows.sort(key=lambda x: x[2], reverse=True)
    return render_template("profile.html", info = rows, blogs = to_display)


# optional search feature at /search

@app.route("/login")
def login():
    session["username"] = "test"
    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


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

if __name__ == "__main__":
    app.debug = True
    app.run()
