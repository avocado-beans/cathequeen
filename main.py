from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_session import Session
from datetime import timedelta
import time
import requests
import pymysql
import utils as utl

app = Flask(__name__)   
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
Session(app)



@app.route('/', methods =["GET", "POST"])
def index():
    if not session.get('start_at') is None:
        cloud_stat, conn2 = utl.save_to_cloud(session.get('start_at'), conn)
        conn = conn2
        if cloud_stat == 'RESET':
            session['start_at']=time.time()
    if session.get('girl1_url') is None and session.get('girl2_url') is None:
        print("HELLO")
        conn = pymysql.connect(
        host='sql11.freesqldatabase.com',
        user='sql11700114',
        password='cAe4eMACLu',
        db='sql11700114',
        cursorclass=pymysql.cursors.DictCursor
        )
        cloud_stat, conn2 = utl.save_to_cloud(session.get('start_at'), conn)
        conn = conn2
        session['girl1_url'], clock=utl.pick_random_girl()
        session['girl2_url'], clock=utl.pick_random_girl([], session.get('girl1_url'))
        
        session['girllist1']=[]
        session['girllist2']=[]
        session['exclude']=[]
        session['start_at']=time.time()
        session['time']=0
        utl.check_if_empty(conn)
        
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
                randy, clock = utl.pick_random_girl(session.get('girllist2'), session.get('girl1_url'), session.get('time'), session.get('exclude'))
                if clock==-1:
                    session['exclude']=[]
                    session['time']=0
                if randy == 'FINISHED':
                    print('tehe')
                    session['crush'] = session['girl1_url']
                    return redirect(url_for('crush'))
                session['girl2_url']= randy
                
            if session['winner'] == 2:
                print("GIRL2WON")
                session['girllist2'] = []
                utl.update_ratings_P(session.get('girl1_url'), session.get('girl2_url'), session.get('winner'), 10)
                girllist = session.get('girllist1')
                girllist.append(session.get('girl1_url'))
                session['girllist1'] = girllist
                randy, clock = utl.pick_random_girl(session.get('girllist1'), session.get('girl2_url'), session.get('time'), session.get('exclude'))
                if clock==-1:
                    session['exclude']=[]
                    session['time']=0
                if randy == 'FINISHED':
                    print('tehe')
                    session['crush'] = session['girl2_url']
                    return redirect(url_for('crush'))
                session['girl1_url']= randy
            session['switch_pics'] = False           
    
    return render_template("index.html", girl1_url=session.get('girl1_url'), girl2_url=session.get('girl2_url'))
    
@app.route('/image1', methods =["GET", "POST"])
def image1():
    if not session.get('start_at') is None:
        cloud_stat, conn2 = utl.save_to_cloud(session.get('start_at'), conn)
        conn = conn2
        if cloud_stat == 'RESET':
            session['start_at']=time.time()
    if request.method == "POST":
        session['switch_pics'] = True
        session['winner'] = 1
        return redirect(url_for('index'))
        
@app.route('/image2', methods =["GET", "POST"])
def image2():
    if not session.get('start_at') is None:
        cloud_stat, conn2 = utl.save_to_cloud(session.get('start_at'), conn)
        conn = conn2
        if cloud_stat == 'RESET':
            session['start_at']=time.time()
    if request.method == "POST":
        session['switch_pics'] = True
        session['winner'] = 2
        return redirect(url_for('index'))

@app.route('/leader_board', methods =["GET", "POST"])
def leader_board():
    if not session.get('start_at') is None:
        cloud_stat, conn2 = utl.save_to_cloud(session.get('start_at'), conn)
        conn = conn2
        if cloud_stat == 'RESET':
            session['start_at']=time.time()
    sorted = utl.sorted_list()
    return render_template("leaderboard.html", length=len(sorted[0]), leader_board=sorted[0], scores=sorted[1], images=sorted[2])

@app.route('/your_crush', methods =["GET", "POST"])
def crush():
    if not session.get('start_at') is None:
        cloud_stat, conn2 = utl.save_to_cloud(session.get('start_at'), conn)
        conn = conn2
        if cloud_stat == 'RESET':
            session['start_at']=time.time()
    if not session['crush'] in session.get('exclude'):
        session['girl1_url'], clock=utl.pick_random_girl()
        session['girl2_url'], clock=utl.pick_random_girl([], session.get('girl1_url'))
        session['girllist1']=[]
        session['girllist2']=[]
        session['time']=time.time()
        exclude=session['exclude']
        exclude.append(session['crush'])
        session['exclude'] = exclude
    return render_template("winner.html", girlurl=session.get('crush'))
    
@app.route("/get_total_scores", methods=["GET"])
def get_total_scores():
    file = open('ratings.txt','r')
    ratings = file.readlines()
    file.close()
    return ratings
