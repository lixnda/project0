from flask import Flask
from flask import render_template, session
from flask import request, redirect
import sqlite3, csv, os
from datetime import datetime

app = Flask(__name__)
secret_hehe = os.urandom(32)
app.secret_key = secret_hehe

DB_FILE = "blog.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS logins(name TEXT PRIMARY KEY, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS profile(name TEXT PRIMARY KEY, followers INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS blog(blog_id INTEGER PRIMARY KEY, blog_name TEXT, description TEXT, name TEXT, FOREIGN KEY(name) REFERENCES profile(name))")
c.execute("CREATE TABLE IF NOT EXISTS entry(entry_id INTEGER PRIMARY KEY, date INTEGER, title TEXT, content TEXT, blog_id INTEGER, FOREIGN KEY(blog_id) REFERENCES blog(blog_id))")

"""
------------------READ THIS----------------
to see all blogs a user has:

execute:
"SELECT blog.blog_id, blog.blog_name
FROM blog
WHERE id=<profile_you_want_to_list_blogs_for>;"

-------------------------------------------
similarly,
to see all the entries a blog has:

"SELECT entry.entry_id, entry.date, entry.title
FROM entry
WHERE blog_id=<blog_you_want_to_list_entries_for>"

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

    query = """
        SELECT entry.entry_id, entry.date, entry.title, entry.content, entry.blog_id, blog.blog_name
        FROM entry
        JOIN blog ON entry.blog_id = blog.blog_id
    """

    c.execute(query)
    rows = c.fetchall()  # [Post ID, UNIX TIMESTAMP, Title, Content, Blog ID, Author]

    # FOR TESTING
    # rows = [
    #     (1, 123, "This is a Title", "These are the contents ", 1, "Bob"),
    #     (2, 321, "This is a Title For Blog 2",
    #      "Lorem ipsum odor amet, consectetuer adipiscing elit. Montes iaculis auctor magnis sagittis maecenas egestas class velit. Hac odio erat tellus penatibus, nunc dis litora. Odio egestas est dignissim sodales nec tempor parturient massa. Class ultricies torquent himenaeos sit libero dignissim libero. Vel facilisi mollis morbi ad magna cursus sollicitudin fringilla. Vel pharetra interdum at varius integer habitasse. Molestie curabitur euismod in viverra blandit sociosqu id. Litora aptent volutpat posuere porttitor fringilla.",
    #      2, "Joe")
    # ]

    rows.sort(key=lambda x: x[1], reverse=True)

    to_display = []  # [Counter, Post ID, UNIX TIMESTAMP, Title, Content, Blog ID, Author, blog TITLE]
    for i in range(min(10, len(rows))):
        row = list(rows[i])
        counter = i + 1
        entry_id, timestamp, title, content, blog_id, author = row
        timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        if len(content) > 300:
            content = content[:300] + "..."
        c.execute("SELECT blog_name FROM blog WHERE blog_id = ?", (blog_id,))
        blog_title = c.fetchone()[0]
        # blog_title = "skibidi"
        to_display.append([counter, entry_id, timestamp, title, content, blog_id, author, blog_title])

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

    c.execute("PRAGMA table_info(profile)")
    columns = c.fetchall()
    print(columns)

    c.execute("SELECT name, followers FROM profile WHERE name = ?", (username,))
    rows = c.fetchone()

    # cur = database.cursor()
    # cur.execute("SELECT * FROM Blogs WHERE Author = "+username)
    # blog_rows = cur.fetchall()

    c.execute("""
        SELECT blog_id, blog_name, description, name
        FROM blog
        WHERE name = ?
    """, (username,))
    blog_rows = c.fetchall()  # Each row will contain [blog_id, blog_name, description, author]

    # blog_rows = [
    #     (1, "Blog 1", "Hi this is a description", "Bob"),
    #     (2, "Blog 2",  "Hi this is a description 2", "Bob")
    # ]

    return render_template("profile.html",
                           logged_user = session["username"],
                           username = username,
                           info = rows,
                           blogs = blog_rows
        )

@app.route("/search_user", methods=['POST'])
def search_user():
    if "username" not in session:
        return redirect("/login")
    return redirect("/profile/"+request.form['search'])

@app.route("/login")
def login():
    session["username"] = "test"
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

@app.route("/follow/<username>", methods=['POST'])
def follow(username):
    # follow user, add to database, and redirect to where they came from
    # maybe a post request will do
    # ADD STUFF HERE
    return redirect(request.referrer)

# create blog here
@app.route("/create", methods =['GET','POST'])
def create():
    if "username" not in session:
        return redirect("/login")
    if request.method == 'POST':
        blog_id = c.lastrowid()
        blog_name = request.form.get('name')
        blog_desc = request.form.get('Description')
        name = session['username']
        vals = (blog_name, blog_desc, name)
        command = f"INSERT INTO blog(blog_name, description, name) VALUES(?,?,?)"
        c.execute(command, vals)
        db.commit()
        return redirect(f"/profile/name")
    return render_template("blogs.html")

# for blogs you can make /blogs/blog ID
# for blog editing you can make /blogs/blog ID/edit

def display_blogs(blog_id):
    rows = [
        (1, 123, "This is a Title", "These are the contents ", 1, "Bob"),
        (2, 321, "This is a Title For Blog 2",
         "Lorem ipsum odor amet, consectetuer adipiscing elit. Montes iaculis auctor magnis sagittis maecenas egestas class velit. Hac odio erat tellus penatibus, nunc dis litora. Odio egestas est dignissim sodales nec tempor parturient massa. Class ultricies torquent himenaeos sit libero dignissim libero. Vel facilisi mollis morbi ad magna cursus sollicitudin fringilla. Vel pharetra interdum at varius integer habitasse. Molestie curabitur euismod in viverra blandit sociosqu id. Litora aptent volutpat posuere porttitor fringilla.",
         2, "Joe")
    ]
    idx = blog_id
    user = rows[0][5]
    date = datetime.utcfromtimestamp(rows[0][1]).strftime('%Y-%m-%d %H:%M:%S')
    title = rows[2]
    text = rows[3]

if __name__ == "__main__":
    app.debug = True
    app.run()

if __name__ == "__main__":
    app.debug = True
    app.run()
