import os
import pymysql

def get_db_connection():
    url = os.getenv("mysql://root:DnLawNxZzqsGzPXWSWHLksNGkUtIkqFG@mysql.railway.internal:3306/railway")

    return pymysql.connect(
        host="thomas.proxy.rlwy.net",
        port=58444,
        user="root",
        password="DnLawNxZzqsGzPXWSWHLksNGkUtIkqFG",
        database="railway",
        cursorclass=pymysql.cursors.DictCursor
    )