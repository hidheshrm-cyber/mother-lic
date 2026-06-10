import sqlite3

conn = sqlite3.connect(
    "extracted/licmdb.s3db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
policy_no,
plan_name,
premium,
next_premium,
status,
fupstatus
FROM policies
LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()