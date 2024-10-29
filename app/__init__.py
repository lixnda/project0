from flask import Flask             
from flask import render_template   
from flask import request   
import sqlite3, csv

app = Flask(__name__)

@app.route("/")
def homepage():
    return "hi"
    
if __name__ == "__main__":
    app.debug = True 
    app.run()
