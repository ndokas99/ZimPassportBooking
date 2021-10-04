from flask import render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import OperationalError
from models import *
from os import path
from datetime import datetime, timedelta


@app.route('/')
def index():
    session['state'] = 'logged out'
    return render_template('index.html')


@app.route('/signup')
def signup():
    session['state'] = 'logged out'
    return render_template('signup.html')


@app.route('/login')
def login():
    session['state'] = 'logged out'
    return render_template('login.html')


@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        idNum = request.form['idNum']
        idNum = idNum.replace(" ", "").replace("-", "")
        fullname = request.form['fullName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if len(idNum) < 9:
            flash("ID number is invalid", category="error")
        elif Account.query.filter_by(id=idNum).first():
            flash("Account with this ID already exists", category='error')
        elif fullname.count(" ") < 1:
            flash("Fullname should contain at least two words", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 7:
            flash("Passwords should be at least 7 characters", category="error")
        else:
            acc = Account(
                id=idNum,
                fullname=fullname,
                password=generate_password_hash(password1, method="sha256")
            )
            db.session.add(acc)
            db.session.commit()
            flash("Account created successfully.", category="success")
            print('hello')
            return render_template('login.html')

        return render_template('signup.html')


@app.route('/apply', methods=['POST'])
def apply():
    if request.method == 'POST':
        idNum = request.form['idNum']
        idNum = idNum.replace(" ", "").replace("-", "")
        password = request.form['password']

        acc = Account.query.filter_by(id=idNum).first()
        if acc:
            if check_password_hash(acc.password, password):
                session['state'] = "logged in"
                return render_template("application_form.html")
            else:
                flash("Account does not exist", category="error")
        else:
            flash("Account does not exist", category="error")

        return render_template("login.html")


@app.route('/booking', methods=['POST'])
def book():
    if session == 'logged out':
        return render_template('login.html')
    else:
        if request.method == 'POST':
            session['id'] = request.form['id'].replace(" ", "").replace("-", "")
            personal = Personal(
                id=session['id'],
                birth_entry_no=request.form['ben'],
                surname=request.form['surname'],
                other_names=request.form['other_names'],
                maiden_name=request.form['maiden_name'],
                name_changed=request.form['name_changed'],
                details=request.form['details'],
                sex=request.form['sex'],
                marital_status=request.form['marital_status'],
                dob=request.form['dob'],
                place_of_birth=request.form['pob'],
                country_of_birth=request.form['cob'],
                height=request.form['height'],
                colour_of_eyes=request.form['coe'],
                colour_of_hair=request.form['coh'],
                peculiarities=request.form['pecs'],
                profession=request.form['prof'],
                address=request.form['res'],
                perm_residence=request.form['copr'],
                telephone=request.form['tel']
            )
            db.session.add(personal)

            mdetails = Woman_marriage_details(
                id=session['id'],
                date_of_marriage=request.form['dom'] or None,
                husband_name=request.form['hfn'] or None,
                place_married=request.form['pcm'] or None,
                husbands_place=request.form['hpcb'] or None,
                husband_citizenship=request.form['hc'] or None,
                marr_or_div_number=request.form['mdon'] or None,
                married_more=request.form['mmto'] or None
            )
            db.session.add(mdetails)

            kin = Kin(
                id=session['id'],
                kin_name=request.form['kfn'],
                kin_relation=request.form['krta'],
                kin_address=request.form['kra'],
                kin_telephone=request.form['ktel']
            )
            db.session.add(kin)

            citizenship = Citizenship(
                id=session['id'],
                citizen_by=request.form['citizen_by'],
                issued_document_before=request.form['idb'],
                documents_number=request.form['ipn'] or None,
                holding_foreign=request.form['hfp'],
                foreign_number=request.form['fpn'] or None,
                renounce_foreign=request.form['rfb'],
                surrender_foreign=request.form['sfp'],
                surrendered_number=request.form['sfpn'] or None,
                date=request.form['ddate']
            )
            db.session.add(citizenship)

            guardian = Guardian(
                id=session['id'],
                guardian_name=request.form['gfn'] or None,
                guardian_id=request.form['gid'] or None,
                relation=request.form['grtc'] or None,
                date=request.form['gdate'] or None
            )
            db.session.add(guardian)

            lost = Lost_passport(
                id=session['id'],
                lost_passport_no=request.form['lspn'] or None,
                issued_at=request.form['lsit'] or None,
                issued_date=request.form['lsid'] or None,
                bearer_name=request.form['lsfn'] or None,
                reason=request.form['lsreason'] or None
            )
            db.session.add(lost)

            prev = Previous_marriage(
                id=session['id'],
                details=request.form['prev_details'] or None
            )
            db.session.add(prev)

            docs = Documents(
                id=session['id'],
                bcert=request.files['bcert'].stream.read(),
                nid=request.files['nat_id'].stream.read(),
                fnid=request.files['fnid'].stream.read()
            )
            db.session.add(docs)
            db.session.commit()

            return render_template('booking.html')


@app.route('/confirmation', methods=['POST'])
def confirm():
    if session['state'] == 'logged out':
        return render_template('login.html')
    else:
        if request.method == "POST":
            now = datetime.now()
            if request.form['period'] == '24hrs':
                date = now + timedelta(days=1)
            elif request.form['period'] == '3days':
                date = now + timedelta(days=3)
            else:
                date = now + timedelta(days=91)

            booking = Booking(
                id=session['id'],
                release=request.form['period'],
                date=date.date(),
                pay_id=request.form['pay_id']
            )
            db.session.add(booking)
            db.session.commit()

            return render_template('confirmation.html', date=date)


def create_database():
    if not path.exists("citizens.db"):
        try:
            db.create_all(app=app)
        except OperationalError:
            pass


create_database()


if __name__ == '__main__':
    app.run('0.0.0.0')
