from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_wtf import Form
from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
import hashlib
import locale
import pymysql
import time
from pymongo import MongoClient
import dns
app = Flask(__name__)
app.config['SECRET_KEY'] = '8ffe05624dfe0efdf7c7f67288d4f4ce5005e0dfb6a1bc48366ef9906dd0586e'


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/home')
def home():

	# Disallow unlogged in users from requesting homepage.
	if 'username' not in session or session['username'] == '':
		return redirect(url_for('index'))

	return redirect(url_for('traveller'))

@app.route('/login-page')
def login_page():

	# Show login page if not logged in. Redirect to home if already logged in.
	if 'username' not in session or session['username'] == '':
		return render_template('login.html')
	else:
		return redirect(url_for('traveller'))

@app.route('/login', methods=['POST'])
def verify_credentials():
    # Parse user input fields
    name=request.form['login_username']
    password=hashlib.sha256(request.form['login_password'].encode('utf-8')).hexdigest()
    error = None
    for x in collection.find():
        if(x['username']=="admin" and x['password']==hashlib.sha256('admin123'.encode('utf-8')).hexdigest()):
            session['username'] = x['username']
            session['email'] = x['email']
            session['is_admin'] = 1
            session['name'] = x["fname"]
            return redirect(url_for('home'))
        elif(x['username']==name and x['password']==password):
            session['username'] = x['username']
            session['email'] = x['email']
            session['is_admin'] = 0
            session['name'] = x["fname"]
            return redirect(url_for('traveller'))
        else:
            error = 'Incorrect username or password. Please try again.'
            return render_template('login.html', error=error)
            
@app.route('/logout')
def logout():

	# Clear out session variables
	session.clear()
	return redirect(url_for('index'))

# On Register Form Submit. Loads home page.
# TODO: Re-fill out correct fields when registration fails.
@app.route('/register', methods=['POST'])
def register():

	# Parse user input fields
	name=request.form['register_username']
	password1=hashlib.sha256(request.form['register_password'].encode('utf-8')).hexdigest()
	password2=hashlib.sha256(request.form['register_password2'].encode('utf-8')).hexdigest()
	firstname=request.form['register_firstname']
	lastname=request.form['register_lastname']
	email=request.form['register_email']
	# Check if all user fields filled in
	if name == '' or password1 == '' or password2 == '' or firstname == '' or firstname == '' or lastname == '' or email == '':
		error = 'Please fill out all the fields.'
		return render_template('login.html', error2=error, scroll="register")

	# Check that passwords match
	if password1 != password2:
		error = 'Passwords do not match.'
		return render_template('login.html', error2=error, scroll="register")

	x=collection.find({"email":email})
	for i in x:
		if i["email"]==email:
			error = 'You have already registered, PLease login instead'
			return render_template('login.html', error2=error, scroll="register")
	collection.insert_one({"username":name,"fname":firstname,"password":password1,"email":email})
    
	# Update current user session
	session['username'] = name
	session['name'] = firstname
	session['is_admin'] = 0
	session['email'] = email

	return redirect(url_for('home'))

class details():
	def __init__(self, u_name):
		self.uname =u_name

	def insert_details(self,source_loc,num_people,budget):
		budget=int(budget)
		collection2.insert_one({"username":self.uname,"source":source_loc,"budget":budget,"travellers":num_people})
    
	def view_details(self):
		i=collection2.find({"username":self.uname})
		return i
	
	def delete_details(self):
		collection2.delete_one({"username":self.uname})
		return
	
	def update_details(self,source_loc,num_people,budget):
		budget=int(budget)
		collection2.update({"username":self.uname},{"username":self.uname,"source":source_loc,"budget":budget,"travellers":num_people})

@app.route('/traveller',methods=['POST','GET'])
def traveller():
	error=None
	travel=details(session['username'])
	if request.method == 'POST':
		loca = request.form["loc"]
		num = request.form["num_tr"]
		bud = request.form["budg"]
		if loca == '' or num == '' or bud == '':
			error = 'Please fill out all the fields.'
			return render_template('traveller.html', error=error, scroll="register")
		x=collection2.find({"username":session['username']})
		for i in x:
			if i['username']==session['username']:
				error="You have already entered traveller details,edit instead"
				show=travel.view_details()
				return render_template('traveller.html', error=error)
		travel.insert_details(loca,num,bud)
		return redirect(url_for('traveller'))		
	else:
		show=travel.view_details()
		return render_template('traveller.html',items=show)

@app.route('/delete')
def delete():
	error=None
	travel=details(session['username'])
	x=collection2.find({"username":session['username']})
	for i in x:
		if i['username']==session['username']:
			travel.delete_details()
	return redirect(url_for('traveller'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	travel=details(session['username'])
	show=travel.view_details()
	if request.method == 'POST':
		loca = request.form["loc"]
		num = request.form["num_tr"]
		bud = request.form["budg"]
 
		try:
			travel.update_details(loca,num,bud)
			return redirect(url_for('traveller'))
		except:
			return 'There was an issue updating your task'
	else:
		return render_template('edit.html', items=show)

@app.route('/detail')
def detail():
	x=collection2.find({"username":session['username']})
	error=None
	if len(list(x))==0:
		return redirect(url_for('traveller'))
	return 	redirect(url_for('reviews'))

@app.route('/review')
def reviews():

	# Lists a user's visited attractions with a "Review" button.
	cursor = db.cursor()
	query = view_completed_attractions_query()
	cursor.execute(query)
	attractions = [dict(date=row[0], name=row[1], description=row[2]) for row in cursor.fetchall()]
	return render_template('review.html', items=attractions, session=session)


# Run the application
if __name__ == '__main__':

	# Note: If your database uses a different password, enter it here.
	db_pass = 'master@4123'
	client=MongoClient("mongodb+srv://admin-Ayush:vSYzh9RDkmZ8dr0t@cluster0.llgkb.mongodb.net/user?retryWrites=true&w=majority")
	collection = client.user.project
	collection2=client.user.deets
	# Make sure your database is started before running run.py
	db_name = 'team1'
	db = pymysql.connect(host='localhost', user='root', passwd=db_pass, db=db_name)
	app.run(debug=True)
	db.close()