from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import utils as utl
app = Flask(__name__)   
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods =["GET", "POST"])
def index():
    return render_template("index.html")

    

