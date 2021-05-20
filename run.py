# import re
from flask import Flask  
from flask import render_template,url_for,flash,redirect,request,Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,current_user,logout_user
from flask_login import UserMixin
from email.message import EmailMessage
import smtplib
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = 'bdbe7e1621612f790a6c829de37379a5'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
login_manger=LoginManager(app)
login_manger.login_view = 'login'

@login_manger.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

class User(db.Model,UserMixin):
     id = db.Column(db.Integer ,primary_key=True)
     username = db.Column(db.String(20),unique=True,nullable=False)
     email = db.Column(db.String(120),unique=True,nullable=False)
     image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
     

     def __repr__(self):
          return f"User('{self.username}','{self.email}','{self.image_file}')"


# from models import User
@app.route('/') 
def home():  
    return render_template('home.html');  

@app.route('/register',methods=['POST','GET']) 
def register():  
	if(request.method == 'POST'):
		print(request.form)
		print(request.form.get("name"))
		user =User(username=request.form.get("name"),email=request.form.get("email"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html');  

@app.route('/login',methods=["POST","GET"]) 
def login():
	if request.method=="POST":
		print(request.form)
		user=User.query.filter_by(email= request.form.get('email')).first()
		print(user)
		login_user(user)
		return redirect(url_for('hotel'))
	return render_template('login.html')
    
def verfieddoc(rec,html):
     EMAIL_ADDRESS= os.environ.get('EMAIL_NAME')               
     EMAIL_PASSWORD=   "" #os.environ('EMAIL_PASS')                                       
     subject='Application Status'
     msg=EmailMessage()
     msg['Subject']=subject
     msg['From']=EMAIL_ADDRESS
     msg['Bcc']=rec
     msg.add_alternative(html, subtype='html')
     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
          smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
          smtp.send_message(msg)

  
  
Hotel= [{ "name" : "Bala'sHotel", "rating" : 4.3, "place" : "South Indian", "timings" : "10Am to 7Pm", "mintime" : 45, "image_file" : "parivar.jpg" }]
Dish=[{  "dishname" : "Chicken ", "rating" : 4.3, "price" : 299, "description" : "Biryani, also known as biriyani, biriani, birani or briyani, is a mixed rice dish with its origins among the Muslims of the Indian subcontinent.", "hotel" : "BalasHotel", "proteins" : 25, "carbohydrates" : 30, "fat" : 20, "image_file" : "chicken.jpg","times":1 }]
@app.route('/hotel') 
def hotel():  
	print(Hotel)
	return render_template('hotel.html',data=Hotel); 

@app.route('/dish') 
def dish():  
	print(Hotel)
	return render_template('dishes.html',data=Dish); 


ucart=[]
@app.route('/addtocart',methods=["POST"]) 
def cart():
	global ucart
	ucart.append(Dish[0])
	flash('Dish add to cart','success')
	return redirect(url_for('dish')) 


@app.route('/cart') 
def usercart():
	global ucart
	data=ucart
	return render_template('cart.html',data=ucart) 


@app.route('/buy',methods=["POST","GET"]) 
def buy():
	html="""<table>
  <tr>
    <th>Dish</th>
    <th>count</th>
    <th>price</th>
  </tr>
  """
	cost=0
	global ucart
	for i in ucart:
		html+=f"""<tr><td>{i["dishname"]}</td><td>{i["times"]}</td><td>{i["price"]}</td></tr> """
		cost+=i['price']
	html+=f"""<tr><td>GST</td><td>2%</td><td>{cost*0.02}</td></tr>"""
	cost+=cost*0.02
	html+=f"""<tr><td>Total</td><td>=</td><td>{cost}</td></tr>"""

	verfieddoc('balapavankumar333@gmail.com',html)
	return render_template('buy.html',data=Markup(html)); 

@app.route('/logout')
def logout():

     logout_user()
     return redirect(url_for('home'))

@app.route('/account') 
def account():  
    return render_template('account.html'); 


if __name__ =='__main__':  
    app.run(debug = True)