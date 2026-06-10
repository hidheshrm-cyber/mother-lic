import sqlite3

conn = sqlite3.connect(
    "extracted/licmdb.s3db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
c.name,
p.policy_no,
p.premium,
p.status

FROM policies p

JOIN client c
ON p.familycode = c.familycode
AND p.perscode = c.perscode

LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()