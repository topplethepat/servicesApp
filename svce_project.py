from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_databasesetup import Base, Service, ServiceItems

app = Flask(__name__)

engine = create_engine('sqlite:///servicemenu.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/services/')
def ServiceMenu():
	services = session.query(Service).all()
	
	return render_template('landing.html', services = services)

@app.route('/services/<int:service_id>/')
def ServiceItemsMenu(service_id):
	services = session.query(Service).filter_by(id = service_id).one()
	
	items = session.query(ServiceItems).filter_by(service_id = services.id)

	return render_template('servicemenu.html', services = services, items = items)	

@app.route('/services/<int:service_id>/add/', methods = ['GET', 'POST'])
def serviceItemsAdd(service_id):
	
	if request.method == 'POST':
		newService = ServiceItems(name = request.form['name'], description = request.form['description'], 
			price = request.form['price'],service_id = service_id)
		session.add(newService)
		session.commit()
		return redirect(url_for('ServiceItemsMenu',service_id = service_id))
	else:
		return render_template('services_add.html', service_id = service_id)

@app.route('/services/<int:service_id>/<int:item_id>/edit/', methods = ['GET', 'POST'])		
def serviceItemsEdit(service_id, item_id):
	eachItem = session.query(ServiceItems.filter_by(id = item_id).one())
	

	return render_template('services_edit.html', service_id = service_id, item_id = item_id, eachItem = e.id)


if __name__ == '__main__':
	
	app.debug = True
	app.run(host='0.0.0.0', port=8000)