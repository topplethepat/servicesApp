**ServiceApp Project** 
*Udacity Full Stack Web Developer Nanodegree Project 2*

***REQUIREMENTS***

- Python 2.7
- flask
- sqlalchemy
- Google account to login


The file service_app.py may be run in a Vagrant managed virtual machine, or VM.
Vagrant and VirtualBox must be installed on users local machine.


***SETUP and EXECUTION***

Start the VM:

	vagrant up

Log into the VM:

	vagrant ssh

Navigate to correct directory:

	cd /vagrant

Create the database:

	python my_databasesetup.py

Populate the database:

	python populate_svcs.py

Run the script:

	python service_app.py	

Go to http://localhost:5000/login on your browser and login	

