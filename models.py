from db import db

class Txt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    my_blob = db.Column(db.BLOB)

