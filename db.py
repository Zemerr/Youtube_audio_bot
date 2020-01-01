import psycopg2
import bot

connection = psycopg2.connect(database='database', user='user',
                              password='password',
                              host='host', port='port')
cursor = connection.cursor()

def add_user(id, language, status, time, log):
     try:
        cursor.execute('INSERT INTO "users" VALUES (%s, %s, %s, %s, %s)', (id, language, status, time, log))
        connection.commit()
        return True
     except(psycopg2.errors.UniqueViolation):
         cursor.execute("ROLLBACK")
         connection.commit()
         cursor.execute('UPDATE "users" SET "language" = (%s) WHERE id = (%s)', (language, id))
         connection.commit()
         return True
     except Exception as e:
         bot.sendMessage(-10396479175, str(e) + "--- добавление юзера в базу(db.py, add_user)")
         conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
         conn.cursor()
         return False

def status(id, status):
    try:
        cursor.execute('UPDATE "users" SET "status" = (%s) WHERE id = (%s)', (status, id))
        connection.commit()
        return True
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- изменение статуса(db.py, status)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return

def editlog(id, log):
    try:
        cursor.execute('UPDATE "users" SET "log" = (%s) WHERE id = (%s)', (log, id))
        connection.commit()
        return True
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- изменение лога(db.py, editlog)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return

def aud(numb):
    try:
        stmt = """SELECT "time" FROM (SELECT ROW_NUMBER () OVER (ORDER BY status) AS RowNum, * FROM public.users) sub WHERE RowNum = (%s)"""
        args = (numb,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- рассылка (db.py, aud)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return 0

def rassilka(numb):
    try:
        stmt = """SELECT "id" FROM (SELECT ROW_NUMBER () OVER (ORDER BY status) AS RowNum, * FROM public.users) sub WHERE RowNum = (%s)"""
        args = (numb,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- рассылка (db.py, rassilka)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return '583128078'

def getlog(id):
    try:
        stmt = """SELECT "log" FROM public.users WHERE id = (%s)"""
        args = (id,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- выбор лога юзера из базы(db.py, getlog)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return '2'

def addtimes(time, id):
    try:
        cursor.execute('UPDATE "users" SET "time" = (%s) WHERE id = (%s)', (time, id))
        connection.commit()
        return True
    except Exception as e:
        bot.sendMessage(-10096479175, str(e) + "--- добавление раза в базу(db.py, addtimes)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return False

def active():
    try:
        cursor.execute('SELECT count(*) from "users" WHERE "status" = 1')
        connection.commit()
        return cursor.fetchone()
    except Exception as e:
        bot.sendMessage(-10096479175, str(e) + "--- Подсчёт актив")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return False

def deactive():
    try:
        cursor.execute('SELECT count(*) from "users" WHERE "status" = 0')
        connection.commit()
        return cursor.fetchone()
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- Подсчёт неактив")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return False

def count():
    try:
        cursor.execute('SELECT count(*) from "users"')
        connection.commit()
        return cursor.fetchone()
    except Exception as e:
        bot.sendMessage(-10396479175, str(e) + "--- Подсчёт")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return False

def get_language(id):
    try:
        stmt = """SELECT "language" FROM public.users WHERE id = (%s)"""
        args = (id,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        bot.sendMessage(-10096479175, str(e) + "--- выбор языка юзера из базы(db.py, get_language)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return "en"

def gettimes(id):
    try:
        stmt = """SELECT "time" FROM public.users WHERE id = (%s)"""
        args = (id,)
        cursor.execute(stmt, args)
        p = cursor.fetchone()
        b = p[0]
        return b
    except Exception as e:
        bot.sendMessage(-10013979175, str(e) + "--- подсчёт количества раз(db.py, gettimes)")
        conn = psycopg2.connect(database='database', user='user', password='password', host='host', port='port')
        conn.cursor()
        return 0

