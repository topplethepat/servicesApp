import random
import string
import httplib2
import json
import requests

from flask import Flask,render_template,request,redirect,jsonify,url_for,flash
# converts response into object to send to client
from flask import make_response 
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from my_databasesetup import Base, Service, TaskItem, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__) 

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine(
	'sqlite:///servicemenuwithusers1.db',
	connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
	# checks to make sure it is user and not malicious script
	if request.args.get('state') != login_session['state']:  
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	code = request.data
	try:
		# upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		# onetime code flow server is sending off
		oauth_flow.redirect_uri = 'postmessage'
		# exchanges authorization code for a credentials object	 
		credentials = oauth_flow.step2_exchange(code) 
	except FlowExchangeError:
		response = make_response(
		json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		         % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								            200)
		response.headers['Content-Type'] = 'application/json'
		return response
		
	# Store the access token in the session for later use.
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id
	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# see if user exists, if not create new
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
		login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None	


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s',access_token
    print 'User name is: '
    print login_session['username']
    url='https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke user token.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON APIs to view Services Information


@app.route('/service/<int:service_id>/task/JSON')
def serviceTaskJSON(service_id):
		services = session.query(Service).filter_by(id = service_id).all()
		items = session.query(TaskItem).filter_by(service_id = service_id).all()
		return jsonify(TaskItems=[i.serialize for i in items])

@app.route('/service/JSON')
def servicesJSON():
		services = session.query(Service).all()
		return jsonify(services= [service.serialize for service in services])

# Show all services, different views per whether user is logged in or not
@app.route('/')
@app.route('/service/')
def showServices():
	services = session.query(Service).all()

	if 'username' not in login_session:
		return render_template('show_if_not_loggedIn.html', services = services)
	else:
		
		return render_template('show.html', services = services)

# Create a new service
@app.route('/service/new/', methods=['GET','POST'])
def newService():
	if request.method == 'POST' and 'username' in login_session:
			newService = Service(name = request.form['name'])
			session.add(newService)
			#flash('New service %s Successfully Created' % newService.name)
			session.commit()
			return redirect(url_for('showServices'))
	else:
			return render_template('newService.html')

# Edit a service
@app.route('/service/<int:service_id>/edit/', methods = ['GET', 'POST'])
def editService(service_id):
	editedService = session.query(Service).filter_by(id = service_id).one()
	if request.method == 'POST' and 'username' in login_session:
			if request.form['name']:
				editedService.name = request.form['name']
				#flash('service Successfully Edited %s' % editedService.name)
				return redirect(url_for('showServices'))
	else:
		return render_template('services_edit.html', service = editedService)


# Delete a service - not used in application currently but may add later
@app.route('/service/<int:service_id>/delete/', methods = ['GET','POST'])
def deleteService(service_id):
	serviceToDelete = session.query(Service).filter_by(id = service_id).one()
	if request.method == 'POST' and 'username' in login_session:
		session.delete(serviceToDelete)
		# flash('%s Successfully Deleted' % serviceToDelete.name)
		session.commit()
		return redirect(url_for('showServices', service_id = service_id))
	else:
		return render_template('serviceDelete.html',service = serviceToDelete)

# Show a service Task
@app.route('/service/<int:service_id>/')
@app.route('/service/<int:service_id>/task/')
def showTask(service_id):
		service = session.query(Service).filter_by(id = service_id).one()
		items = session.query(TaskItem).filter_by(service_id = service_id).all()
		return render_template('task.html', items = items, service = service)
		 


# Create a new Task item
@app.route('/service/<int:service_id>/task/new/',methods=['GET','POST'])
def newTaskItem(service_id):
	service = session.query(Service).filter_by(id = service_id).one()
	if request.method == 'POST' and 'username' in login_session:
			newItem = TaskItem(
				name = request.form['name'], description = request.form['description'], 
				price = request.form['price'], service_id = service_id)
			session.add(newItem)
			session.commit()
			#flash('New Task %s Item Successfully Created' % (newItem.name))
			return redirect(url_for('showTask', service_id = service_id))
	else:
			return render_template('newTaskItem.html', service_id = service_id)

# Edit a Task item
@app.route('/service/<int:service_id>/task/<int:task_id>/edit', methods=['GET','POST'])
def editTaskItem(service_id, task_id):

		editedItem = session.query(TaskItem).filter_by(id = task_id).one()
		service = session.query(Service).filter_by(id = service_id).one()
		if request.method == 'POST' and 'username' in login_session:
				if request.form['name']:
						editedItem.name = request.form['name']
				if request.form['description']:
						editedItem.description = request.form['description']
				if request.form['price']:
						editedItem.price = request.form['price']
				# if request.form['animal']:
				# 		editedItem.course = request.form['animal']
				session.add(editedItem)
				session.commit() 
				flash('Task Item Successfully Edited')
				return redirect(url_for('showTask', service_id = service_id))
		else:
				return render_template(
					'editTaskitem.html', service_id = service_id, Task_id = task_id, item = editedItem)


# Delete a Task item
@app.route('/service/<int:service_id>/task/<int:task_id>/delete',methods=['GET','POST'])
def deleteTaskItem(service_id,task_id):
		service = session.query(Service).filter_by(id = service_id).one()
		itemToDelete = session.query(TaskItem).filter_by(id = task_id).one() 
		if request.method == 'POST' and 'username' in login_session:
				session.delete(itemToDelete)
				session.commit()
				flash('Task Item Successfully Deleted')
				return redirect(url_for('showTask', service_id = service_id))
		else:
				return render_template('deleteTaskItem.html', item = itemToDelete)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
