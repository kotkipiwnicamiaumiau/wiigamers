import hashlib
import os
import binascii
import sqlite3


def hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def createdb():
    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users(name TEXT,password TEXT)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS videos(title TEXT,id TEXT)''')
    db.commit()
    db.close()

def insertuser(username, hash):
    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    createdb()
    cursor.execute(
        '''INSERT INTO users(name,password) VALUES(?,?)''', (username, hash))
    db.commit()
    db.close()


def signup_f(user, passwd):
    try:
        passwdhash = hash(passwd)
        insertuser(user, passwdhash)
    except BaseException:
        return False
    return True


def login_f(user, passwd):
    if passwd == "":
        return False
    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    cursor.execute('''SELECT password FROM users WHERE name=?''', (user,))
    users = cursor.fetchone()
    if users is None:
        return False
    user1 = users[0]
    db.commit()
    db.close()
    return verify(user1, passwd)
