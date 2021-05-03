from flask import Flask, flash, render_template, request, redirect, session, url_for
import hashlib
import pymysql
import time
from datetime import date
from pymongo import MongoClient
import dns
import razorpay
import models

app = Flask(__name__)
app.config['SECRET_KEY'] = '8ffe05624dfe0efdf7c7f67288d4f4ce5005e0dfb6a1bc48366ef9906dd0586e'

class base():
	def init():
		pass

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

class user():
	def init():
		pass
	@app.route('/login', methods=['POST'])
	def login():
    	# Parse user input fields
		name=request.form['login_username']
		password=hashlib.sha256(request.form['login_password'].encode('utf-8')).hexdigest()
		error = None
		if name == '' or password == '':
			error = 'Please fill out all the fields.'
			return render_template('login.html', error=error)
		cur=collection.find({'username': name})
		if len(list(cur))==0:
			error = 'Incorrect username or password. Please try again.'
			return render_template('login.html', error=error)

		for x in collection.find({'username': name}):
			if(x['username']=="admin" and x['password']==hashlib.sha256('admin123'.encode('utf-8')).hexdigest()):
				session['username'] = x['username']
				session['email'] = x['email']
				session['is_admin'] = 1
				session['name'] = x["fname"]
				return redirect(url_for('home'))

			else:
				session['username'] = x['username']
				session['email'] = x['email']
				session['is_admin'] = 0
				session['name'] = x["fname"]
				return redirect(url_for('traveller'))

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
		checks=models.check()
		name=request.form['register_username']
		password1=hashlib.sha256(request.form['register_password'].encode('utf-8')).hexdigest()
		password2=hashlib.sha256(request.form['register_password2'].encode('utf-8')).hexdigest()
		firstname=request.form['register_firstname']
		lastname=request.form['register_lastname']
		email=request.form['register_email']
		# Check if all user fields filled in
		if name == '' or password1 == '' or password2 == '' or firstname == '' or lastname == '' or email == '':
			error = 'Please fill out all the fields.'
			return render_template('login.html', error2=error, scroll="register")
	
		chk=checks.check_username(name)
		chk2=checks.check_email(email)
		if chk!=True :
			return render_template('login.html', error2=chk, scroll="register")
		if chk2!=True:
			return render_template('login.html', error2=chk, scroll="register")
		# Check that passwords match
		if password1 != password2:
			error = 'Passwords do not match.'
			return render_template('login.html', error2=error, scroll="register")
	
		x=collection.find({"email":email})
		for i in x:
			if i["email"]==email:
				error = 'You have already registered with this email, PLease login instead'
				return render_template('login.html', error2=error, scroll="register")
		
		x=collection.find({"email":email})
		for i in x:
			if i["username"]==name:
				error = 'You have already registered with this username, PLease login instead'
				return render_template('login.html', error2=error, scroll="register")
		collection.insert_one({"username":name,"fname":firstname,"password":password1,"email":email})
	
		# Update current user session
		session['username'] = name
		session['name'] = firstname
		session['is_admin'] = 0
		session['email'] = email
	
		return redirect(url_for('home'))

class traveling():
	def init():
		pass

	@app.route('/traveller',methods=['POST','GET'])
	def traveller():
		error=None
		travel=models.details(collection2,session['username'])
		show=travel.view_details()
		if request.method == 'POST':
			loca = request.form["loc"]
			num = request.form["num_tr"]
			bud = request.form["budg"]
			if loca == '' or num == '' or bud == '':
				error = 'Please fill out all the fields.'
				return render_template('traveller.html',items=show, error=error,)
			x=collection2.find({"username":session['username']})
			for i in x:
				if i['username']==session['username']:
					error="You have already entered traveller details,edit instead"
					return render_template('traveller.html', items=show,error=error)
			travel.insert_details(loca,num,bud)
			return redirect(url_for('traveller'))		
		else:
			return render_template('traveller.html',items=show)
	
	@app.route('/delete')
	def delete():
		error=None
		travel=models.details(collection2,session['username'])
		x=collection2.find({"username":session['username']})
		for i in x:
			if i['username']==session['username']:
				travel.delete_details()
		return redirect(url_for('traveller'))
	
	@app.route('/edit', methods=['GET', 'POST'])
	def edit():
		travel=models.details(collection2,session['username'])
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
		return 	redirect(url_for('details'))

class hotelsstuff():
	def init():
		pass
	@app.route('/hotels')
	def hotels():
		return render_template('hotels.html')
	
	@app.route('/tourism')
	def tourism():
		return render_template('tourism.html')

	@app.route('/details')
	def details():
		return render_template('details.html')

	@app.route('/travel')
	def travel():
		return render_template('travel.html')

class feedbacks():
	def init():
		pass
	@app.route('/feedback',methods=['POST','GET'])
	def feedback():
		error=None
		feedb=models.feed(collection3,session['username'])
		email=models.mail()
		x=feedb.view_details()
		if request.method=='POST':
			sub = request.form["sub"]
			con = request.form["con"]
			if sub == '' or con == '':
				error = 'Please fill out both fields.'
				return render_template('feedback.html', items=x,error=error)
			c=collection3.find({"username":session['username'],"subject":sub,"desc":con})
			if len(list(c))!=0:
				error="Same Feedback cannot be submitted"
				return render_template('feedback.html',items=x,error=error)
			feedb.insert_details(sub,con)
			email.send_email(session['username'],session['email'],sub,con)
			x=feedb.view_details()
			return render_template('feedback.html',items=x)
		else:	
			return render_template('feedback.html', items=x)

class payments():
	def init():
		pass
	@app.route('/pay',methods=['POST','GET'])
	def pay():
		client=razorpay.Client(auth=('rzp_test_W0iJf3S2txqRlO','4Oxi0f4A331AlQJchqWLQxfD'))
		payment=client.order.create({'amount':500,'currency':'INR','payment_capture':'1'})
		return render_template('pay.html',payment=payment)
	
	@app.route('/success',methods=['POST','GET'])
	def success():
		return render_template('success.html')



# Run the application
if __name__ == '__main__':
	client=MongoClient("ADD_YOUR_MONGOATLAS_USERNAME_AND_PASSWORD")
	collection = client.user.project
	collection2=client.user.deets
	collection3=client.user.feedback
	app.run(debug=True)
