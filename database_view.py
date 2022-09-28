import sqlite3

conn = sqlite3.connect("mydata.db")

sql = "SELECT * FROM parsing_site"
cursor = conn.cursor()
cursor.execute(sql)
res = cursor.fetchall()

for r in res:
    print("title:", r[0])
    print("date:", r[1])
    print("url_image:", r[2])
