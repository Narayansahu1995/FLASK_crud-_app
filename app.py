from flask import Flask, redirect, render_template, request,jsonify, url_for,flash,session
import os,re
import db 
from models import School

app = Flask(__name__)
app.secret_key  = os.urandom(24)

if not os.path.isfile("school.db"):
    db.connect()

@app.route('/login')
def login():
    # schools = db.view()
    return render_template('login.html')

@app.route('/index')
def index():
    schools = db.view()
    return render_template('index.html', schools=schools)

def validate_email(email):
    regex = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$')
    if re.fullmatch(regex,email):
        return True
    else:
        return False
    


@app.route('/get_schools/', defaults={'id': None}, methods=['GET'])
@app.route('/get_schools/<int:id>', methods=['GET'])
def get_schools(id):
    schools = db.view()
    if id is None:
        return jsonify([school.serialize() for school in schools])
    else:
        for school in schools:
            if school.id == id:
                return jsonify(school.serialize())
        return jsonify({"error": "School not found"})
    
@app.route('/delete_school/<int:id>', methods=['GET'])
def delete_school(id):
    db.delete(id)
    return redirect(url_for('index'))

@app.route('/add_school', methods=['POST'])
def add_school():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    if validate_email(email):
        sc = School(None,name,address,email)
        db.insert(sc)
        flash("school added successfully")
        return redirect(url_for('index'))
    else:
        return jsonify({"error": "Invalid email"})
    
@app.route('/update_school', methods=['POST'])
def update_school():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    if validate_email(email):
        sc = School(id,name,email,address)
        db.update(sc)
        flash("school updated successfully")
        return redirect(url_for('index'))
    else:
        return jsonify({"error": "Invalid email"})
    
@app.route('/dashboard', methods=['POST'])
def school_login():
    
    email = request.form['email']
    password = request.form['password']

    if validate_email(email):
        school = db.get_school_by_email(email)
        if school and password == password:
            session['logged_in'] = True
            session['school_email'] = school.email
            flash("Login successful")
            return render_template('dashboard.html')
        else:
            flash("Invalid email or password")
            return redirect(url_for('login'))
    else:
        flash("Invalid email format")
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('school_email', None)
    return redirect(url_for('login'))

@app.route('/')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)