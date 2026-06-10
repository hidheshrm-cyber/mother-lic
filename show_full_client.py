import sqlite3

conn = sqlite3.connect("extracted/licmdb.s3db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    name,
    mobileno,
    dob_r,
    age,
    address,
    street,
    city,
    state,
    email,
    occupation,
    designation
FROM client
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()