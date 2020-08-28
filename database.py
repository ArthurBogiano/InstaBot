import base64


def createdb(conn):
    sql = conn.cursor()
    sql.execute("CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY, user TEXT, pass TEXT)")
    sql.execute("CREATE TABLE IF NOT EXISTS config ("
                " id INTEGER PRIMARY KEY,"
                " instatime INTEGER DEFAULT 2,"
                " logintime INTEGER DEFAULT 5,"
                " urltime INTEGER DEFAULT 2,"
                " commenttime INTEGER DEFAULT 3,"
                " liketime INTEGER DEFAULT 2,"
                " logouttime INTEGER DEFAULT 2"
                ")")
    sql.execute("CREATE TABLE IF NOT EXISTS pessoas (id INTEGER PRIMARY KEY, username TEXT)")


def listlogins(conn):
    sql = conn.cursor()
    sql.execute("SELECT * FROM login")
    return sql.fetchall()


def addlogin(conn, user, senha):
    sql = conn.cursor()
    query = f"INSERT INTO login (user, pass) VALUES ('{user}', '{base64.b64encode(senha.encode()).decode()}');"
    sql.execute(query)
    conn.commit()


def dellogin(conn, id):
    sql = conn.cursor()
    query = f"DELETE FROM login WHERE id = {id};"
    sql.execute(query)
    conn.commit()


def listpessoas(conn):
    sql = conn.cursor()
    sql.execute("SELECT * FROM pessoas")
    return sql.fetchall()


def addpessoa(conn, user):
    sql = conn.cursor()
    query = f"INSERT INTO pessoas (username) VALUES ('{user}');"
    sql.execute(query)
    conn.commit()


def delpessoa(conn, id):
    sql = conn.cursor()
    query = f"DELETE FROM pessoas WHERE id = {id};"
    sql.execute(query)
    conn.commit()


