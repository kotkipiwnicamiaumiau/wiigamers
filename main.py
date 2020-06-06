import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response


app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'

@app.route('/')
def main():
    return render_template('upload.html')

if __name__=='__main__':
    app.run(debug=True)
