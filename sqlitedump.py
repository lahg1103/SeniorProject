import sqlite3

conn = sqlite3.connect('instance/voyage.db')
for line in conn.iterdump():
    print(f"{line}\n")
conn.close()