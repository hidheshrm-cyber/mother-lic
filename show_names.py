import sqlite3

conn = sqlite3.connect(
    "extracted/licmdb.s3db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
name,
mobileno,
city
FROM client
LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()