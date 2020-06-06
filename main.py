import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from login import signup_f, login_f

app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'

@app.route('/')
def main():
    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    if 'username' in session:
        return render_template('upload.html', username = session.get('username'))
    else:
        return redirect(url_for('login'))

@app.route('/viewall')
def view():
    return render_template('viewall.html')

@app.route('/summary/<int:id>')
def summary(id):
    vid_filename="test.mp4"
    summary=[("zdanie1", 5), ("zdanie2", 70)]
    transcript=["zdania dla pierwszej minuty", "zdania dla drugiej minuty", "zdania dla trzeciej minuty"]
    return render_template('summary.html', vid_filename=vid_filename, summary=summary, transcript=transcript, len=len)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('upload'))
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        if login_f(username, password):
            session['username'] = username
            session['password'] = password
            return redirect(url_for('main'))
        else:
            return render_template('login.html', info="Bad login or password!")
    return render_template('login.html', info = "")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('upload'))
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        if signup_f(username, password):
            return redirect(url_for('upload'))
        else:
        	#Bad login or password
            return render_template('signup.html')

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['username']
    del session['password']
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
