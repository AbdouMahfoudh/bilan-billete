import sqlite3
def select (sql, par=None):
    con = sqlite3.connect('Mybase.db')

    c = con.cursor()
    if par is not None :
        c.execute(sql,par)
    else : c.execute(sql)
    res = c.fetchall()
    c.close()
    con.close()
    return res

def insert (sql, par=None):
    con = sqlite3.connect('Mybase.db')

    c = con.cursor()
    if par is not None :
        c.execute(sql,par)
    else : c.execute(sql)
    c.close()
    con.commit()
    con.close()