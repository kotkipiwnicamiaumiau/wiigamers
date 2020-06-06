import sqlite3

def getVideos():
    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    cursor.execute(
        '''SELECT title, id FROM videos''')
    return cursor.fetchall()
