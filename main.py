import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response


app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'

@app.route('/')
def main():
    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/viewall')
def view():
    return render_template('viewall.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['username']
    del session['password']
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
