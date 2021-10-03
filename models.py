from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class App(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.debug = True
        self.config.update({
            "SECRET_KEY": 'HGR85NG75BF84NG85BG95NF9',
            "SQLALCHEMY_DATABASE_URI": 'sqlite:///citizens.db',
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        })


app = App(__name__)
db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Text, primary_key=True)
    fullname = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


class Booking(db.Model):
    id = db.Column(db.Text, primary_key=True)
    release = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    pay_id = db.Column(db.Text, nullable=False)


class Personal(db.Model):
    id = db.Column(db.Text, primary_key=True)
    birth_entry_no = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    other_names = db.Column(db.Text, nullable=True)
    maiden_name = db.Column(db.Text, nullable=True)
    name_changed = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=True)
    sex = db.Column(db.Text, nullable=False)
    marital_status = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Text, nullable=False)
    place_of_birth = db.Column(db.Text, nullable=False)
    country_of_birth = db.Column(db.Text, nullable=False)

    height = db.Column(db.Text, nullable=False)
    colour_of_eyes = db.Column(db.Text, nullable=False)
    colour_of_hair = db.Column(db.Text, nullable=False)
    peculiarities = db.Column(db.Text, nullable=True)
    profession = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    perm_residence = db.Column(db.Text, nullable=False)
    telephone = db.Column(db.Text, nullable=False)
    db.relationship('Woman_marriage_details')
    db.relationship('Kin')
    db.relationship('Citizenship')
    db.relationship('Guardian')
    db.relationship('Lost_passport')
    db.relationship('Previous_marriage')
    db.relationship('Documents')


class Woman_marriage_details(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    date_of_marriage = db.Column(db.Text, nullable=True)
    husband_name = db.Column(db.Text, nullable=True)
    place_married = db.Column(db.Text, nullable=True)
    husbands_place = db.Column(db.Text, nullable=True)
    husband_citizenship = db.Column(db.Text, nullable=True)
    marr_or_div_number = db.Column(db.Text, nullable=True)
    married_more = db.Column(db.Text, nullable=True)


class Kin(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    kin_name = db.Column(db.Text, nullable=False)
    kin_relation = db.Column(db.Text, nullable=False)
    kin_address = db.Column(db.Text, nullable=False)
    kin_telephone = db.Column(db.Text, nullable=False)


class Citizenship(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    citizen_by = db.Column(db.Text, nullable=False)
    issued_document_before = db.Column(db.Text, nullable=False)
    documents_number = db.Column(db.Text, nullable=True)
    holding_foreign = db.Column(db.Text, nullable=False)
    foreign_number = db.Column(db.Text, nullable=True)
    renounce_foreign = db.Column(db.Text, nullable=False)
    surrender_foreign = db.Column(db.Text, nullable=False)
    surrendered_number = db.Column(db.Text, nullable=True)
    date = db.Column(db.Text, nullable=False)


class Guardian(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    guardian_name = db.Column(db.Text, nullable=True)
    guardian_id = db.Column(db.Text, nullable=True)
    relation = db.Column(db.Text, nullable=True)
    date = db.Column(db.Text, nullable=True)


class Lost_passport(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    lost_passport_no = db.Column(db.Integer, nullable=True)
    issued_at = db.Column(db.Text, nullable=True)
    issued_date = db.Column(db.Text, nullable=True)
    bearer_name = db.Column(db.Text, nullable=True)
    reason = db.Column(db.Text, nullable=True)


class Previous_marriage(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    details = db.Column(db.Text, nullable=True)


class Documents(db.Model):
    id = db.Column(db.Text, db.ForeignKey('personal.id'), primary_key=True)
    bcert = db.Column(db.BLOB, nullable=False)
    nid = db.Column(db.BLOB, nullable=False)
    fnid = db.Column(db.BLOB, nullable=False)
