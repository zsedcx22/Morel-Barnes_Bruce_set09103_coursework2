from flask import Flask, render_template, request, redirect, session
import os
import sqlite3
from random import randint
import time
app = Flask(__name__)
app.secret_key=os.urandom(24)

deck=['1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S',
'12S', '13S', '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H',
'11H', '12H', '13H', '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D',
'10D', '11D', '12D', '13D', '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C',
'9C', '10C', '11C', '12C', '13C']

playerlist=list()
p1hand=list()
p2hand=list()
player1=None
player2=None

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
      con.commit()
      return redirect('/profile/')
  elif(request.method=='GET'):
    return render_template('logintemplate.html')

@app.route('/profile/', methods=['POST','GET'])
def profile():
  global player1
  global player2
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
      print(playerlist)#current issue is that one player is not getting in
      if player1==None:
        if len(playerlist)!=0:
          player1=playerlist[randint(0,len(playerlist)-1)]
        if player1 in playerlist:
          playerlist.remove(player1)
      else:
        if player2==None:
          if len(playerlist)!=0:
            player2=playerlist[randint(0,len(playerlist)-1)]
          if player2 in playerlist:
            playerlist.remove(player2)
      if player1!=None and player2!=None:
        return redirect('/blackjack/{}'.format(123))
        break
  elif request.method=='GET':
    return render_template("profiletemplate.html", username=session['user'],
  wins=session['wins'], losses=session['losses'])

@app.route('/blackjack/<gameid>', methods=['POST','GET'])
def blackjack(gameid):
  if(request.method=='POST'):
    button=request.form["submit"]
    if button=="hitme":
      length=len(p1hand)+1
      while len(p1hand)<length:
        if random not in p1hand:
          if random not in p2hand:
            if session['user']==player1
              p1hand.append(random)
            elif session['user']==player2:
              p2hand.append(random)
      return render_template("blackjacktemplate.html", p1name=player1,
    p2name=player2, p1h=p1hand, p2h=p2hand) #add card to hand
    elif button=="stick":
      if session['user']==player1:
        return
      elif session['user']==player2:
        return render_template("blackjacktemplate.html", p1name=player1,
      p2name=player2, p1h=p1hand, p2h=p2hand) #pass the turn to other player/reveal hands and declare winner
    elif button=="fold":
      con=sqlite3.connect('database/userdb.db')
      cur=con.cursor()
      if session['user']==player1:
        cur.execute('''UPDATE user SET losses=losses+1 WHERE
        username="{}";'''.format(player1))
        cur.execute('''UPDATE user SET wins=wins+1 WHERE
        username="{}";'''.format(player2))
        con.commit()
      elif session['user']==player2:
        cur.execute('''UPDATE user SET losses=losses+1 WHERE
        username="{}";'''.format(player2))
        cur.execute('''UPDATE user SET wins=wins+1 WHERE
        username="{}";'''.format(player1))
        con.commit()
      return #win/loss page
  elif(request.method=='GET'):
    while len(p1hand)<2:
      random=deck[randint(0,len(deck)-1)]
      if random not in p1hand:
        p1hand.append(random)

    while len(p2hand)<2:
      random=deck[randint(0,len(deck)-1)]
      if random not in p2hand:
        if random not in p1hand:
          p2hand.append(random)

    return render_template("blackjacktemplate.html", p1name=player1,
    p2name=player2, p1h=p1hand, p2h=p2hand) #launches the jinja2 template
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, threaded=True)
