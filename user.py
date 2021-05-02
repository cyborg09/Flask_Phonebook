from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'random string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    company_name = db.Column(db.String(400),nullable=False)
    First_Name = db.Column(db.String(200), nullable=False)
    Last_name = db.Column(db.String(200), nullable=False)
    Phone = db.Column(db.Integer(), nullable=False)
    Email = db.Column(db.String(200), nullable=False)
    Address = db.Column(db.String(200), nullable=False)
    City = db.Column(db.String(200), nullable=False)
    District = db.Column(db.String(200), nullable=False)
    State = db.Column(db.String(200), nullable=False)
    Pincode = db.Column(db.Integer(), nullable=False)
    gstin = db.Column(db.Integer(), nullable=False)
    pwd = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.id

@app.route('/insert', methods=['POST','GET'])
def insert():
    if request.method == 'POST':
        com_name = request.form['company_name']
        fname = request.form['first_name']
        lname = request.form['last_name']
        phone = request.form['Phone']
        email = request.form['Email']
        addr = request.form['Address']
        city = request.form['City']
        dst = request.form['District']
        state = request.form['State']
        pincode = request.form['pincode']
        gstin = request.form['gstin']
        pwd = request.form['pwd']
        new_user = User(company_name=com_name,First_Name=fname,Last_name=lname,Phone=phone,Email=email,Address=addr,City=city,District=dst,State=state,Pincode=pincode,gstin=gstin,pwd=pwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue in insertion"
    else:
        return render_template('insert.html')

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        search = request.form['search']
        users = User.query.filter_by(company_name=search).all()
        return render_template('index.html', users=users)
    else:
        users = User.query.order_by(User.id).all()
        return render_template('index.html',users=users)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error in deletion"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    user = User.query.get_or_404(id)
    if request.method =='POST':
        user.company_name = request.form['company_name']
        user.First_Name = request.form['first_name']
        user.Last_name = request.form['last_name']
        user.Phone = request.form['Phone']
        user.Email = request.form['Email']
        user.Address = request.form['Address']
        user.City = request.form['City']
        user.District = request.form['District']
        user.State = request.form['State']
        user.Pincode = request.form['pincode']
        user.gstin = request.form['gstin']
        user.pwd = request.form['pwd']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue in Insertion"
    else:
        return render_template('update.html',user=user)


if __name__ == "__main__":
    app.run(debug=True)