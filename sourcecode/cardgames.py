from flask import Flask, render_template, request, redirect, session
import os
import sqlite3
from random import randint
import time
app = Flask(__name__)
app.secret_key=os.urandom(24)
#@app.route('/')
#def init():
#  return render_template("logintemplate.html")
playerlist=[]
@app.route('/', methods=['POST','GET'])
def login():
  if(request.method=='POST'):
    user = request.form['usr']
    pwd = request.form['pwd']
    print(user + pwd)
    #if username and password match then
    con=sqlite3.connect("database/userdb.db")
    cur=con.cursor()
    cur.execute('''SELECT * FROM user WHERE username="{}";'''.format(user))
    x=cur.fetchone()
    if(x!=None):
      if(x[1]==pwd):
        session['user']=user
        session['wins']=x[2]
        session['losses']=x[3]
        return redirect('/profile/')
      else:
        return render_template("logintemplate.html")
    else:
      cur.execute('''INSERT INTO user(username,password,wins,losses)
      VALUES("{}","{}",0,0);'''.format(user,pwd))
      session['user']=user
      session['wins']=0
      session['losses']=0
      return redirect('/profile/')
  elif(request.method=='GET'):
    return render_template('logintemplate.html')
@app.route('/profile/', methods=['POST','GET'])
def profile():
  if request.method == 'POST':
    #when a player clicks to join the queue add them to a list
    #where then once there are at least 2 players randomly choose 2
    #and chuck them into a game by using session to keep track of
    #players 1 and 2
    playerlist.append(session['user'])
    count=0
    while count<30:
      time.sleep(1)
      print count
      count+=1
      if len(playerlist)>=2:
        if session['P1']==None:
          session['P1']=randint(0,len(playerlist))
          playerlist.remove(session['P1'])
        elif session['P2']==None:
          session['P2']=randint(0,len(playerlist))
          playerlist.remove(session['P2'])
        return redirect('/blackjack/')
  elif request.method=='GET':
    return render_template("profiletemplate.html", username=session['user'],
  wins=session['wins'], losses=session['losses'])
@app.route('/blackjack/', methods=['POST','GET'])
def blackjack():
  if request.method=='POST':
    #function for each button (keep it to hit stick and fold)
    #if hit then randomly select a non dealt card and deal it to the player
    #if stick then pass turn then if p2 compare
    #fold makes active player lose
  elif request.method=='GET':
    return render_template("blackjacktemplate.html", p1name=session['P1'],
    p2name=session['P2']) #launches the jinja2 template
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, threaded=True)
