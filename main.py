import os
import os.path
import random
import hashlib
import sys
import json
import string
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from login import signup_f, login_f
from werkzeug.utils import secure_filename
from utils import handle_video

UPLOAD_FOLDER = 'static/vid'
ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return redirect(url_for('upload'))


@app.route('/upload', methods=["GET", 'POST'])
def upload():
    if request.method == "GET":
        if 'username' in session:
            return render_template('upload.html', username=session.get('username'))
        else:
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print("bbs")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            rand_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            filename = secure_filename(rand_id + '.mp4')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            handle_video(rand_id)
            return redirect(url_for('viewall'))


@app.route('/viewall')
def viewall():
    return render_template('viewall.html')


@app.route('/summary/<int:id>')
def summary(id):
    vid_filename="test.mp4"
    summary=[("zdanie1", 5), ("zdanie2", 70)]
    transcript=["zdania dla pierwszej minuty", "zdania dla drugiej minuty", "zdania dla trzeciej minuty"]
    title="Generated Title"
    return render_template('summary.html', vid_filename=vid_filename, summary=summary, transcript=transcript, title=title, len=len)

@app.route('/about')
def about():
    return render_template('about.html')

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
    return render_template('login.html', info="")


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
            # Bad login or password
            return render_template('signup.html')

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['username']
    del session['password']
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
