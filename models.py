from database import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200))
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(200))
    address = db.Column(db.Text)

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('customer.id')
    )

    policy_no = db.Column(db.String(100))

    plan = db.Column(db.String(100))

    premium = db.Column(db.Float)

    sumass = db.Column(db.Float)

    nominee = db.Column(db.String(200))

    nextprem = db.Column(db.String(50))

    maturity = db.Column(db.String(50))

    status = db.Column(db.String(100))