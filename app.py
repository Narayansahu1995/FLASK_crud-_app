from flask import Flask, redirect, render_template, request,jsonify, url_for,flash
import os,re
import db 
from models import School

app = Flask(__name__)
app.secret_key  = os.urandom(24)

if not os.path.isfile("school.db"):
    db.connect()

@app.route('/')
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
        sc = School(None,name,email,address)
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



if __name__ == '__main__':
    app.run(debug=True)