import sqlite3

conn = sqlite3.connect("extracted/licmdb.s3db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM policies")
print("Total Policies:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(*)
FROM policies
WHERE status IN
(
'In grace period',
'Advance Premium',
'FULLY PAID-UP'
)
""")
print("Current Policies:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(*)
FROM policies
WHERE status IN
(
'Lapsed',
'Lapsed, DGH required'
)
""")
print("Lapsed Policies:", cursor.fetchone()[0])

conn.close()