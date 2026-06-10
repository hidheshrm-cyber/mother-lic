from importer import extract_zip
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/check-login", methods=["POST"])
def check_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "lic123" and password == "lic123":
        return "success"
    else:
        return "failed"
@app.route("/dashboard")
def dashboard():

    import sqlite3

    conn = sqlite3.connect(
        "extracted/licmdb.s3db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM policies"
    )

    total_count = cursor.fetchone()[0]

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

    current_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM policies
    WHERE status IN
    (
    'Lapsed',
    'Lapsed, DGH required'
    )
    """)

    lapsed_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_count=total_count,
        current_count=current_count,
        lapsed_count=lapsed_count
    )

@app.route("/allpolicies")
def allpolicies():

    import sqlite3

    conn = sqlite3.connect(
        "extracted/licmdb.s3db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
    c.name,
    c.mobileno,
    c.dob_r,
    c.age,
    c.address,
    c.street,
    c.city,
    c.state,
    c.email,
    c.occupation,
    c.designation,

    p.policy_no,
    p.premium,
    p.next_premium,
    p.status

FROM policies p

JOIN client c
ON p.familycode = c.familycode
AND p.perscode = c.perscode

    ORDER BY c.name
    """)

    rows = cursor.fetchall()

    conn.close()

    html = """
    <h1>Total Policies</h1>

    <table border='1' cellpadding='10'>
  <tr>
    <th>Name</th>
    <th>Mobile</th>
    <th>DOB</th>
    <th>Age</th>
    <th>Address</th>
    <th>Street</th>
    <th>City</th>
    <th>State</th>
    <th>Email</th>
    <th>Occupation</th>
    <th>Designation</th>
    <th>Policy No</th>
    <th>Premium</th>
    <th>Next Premium Date</th>
    <th>Status</th>
</tr>
    """

    for row in rows:

        html += f"""
        
<tr>
    <td>{row[0]}</td>
    <td>{row[1]}</td>
    <td>{row[2]}</td>
    <td>{row[3]}</td>
    <td>{row[4]}</td>
    <td>{row[5]}</td>
    <td>{row[6]}</td>
    <td>{row[7]}</td>
    <td>{row[8]}</td>
    <td>{row[9]}</td>
    <td>{row[10]}</td>
    <td>{row[11]}</td>
    <td>{row[12]}</td>
    <td>{row[13]}</td>
    <td>{row[14]}</td>
</tr>
"""
        

    html += "</table>"

    return html

@app.route("/current")
def current():

    import sqlite3

    conn = sqlite3.connect("extracted/licmdb.s3db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        c.name,
        c.mobileno,
        c.dob_r,
        c.age,
        c.address,
        c.street,
        c.city,
        c.state,
        c.email,
        c.occupation,
        c.designation,
        p.policy_no,
        p.premium,
        p.next_premium,
        p.status

    FROM policies p

    JOIN client c
      ON p.familycode = c.familycode
     AND p.perscode = c.perscode

    WHERE p.status IN
    (
        'In grace period',
        'Advance Premium',
        'FULLY PAID-UP'
    )

    ORDER BY c.name
    """)

    rows = cursor.fetchall()

    conn.close()

    html = """
    <h1>Current Policies</h1>

    <table border='1' cellpadding='8'>
    <tr>
        <th>Name</th>
        <th>Mobile</th>
        <th>DOB</th>
        <th>Age</th>
        <th>Address</th>
        <th>Street</th>
        <th>City</th>
        <th>State</th>
        <th>Email</th>
        <th>Occupation</th>
        <th>Designation</th>
        <th>Policy No</th>
        <th>Premium</th>
        <th>Next Premium Date</th>
        <th>Status</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row[0] or ''}</td>
            <td>{row[1] or ''}</td>
            <td>{row[2] or ''}</td>
            <td>{row[3] or ''}</td>
            <td>{row[4] or ''}</td>
            <td>{row[5] or ''}</td>
            <td>{row[6] or ''}</td>
            <td>{row[7] or ''}</td>
            <td>{row[8] or ''}</td>
            <td>{row[9] or ''}</td>
            <td>{row[10] or ''}</td>
            <td>{row[11] or ''}</td>
            <td>{row[12] or ''}</td>
            <td>{row[13] or ''}</td>
            <td>{row[14] or ''}</td>
        </tr>
        """

    html += "</table>"

    return html
@app.route("/lapsed")
def lapsed():

    import sqlite3

    conn = sqlite3.connect(
        "extracted/licmdb.s3db"
    )

    cursor = conn.cursor()

    cursor.execute("""
  SELECT
    c.name,
    c.mobileno,
    c.dob_r,
    c.age,
    c.address,
    c.street,
    c.city,
    c.state,
    c.email,
    c.occupation,
    c.designation,

    p.policy_no,
    p.premium,
    p.next_premium,
    p.status

FROM policies p

JOIN client c
ON p.familycode = c.familycode
AND p.perscode = c.perscode

    WHERE p.status IN
    (
        'Lapsed',
        'Lapsed, DGH required'
    )

    ORDER BY c.name
    """)

    rows = cursor.fetchall()

    conn.close()

    html = """
    <h1>Lapsed Policies</h1>

    <table border='1' cellpadding='8'>
    <tr>
    <th>Name</th>
    <th>Mobile</th>
    <th>DOB</th>
    <th>Age</th>
    <th>Address</th>
    <th>Street</th>
    <th>City</th>
    <th>State</th>
    <th>Email</th>
    <th>Occupation</th>
    <th>Designation</th>
    <th>Policy No</th>
    <th>Premium</th>
    <th>Next Premium Date</th>
    <th>Status</th>
</tr>
    """

    for row in rows:
        html += f"""
<tr>
    <td>{row[0]}</td>
    <td>{row[1]}</td>
    <td>{row[2]}</td>
    <td>{row[3]}</td>
    <td>{row[4]}</td>
    <td>{row[5]}</td>
    <td>{row[6]}</td>
    <td>{row[7]}</td>
    <td>{row[8]}</td>
    <td>{row[9]}</td>
    <td>{row[10]}</td>
    <td>{row[11]}</td>
    <td>{row[12]}</td>
    <td>{row[13]}</td>
    <td>{row[14]}</td>
</tr>
"""
        

    html += "</table>"

    return html
@app.route("/search")
def search():

    q = request.args.get("q", "")

    import sqlite3

    conn = sqlite3.connect(
        "extracted/licmdb.s3db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        c.name,
        c.mobileno,
        p.policy_no,
        p.premium,
        p.next_premium,
        p.status

    FROM policies p

    JOIN client c
      ON p.familycode = c.familycode
     AND p.perscode = c.perscode

    WHERE p.status LIKE ?

    ORDER BY c.name
    """, (f"%{q}%",))

    rows = cursor.fetchall()

    conn.close()

    html = f"""
    <h1>Policies Matching '{q}'</h1>

    <table border='1' cellpadding='10'>
    <tr>
        <th>Name</th>
        <th>Mobile</th>
        <th>Policy No</th>
        <th>Premium</th>
        <th>Next Premium</th>
        <th>Status</th>
    </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
            <td>{row[5]}</td>
        </tr>
        """

    html += "</table>"

    return html
UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)
@app.route("/search-status")
def search_status():

    q = request.args.get("q", "")

    import sqlite3

    conn = sqlite3.connect("extracted/licmdb.s3db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        c.name,
        c.mobileno,
        c.dob_r,
        c.age,
        c.address,
        c.street,
        c.city,
        c.state,
        c.email,
        c.occupation,
        c.designation,
        p.policy_no,
        p.premium,
        p.next_premium,
        p.status

    FROM policies p

    JOIN client c
      ON p.familycode = c.familycode
     AND p.perscode = c.perscode

    WHERE p.status LIKE ?

    ORDER BY c.name
    """, (f"%{q}%",))

    rows = cursor.fetchall()

    conn.close()

    html = f"""
    <html>
    <head>
        <title>Status Search</title>
    </head>
    <body>

    <h1>Status Search : {q}</h1>

    <table border="1" cellpadding="8" cellspacing="0">

        <tr>
            <th>Name</th>
            <th>Mobile</th>
            <th>DOB</th>
            <th>Age</th>
            <th>Address</th>
            <th>Street</th>
            <th>City</th>
            <th>State</th>
            <th>Email</th>
            <th>Occupation</th>
            <th>Designation</th>
            <th>Policy No</th>
            <th>Premium</th>
            <th>Next Premium Date</th>
            <th>Status</th>
        </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row[0] or ''}</td>
            <td>{row[1] or ''}</td>
            <td>{row[2] or ''}</td>
            <td>{row[3] or ''}</td>
            <td>{row[4] or ''}</td>
            <td>{row[5] or ''}</td>
            <td>{row[6] or ''}</td>
            <td>{row[7] or ''}</td>
            <td>{row[8] or ''}</td>
            <td>{row[9] or ''}</td>
            <td>{row[10] or ''}</td>
            <td>{row[11] or ''}</td>
            <td>{row[12] or ''}</td>
            <td>{row[13] or ''}</td>
            <td>{row[14] or ''}</td>
        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/dashboard">
        <button>Back To Dashboard</button>
    </a>

    </body>
    </html>
    """

    return html
@app.route("/search-customer")
def search_customer():

    q = request.args.get("q", "")

    import sqlite3

    conn = sqlite3.connect(
        "extracted/licmdb.s3db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        c.name,
        c.mobileno,
        c.dob_r,
        c.age,
        c.address,
        c.street,
        c.city,
        c.state,
        c.email,
        c.occupation,
        c.designation,
        p.policy_no,
        p.premium,
        p.next_premium,
        p.status

    FROM policies p

    JOIN client c
      ON p.familycode = c.familycode
     AND p.perscode = c.perscode

   WHERE
    c.name LIKE ?
    OR c.mobileno LIKE ?
    OR c.dob_r LIKE ?
    OR CAST(c.age AS TEXT) LIKE ?
    OR c.address LIKE ?
    OR c.street LIKE ?
    OR c.city LIKE ?
    OR c.state LIKE ?
    OR c.email LIKE ?
    OR c.occupation LIKE ?
    OR c.designation LIKE ?
    OR CAST(p.policy_no AS TEXT) LIKE ?
    OR CAST(p.premium AS TEXT) LIKE ?
    OR p.next_premium LIKE ?
    OR p.status LIKE ?

    ORDER BY c.name
    """, (
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%",
    f"%{q}%"
))

    rows = cursor.fetchall()

    conn.close()

    html = f"""
    <html>
    <head>
        <title>Customer Search</title>
    </head>
    <body>

    <h1>Search Results : {q}</h1>

    <table border="1" cellpadding="10" cellspacing="0">

        <tr>
            <th>Name</th>
            <th>Mobile</th>
            <th>DOB</th>
            <th>Age</th>
            <th>Address</th>
            <th>Street</th>
            <th>City</th>
            <th>State</th>
            <th>Email</th>
            <th>Occupation</th>
            <th>Designation</th>
            <th>Policy No</th>
            <th>Premium</th>
            <th>Next Premium Date</th>
            <th>Status</th>
        </tr>
    """

    for row in rows:

        html += f"""
        <tr>
            <td>{row[0] or ''}</td>
            <td>{row[1] or ''}</td>
            <td>{row[2] or ''}</td>
            <td>{row[3] or ''}</td>
            <td>{row[4] or ''}</td>
            <td>{row[5] or ''}</td>
            <td>{row[6] or ''}</td>
            <td>{row[7] or ''}</td>
            <td>{row[8] or ''}</td>
            <td>{row[9] or ''}</td>
            <td>{row[10] or ''}</td>
            <td>{row[11] or ''}</td>
            <td>{row[12] or ''}</td>
            <td>{row[13] or ''}</td>
            <td>{row[14] or ''}</td>
        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/dashboard">
        <button>Back To Dashboard</button>
    </a>

    </body>
    </html>
    """

    return html
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["zipfile"]

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        folder = extract_zip(filepath)

        return f"""
        <h2>Upload Successful</h2>

        <p><b>File Name:</b> {file.filename}</p>

        <p><b>Saved To:</b> {filepath}</p>

        <p><b>Extracted To:</b> {folder}</p>
        """

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
