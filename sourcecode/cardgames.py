from flask import Flask, render_template, request, redirect
import os
app = Flask(__name__)
@app.route('/')
def init():
  return render_template(cardtemplate.html)
@app.route('/', methods=['POST'])
def login():
  user = request.form['username']
  pwd = request.form['password']
  #if username and password match then
  return redirect('/profile/')
  #else if username not taken create new account else return error
  return redirect('/profile/')
  #
  return render_template(cardtemplate.html)
@app.route('/profile/')
def profile_load():
  retrun render_template(profiletemplate.html)
@app.route('/profile/', methods=['POST','GET'])
def profile():
  if request.method == 'POST':
    button_id = request.form['top_button_id']
    #or just use top bar buttons
    #if button profile
    return render_template(profiletemplate.html)
@app.route('/blackjack/', methods=['POST','GET'])
def blackjack():
  if request.method=='POST':
    #print(request.form.getlist('submit')[1:])
  elif request.method=='GET':
    return render_template('sharktemplate.html', sharkorder=sharkorder,
      sharkfamily=sharkfamily, sharkgenus=sharkgenus, sharkname=sharkname,
      sharks=sharks) #launches the jinja2 template

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
