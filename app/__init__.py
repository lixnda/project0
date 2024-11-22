from flask import Flask, render_template, request, redirect, url_for,g,session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)  # Replace 'your_secret_key' with a strong, random key
DATABASE = 'database.db'

def get_db(): #opens connection
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception): #closes connection
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        #cursor.execute('drop table if exists user ')
        cursor.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT NOT NULL,username TEXT NOT NULL,password TEXT NOT NULL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS blog (blogid INTEGER PRIMARY KEY AUTOINCREMENT, blogname TEXT NOT NULL, blogdesc TEXT NOT NULL, id Integer,FOREIGN KEY(id) REFERENCES user(id))')
        cursor.execute('CREATE TABLE IF NOT EXISTS blogpost (postid INTEGER PRIMARY KEY AUTOINCREMENT, postname TEXT NOT NULL, postdesc TEXT NOT NULL, blogid Integer,FOREIGN KEY(blogid) REFERENCES blog(blogid))')
        db.commit()

# Initialize the database
init_db()


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route("/", methods = ['GET', 'POST'])
def disp_loginpage():
    if request.method=='POST':
        db = get_db()
        cursor = db.cursor()
        if request.method == 'POST':
            username = request.form['username']
            password= request.form['password']
        cursor.execute('SELECT ID FROM user WHERE username= ? and password=?', (username,password))
        db_row = cursor.fetchone()
        if db_row:
            session['username'] = username
            session['id'] = db_row[0]
            return redirect(url_for('read_profile'))
        else:
            return render_template("login.html")
           
    else:
        return render_template("login.html")    
        

@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == 'GET':
        session.pop('username')
        session.pop('id')
        return render_template("login.html")
    
@app.route('/<name>')
def hello(name):
    """Renders a sample page."""
    message=request.args.get('msg','')
    return "Hello World! to " + name + " --- " + message


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        return render_template('create.html')

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO user (name, email,username,password) VALUES (?, ?,?,?)', (name, email,username,password))
        db.commit()
        return redirect(url_for('disp_loginpage'))
    return render_template('create.html')
   

@app.route('/createblog', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        blogname = request.form['blogname']
        blogdesc= request.form['blogdesc']
        _id = session.get('id')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO blog (blogname, blogdesc,id) VALUES (?, ?,?)', (blogname, blogdesc,_id))
        db.commit()
        return redirect(url_for('read_profile'))
    return render_template('createblog.html')
   
@app.route('/createblogpost/<int:blog_id>', methods=['GET', 'POST'])
def create_blogpost(blog_id):
    if request.method == 'POST':
        postname = request.form['postname']
        postdesc= request.form['postdesc']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO blogpost (postname, postdesc,blogid) VALUES (?, ?,?)', (postname, postdesc,blog_id))
        db.commit()
        return redirect(url_for('read_blogpost',blog_id=blog_id))
    return render_template('createblogpost.html',blog_id=blog_id)
   



# READ
@app.route('/read')
def read_users():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user')
        db_rows = cursor.fetchall()
        return render_template('read.html', db_rows=db_rows)
    else: 
        return render_template("login.html")    

# READ BLog
@app.route('/profile')
def read_profile():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM blog where id=' + str(session.get('id')) )
        db_rows = cursor.fetchall()
        return render_template('profile.html', db_rows=db_rows)
    else: 
        return render_template("login.html")    


# READ Post
@app.route('/blogpost/<int:blog_id>')
def read_blogpost(blog_id):
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM BlogPost where Blogid=' + str(blog_id) )
        db_rows = cursor.fetchall()
        cursor.execute('SELECT Blogname FROM Blog where Blogid=' + str(blog_id) )
        db_row_blogname = cursor.fetchone()
        blog_name=db_row_blogname[0]
        return render_template('BlogPost.html', db_rows=db_rows,blog_id=blog_id,blog_name=blog_name)
    else: 
        return render_template("login.html")    

    
# UPDATE
@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            cursor.execute('UPDATE user SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
            db.commit()
            return redirect(url_for('read_users'))
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return render_template('update.html', user=user)
    else: 
        return render_template("login.html")    

# UPDATE BLOG
@app.route('/updateblog/<int:blog_id>', methods=['GET', 'POST'])
def update_blog(blog_id):
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        if request.method == 'POST':
            blogname = request.form['blogname']
            blogdesc= request.form['blogdesc']
            _id = session.get('id')
            cursor.execute('UPDATE blog SET blogname = ?, blogdesc= ? WHERE blogid = ?', (blogname, blogdesc, blog_id))
            db.commit()
            return redirect(url_for('read_profile'))
        cursor.execute('SELECT * FROM blog WHERE blogid = ?', (blog_id,))
        db_row = cursor.fetchone()
        return render_template('blogupdate.html', db_row=db_row)
    else: 
        return render_template("login.html")    

# UPDATE BLOG
@app.route('/updateblogpost/<int:blog_id>/<int:post_id>', methods=['GET', 'POST'])
def update_blogpost(blog_id,post_id):
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        if request.method == 'POST':
            postname = request.form['postname']
            postdesc= request.form['postdesc']
            _id = session.get('id')
            cursor.execute('UPDATE blogpost SET postname = ?, postdesc= ? WHERE postid = ?', (postname, postdesc, post_id))
            db.commit()
            return redirect(url_for('read_blogpost',blog_id=blog_id))
        cursor.execute('SELECT * FROM blogpost WHERE postid =' + str(post_id))
        db_row = cursor.fetchone()
        return render_template('blogpostupdate.html', blog_id=blog_id,db_row=db_row)
    else: 
        return render_template("login.html")    


# DELETE
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
        db.commit()
        return redirect(url_for('read_users'))
    else: 
        return render_template("login.html")    
    
# DELETE
@app.route('/delete/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    if 'blogname' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM blog WHERE blogid = ?', (blog_id,))
        db.commit()
        return redirect(url_for('read_blogs'))
    else: 
        return render_template("login.html")    

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
