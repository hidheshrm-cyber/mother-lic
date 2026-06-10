import sqlite3

conn = sqlite3.connect("extracted/licmdb.s3db")
cursor = conn.cursor()

cursor.execute("""
SELECT policy_no, next_premium
FROM policies
LIMIT 20
""")

for row in cursor.fetchall():
    print(row)

conn.close()