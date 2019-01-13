from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sq1database_setup import Base,Menu,Cart,Account,Order
import razorpay
from random import randint
import datetime
import pyqrcode

app = Flask(__name__,static_url_path='/static')
engine = create_engine('sqlite:///square1.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

session_login=False
userid=' '
useroll=0
date=' '

@app.route('/',methods=['GET','POST'])
def home():
	global session_login
	global userid
	if  session_login==False:
		return render_template('Login.html')
	elif session_login==True:
		all_item=session.query(Cart).filter_by(roll_no=useroll)
		count=all_item.count()
		return render_template('indexS.html',userid=userid,count=count)

	



@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method=='POST' and str(request.form['password'])==str(request.form['cpassword']):

			newaccount=Account(roll_no=int(request.form['roll']),name=str(request.form['fname']),email_id=str(request.form['email']),password=str(request.form['password']),balance=int(0))
			session.add(newaccount)
			session.commit()
			return 'Thanks for Registeration.Now Kindly Login to your Account'

	return 'Password not  match'	



@app.route('/login',methods=['GET','POST'])
def login():
	global session_login
	global userid
	global useroll
	if request.method=='POST':
		useroll=int(request.form['roll'])
		if session.query(Account).filter_by(roll_no=int(request.form['roll'])).count()!=0:
			loggedin=session.query(Account).filter_by(roll_no=int(request.form['roll'])).one()
			if str(request.form['password'])==loggedin.password:
				session_login=True
				#session.query(Cart).delete()
				userid=str(loggedin.name)
				useroll=int(loggedin.roll_no)
				all_item=session.query(Cart).filter_by(roll_no=useroll)
				count=all_item.count()
				return render_template('indexS.html',userid=userid,count=count)
			else:
				return 'Password Did not matched,Kindly Relogin'
		else:
			return 'No Record Found'
	


@app.route('/menu', methods=['GET', 'POST'])
def add_cart():
	global session_login
	global userid
	global useroll
	if request.method=='POST':
		if session_login==True:
			item_cart=session.query(Cart).filter_by(product_id=str(request.form['pid']))
			if item_cart.count()==0:
				item_added=session.query(Menu).filter_by(product_id=str(request.form['pid'])).one()
				cartt=Cart(product_id=str(item_added.product_id),product_name=str(item_added.product_name),product_price=int(item_added.product_price),
					product_image=str(item_added.product_image),product_quantity=int(1),roll_no=useroll)
				session.add(cartt)
				session.commit()
				return 'ok'
	elif request.method=='GET':
		if session_login==True:
			all_item=session.query(Cart).filter_by(roll_no=useroll)
			count=all_item.count()
			return render_template('squareone.html',userid=userid,count=count)
		elif session_login==False:
			return 'Login Kar Le Pahle'
	return 'ok'

		
@app.route('/removeFromCart',methods=['GET', 'POST'])
def remove_cart():
	global session_login
	global userid
	global useroll
	if request.method=='POST':
		if session_login==True:
			item_cart=session.query(Cart).filter_by(product_id=str(request.form['pid']))
			if item_cart.count()!=0:
				item_cart=session.query(Cart).filter_by(product_id=str(request.form['pid'])).one()
				session.delete(item_cart)
				session.commit()
				return 'hi'
	return 'ok'





@app.route('/cart', methods=['GET', 'POST'])
def checkout():
	global session_login
	global userid
	global useroll
	if request.method=='GET':
		if session_login==True:
			all_item=session.query(Cart).filter_by(roll_no=useroll)
			count=all_item.count()
			return render_template('cartt.html',items=all_item,userid=userid,count=count)
		elif session_login==False:
			return 'Login Kar Le Pahle'
	elif request.method=='POST' and session_login==True:
		quantity=request.get_json()
		Quant=quantity['x']
		i=0
		all_item=session.query(Cart).filter_by(roll_no=useroll)
		for item in all_item:
			item.product_quantity=int(Quant[i])
			session.add(item)
			session.commit()
			i+=1
		return jsonify(message='SUCCESSFUL')






@app.route('/logout',methods=['GET','POST'])
def logout():
	global session_login
	global userid
	if session_login==True:
		#session.query(Cart).delete()
		session_login=False
		return render_template('Login.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
	global session_login
	global userid
	global useroll
	if request.method=='GET' and session_login==True:
		logged_user=session.query(Account).filter_by(roll_no=useroll).one()
		#current_balance=logged_user.balance
		all_item=session.query(Cart).filter_by(roll_no=useroll)
		count=all_item.count()
		return render_template('profile.html',userid=userid,user=logged_user,count=count)
	elif request.method=='GET' and session_login==False:
		return 'Login Kar Le Pahle'
	elif request.method=='POST':
		logged_user=session.query(Account).filter_by(roll_no=useroll).one()
		logged_user.balance+=int(request.form['balance'])
		session.add(logged_user)
		session.commit()
		return 'ok'


@app.route('/paywithwallet',methods=['GET','POST'])
def pay():
	global session_login
	global userid
	global useroll
	if request.method=='POST' and session_login==True:
		logged_user=session.query(Account).filter_by(roll_no=useroll).one()
		if logged_user.balance<request.form['debit']:
			return jsonify(message='TRANSACTION UNSUCCESSFUL')
		else:
			logged_user.balance-=int(request.form['debit'])
			session.add(logged_user)
			session.commit()
			return jsonify(message='TRANSACTION SUCCESSFUL')


@app.route('/rechargewallet',methods=['GET','POST'])
def recharge():
	global session_login
	global userid
	global useroll
	if request.method=='POST' and session_login==True:
		logged_user=session.query(Account).filter_by(roll_no=useroll).one()
		logged_user.balance+=int(request.form['credit'])
		session.add(logged_user)
		session.commit()
		return jsonify(message='BALANCE UPDATED')


@app.route('/invoicegenerate',methods=['GET','POST'])
def invoice():
	global session_login
	global userid
	global useroll
	global date
	if request.method=='POST' and session_login==True:
		orderid=randint(10**5, (10**6)-1)
		date=str(datetime.date.today())
		all_item=session.query(Cart).filter_by(roll_no=useroll)
		for item in all_item:
			bill=Order(order_id=int(orderid),invoice_date=date,invoice_valid=date,roll_no=useroll,name=userid,
				product_name=item.product_name,product_price=item.product_price,product_quantity=item.product_quantity,product_id=item.product_id,
				strikethrough='No')
			session.add(bill)
			session.commit()
		session.query(Cart).filter_by(roll_no=useroll).delete()
		return jsonify(message=str(orderid))

@app.route('/invoice/<int:orderid>',methods=['GET','POST'])
def displayinvoice(orderid):
	name=' '
	uroll=0
	date=' '

	if request.method=='GET':
		order_details=session.query(Order).filter_by(order_id=orderid)
		#orderr=order_details.one()
		total=0
		for odr in order_details:
			total+=(odr.product_quantity*odr.product_price)
			name=odr.name
			uroll=odr.roll_no
			date=odr.invoice_date
		tax=0.05*total
		tot=total+tax
		return render_template('invoice.html',subtotal=total,tax=tax,total=tot,order=order_details,name=name,roll=uroll,orderid=orderid,date=date)
	elif request.method=='POST':
		order_details=session.query(Order).filter_by(order_id=int(request.form['orderid']))
		for order in order_details:
			if order.product_id==str(request.form['pid']):
				order.strikethrough='Yes'
				session.add(order)
				session.commit()
	return 'ok'


@app.route('/passupdate',methods=['GET','POST'])
def updatepassword():
	global session_login
	global userid
	global useroll
	opass=' '
	if request.method=='POST' and session_login==True:
		logged_user=session.query(Account).filter_by(roll_no=useroll).one()
		if str(request.form['opassword'])==logged_user.password:
			if str(request.form['password'])==str(request.form['cpassword']):

				logged_user.password=request.form['npass']
				session.add(logged_user)
				session.commit()
				return 'Password updated'
			else:
				return 'Password not match'
		else:
			return 'Old password wrong'


@app.route('/deleteaccount',methods=['GET','POST'])
def deleteaccount():
	global session_login
	global userid
	global useroll
	if request.method=='POST' and session_login==True:
		logged_user=session.query(Account).filter_by(roll_no=useroll).one()
		session.delete(logged_user)
		session_login=False
		return jsonify(message='deleted')
	return jsonify(message='login karle')


@app.route('/generateqrcode',methods=['GET','POST'])
def qrcode():
	global session_login
	global userid
	global useroll
	if request.method=='POST' and session_login==True:
		orderid=int(request.form['order'])
		Url='http://localhost:5000/invoice/'+str(orderid)
		url = pyqrcode.create(Url)
		url.svg(str(orderid)+'.svg', scale=8)
		print(url.terminal(quiet_zone=1))
		return jsonify(message='QR code generated')
	else:
		return jsonify(message='QR code not generated')



'''
all_item=session.query(Menu).all() to get all rows
		for x in all_item:
			print x.product_name
		print item_added.product_name
		Without .one returns array of Objects
		print session.query(Cart).delete() to delete all rows




@app.route('/payments', methods=['GET', 'POST'])
def getallpayment():
	client = razorpay.Client(auth=("rzp_test_ltGbBSkdqhYwIk", "JVsMpdGh21Es8hWhyAAWy2jM"))
	resp = client.payment.fetch_all()
	for r in resp:
		print r
		print resp[r]
		#print r["count"]
	return 'ok'
	return resp




@app.route('/orders', methods=['GET', 'POST'])
def getallorder():
	if request.method=='POST':
		client = razorpay.Client(auth=("rzp_test_ltGbBSkdqhYwIk", "JVsMpdGh21Es8hWhyAAWy2jM"))
		order_amount =600
		order_currency = 'INR'
		order_receipt = '1610991954'
		notes = {'ids': '1954'}   # OPTIONAL
		client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt)
		return 'ok'

	
@app.route('/paynow')
def app_create():
    return render_template('checkout.html')


@app.route('/charge', methods=['POST'])
def app_charge():
    amount = 5100
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    return json.dumps(razorpay_client.payment.fetch(payment_id))'''


		
if __name__ == '__main__':
    app.secret_key = 'super_secret_key' #to create sessions
    app.debug = True
    app.run(host='0.0.0.0', port=5000)