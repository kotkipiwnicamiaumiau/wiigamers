import hashlib, os, binascii, sqlite3
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-yo6tm.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.dogs
coll = db.users

def hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def insertuser(username, hash):
    post = {"username": username, "password": hash}
    post_id = coll.insert_one(post)

def signup_f(user, passwd):
    try:
        passwdhash=hash(passwd)
        insertuser(user,passwdhash)
    except:
        return False
    return True

def login_f(user, passwd):
    if passwd == "":
        return False
    res=coll.find_one({"username": user})
    user1=res['password']
    return verify(user1, passwd)
