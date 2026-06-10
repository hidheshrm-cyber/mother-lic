# check_statuses.py

import sqlite3

conn = sqlite3.connect("extracted/licmdb.s3db")
cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT status
FROM policies
ORDER BY status
""")

for row in cursor.fetchall():
    print(row[0])

conn.close()