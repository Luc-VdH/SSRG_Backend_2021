### To run the webserver (from the ssrg_backend directory):

	make sure flask is installed, run: pip3 install flask

	run the app.py script: python3 src/app.py
	this will start up the server similar to npm start

	open the browser and go to localhost:8000 to view the text returned from the server

### To run moss script:
* chmod ug+x moss
* ./moss -l java file1 fil2 etc

### Connecting to the EC2 instance
* cd into the ssh directory
* chmod +x aws.sh
* ./aws.sh

### To run Celery (from within the src directory):
    need to download rabbitmq and celery:
        sudo apt-get install rabbitmq-server
        pip install celery
	in src dir run:
		celery -A JobHandler worker --loglevel=info
		
### To run Folderizer
    need to install packages:
        pip3 install pyunpack
        pip3 install patool

### To run UnitTests
    run command from main dir:
        python3 -m unittest discover -s test 
