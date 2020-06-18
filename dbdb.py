import sqlite3

def dbcon():
    return sqlite3.connect('mydb.db')

def create_table():
    try:
        query = '''
            CREATE TABLE "users" (
                "id"    varchar(50),
                "pw"    varchar(50),
                "name"  varchar(50),
                "hp"    INTEGER,
                "mp"    INTEGER,
                PRIMARY KEY("id")
            )
        '''
        db = dbcon()
        c = db.cursor()
        c.execute(query)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()

def insert_user(id, pw, name):
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (id, pw, name, 30, 10)
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()

def select_all():
    ret = list()
    try:
        db = dbcon()
        c = db.cursor()
        c.execute('SELECT * FROM users')
        ret = c.fetchall()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
    return ret

def select_user(id, pw):
    ret = ()
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (id, pw)
        c.execute('SELECT * FROM users WHERE id = ? AND pw = ?', setdata)
        ret = c.fetchone()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
    return ret

def check_id(id):
    ret = ()
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (id,)
        c.execute('SELECT * FROM users WHERE id = ?', setdata)
        ret = c.fetchone()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
    return ret

def set_status(hp, mp, id):
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (hp, mp, id)
        c.execute('UPDATE users SET hp = ?, mp = ? WHERE id = ?', setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()