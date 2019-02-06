#FB pw serviceApp2019
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from my_databasesetup import Base, Service, TaskItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response # converts response into object to send to client
import requests


engine = create_engine('sqlite:///servicemenuwithusers1.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#JSON APIs to view service Information
# @app.route('/service/<int:service_id>/task/JSON')
# def serviceItemJSON(service_id):
# 		service = session.query(Service).filter_by(id = service_id).one()
# 		items = session.query(TaskItem).filter_by(service_id = service_id).all()
# 		return jsonify(TaskItems=[i.serialize for i in items])


	
# @app.route('/service/<int:service_id>/task/<int:task_id>/JSON')
# def serviceItemJSON(service_id, task_item_id):
# 		Task_Item = session.query(TaskItem).filter_by(id = task_item_id).one()
# 		return jsonify(Task_Item = Task_Item.serialize)

# @app.route('/service/JSON')
# def servicesJSON():
# 		services = session.query(Service).all()
# 		return jsonify(services= [r.serialize for r in services])


#Show all services
@app.route('/')
@app.route('/service/')
def showServices():
	service = session.query(Service).all()

	# if 'username' not in login_session:
	# 	return render_template('publicservices.html', services = services)
	# else:
		
	return render_template('show.html', service = service)

#Create a new service
@app.route('/service/new/', methods=['GET','POST'])
def newService():
	if request.method == 'POST':
			newService = Service(name = request.form['name'])
			session.add(newService)
			#flash('New service %s Successfully Created' % newService.name)
			session.commit()
			return redirect(url_for('showServices'))
	else:
			return render_template('services_add.html')

#Edit a service
@app.route('/service/<int:service_id>/edit/', methods = ['GET', 'POST'])
def editService(service_id):
	editedService = session.query(Service).filter_by(id = service_id).one()
	if request.method == 'POST':
			if request.form['name']:
				editedService.name = request.form['name']
				#flash('service Successfully Edited %s' % editedService.name)
				return redirect(url_for('showServices'))
	else:
		return render_template('services_edit.html', service = editedService)


#Delete a service
@app.route('/service/<int:service_id>/delete/', methods = ['GET','POST'])
def deleteService(service_id):
	serviceToDelete = session.query(Service).filter_by(id = service_id).one()
	if request.method == 'POST':
		session.delete(serviceToDelete)
		#flash('%s Successfully Deleted' % serviceToDelete.name)
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
		 


#Create a new Task item
@app.route('/service/<int:service_id>/task/new/',methods=['GET','POST'])
def newTaskItem(service_id):
	service = session.query(Service).filter_by(id = service_id).one()
	if request.method == 'POST':
			newItem = TaskItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], service_id = service_id)
			session.add(newItem)
			session.commit()
			#flash('New Task %s Item Successfully Created' % (newItem.name))
			return redirect(url_for('showTask', service_id = service_id))
	else:
			return render_template('newTaskItem.html', service_id = service_id)

# #Edit a Task item
@app.route('/service/<int:service_id>/task/<int:task_id>/edit', methods=['GET','POST'])
def editTaskItem(service_id, task_id):

		editedItem = session.query(TaskItem).filter_by(id = task_id).one()
		service = session.query(Service).filter_by(id = service_id).one()
		if request.method == 'POST':
				if request.form['name']:
						editedItem.name = request.form['name']
				if request.form['description']:
						editedItem.description = request.form['description']
				if request.form['price']:
						editedItem.price = request.form['price']
				if request.form['animal']:
						editedItem.course = request.form['animal']
				session.add(editedItem)
				session.commit() 
				flash('Task Item Successfully Edited')
				return redirect(url_for('showTask', service_id = service_id))
		else:
				return render_template('editTaskitem.html', service_id = service_id, Task_id = task_id, item = editedItem)


# #Delete a Task item
@app.route('/service/<int:service_id>/task/<int:task_id>/delete', methods = ['GET','POST'])
def deleteTaskItem(service_id,task_id):
		service = session.query(Service).filter_by(id = service_id).one()
		itemToDelete = session.query(TaskItem).filter_by(id = task_id).one() 
		if request.method == 'POST':
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


