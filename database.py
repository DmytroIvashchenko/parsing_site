import sqlite3

conn = sqlite3.connect("mydata.db")

sql = "CREATE TABLE parsing_site (title TEXT, date TEXT, url_image TEXT)"

cursor = conn.cursor()
cursor.execute(sql)


conn.close()
