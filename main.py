from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import utils as utl
app = Flask(__name__)   
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods =["GET", "POST"])
def index():
    if session.get('girl1_url') is None:
        session['girl1_url']=utl.pick_random_girl()
        session['girl2_url']=utl.pick_random_girl()
    if session.get('switch_pics'):
        if session['switch_pics'] is True:
            if session['winner'] == 1:
                print("GIRL1WON")
                utl.update_ratings_P(session.get('girl1_url'), session.get('girl2_url'), session.get('winner'), 10)
                session['girl2_url']=utl.pick_random_girl()
            if session['winner'] == 2:
                print("GIRL2WON")
                utl.update_ratings_P(session.get('girl1_url'), session.get('girl2_url'), session.get('winner'), 10)
                session['girl1_url']=utl.pick_random_girl()
            session['switch_pics'] = False           
    
    return render_template("index.html", girl1_url=session.get('girl1_url'), girl2_url=session.get('girl2_url'))
    
@app.route('/image1', methods =["GET", "POST"])
def image1():
    if request.method == "POST":
        session['switch_pics'] = True
        session['winner'] = 1
        return redirect(url_for('index'))
        
@app.route('/image2', methods =["GET", "POST"])
def image2():
    if request.method == "POST":
        session['switch_pics'] = True
        session['winner'] = 2
        return redirect(url_for('index'))

@app.route('/leader_board', methods =["GET", "POST"])
def leader_board():
    return render_template("leaderboard.html", length=10, leader_board=utl.sorted_list()[0], scores=utl.sorted_list()[1], images=utl.sorted_list()[2])
    

    

