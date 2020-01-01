import psycopg2
import bot
connection = psycopg2.connect(database='database', user='user',
                              password='password',
                              host='host', port='port')
cursor = connection.cursor()

def addmusic(ytid, tgid, size):
    try:
        cursor.execute('INSERT INTO "audio" VALUES (%s, %s, %s)', (ytid, tgid, size))
        connection.commit()
        return True
    except Exception as e:
        bot.sendMessage(-196479175, str(e) + "--- добавление аудио в базу(db.py, addmusic)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return False


def findsize(ytid):
    try:
        stmt = 'SELECT "size" FROM "audio" WHERE ytid = (%s)'
        args = (ytid,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        bot.sendMessage(-196479175, str(e) + "--- поиск размера в базе(db.py, findsize)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return None

def findmusic(ytid):
    try:
        stmt = 'SELECT "tgid" FROM "audio" WHERE ytid = (%s)'
        args = (ytid,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        if str(e) == "'NoneType' object is not subscriptable":
            return None
        else:
            bot.sendMessage(-106479175, str(e) + "--- поиск музыки в базе(db.py, findmusic)")
            conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
            conn.cursor()
            return None

def count():
    try:
        cursor.execute('SELECT count(*) from "audio"')
        connection.commit()
        return cursor.fetchone()
    except Exception as e:
        bot.sendMessage(-106479175, str(e) + "--- Подсчёт audio")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return False
