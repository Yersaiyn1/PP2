import psycopg2
from configparser import ConfigParser

def config(filename='config.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {param[0]: param[1] for param in parser.items(section)}

def get_connection():
    return psycopg2.connect(**config())

def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT level, score FROM user_scores WHERE username=%s ORDER BY saved_at DESC LIMIT 1", (username,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

def save_score(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
    cur.execute("INSERT INTO user_scores (username, score, level) VALUES (%s, %s, %s)", (username, score, level))
    conn.commit()
    cur.close(); conn.close()
