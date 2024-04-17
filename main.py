from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session

from datetime import timedelta
import utils as utl

app = Flask(__name__)   
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
Session(app)

@app.route('/', methods =["GET", "POST"])
def index():
    if session.get('girl1_url') is None and session.get('girl2_url') is None:
        print("HELLO")
        session['girl1_url']=utl.pick_random_girl()
        session['girl2_url']=utl.pick_random_girl([], session.get('girl1_url'))
        session['girllist1'] =[]
        session['girllist2'] =[]
        print("BYE")
        
    if session.get('switch_pics') is True:
        print(session.get('girl1_url'), session.get('girl2_url'))
        if session['switch_pics'] is True:
            if session['winner'] == 1:
                print("GIRL1WON")
                session['girllist1'] = []
                utl.update_ratings_P(session.get('girl1_url'), session.get('girl2_url'), session.get('winner'), 10)
                girllist = session.get('girllist2')
                girllist.append(session.get('girl2_url'))
                session['girllist2'] = girllist
                randy = utl.pick_random_girl(session.get('girllist2'), session.get('girl1_url'))
                if randy == session['girl2_url']:
                    girlurl = session['girl1_url']
                    return render_template("winner.html", girlurl)
                session['girl2_url']= randy
            if session['winner'] == 2:
                print("GIRL2WON")
                session['girllist2'] = []
                utl.update_ratings_P(session.get('girl1_url'), session.get('girl2_url'), session.get('winner'), 10)
                girllist = session.get('girllist1')
                girllist.append(session.get('girl1_url'))
                session['girllist1'] = girllist
                randy = utl.pick_random_girl(session.get('girllist1'), session.get('girl2_url'))
                if randy == session['girl1_url']:
                    girlurl = session['girl2_url']
                    return render_template("winner.html", girlurl)
                session['girl1_url']= randy
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
    return render_template("leaderboard.html", length=len(utl.sorted_list()[0]), leader_board=utl.sorted_list()[0], scores=utl.sorted_list()[1], images=utl.sorted_list()[2])
    
