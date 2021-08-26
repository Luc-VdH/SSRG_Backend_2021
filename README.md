### To run the webserver:

	make sure flask is installed, run: pip3 install flask

	run the app.py script: python3 app.py
	this will start up the server similar to npm start

	open the browser and go to localhost:8000 to view the text returned from the server

### To run moss script:
* chmod ug+x moss
* ./moss -l java file1 fil2 etc

### Connecting to the EC2 instance
* cd into the ssh directory
* chmod +x aws.sh
* ./aws.sh

### To run Celery
    need to download rabbitmq and celery:
        sudo apt-get install rabbitmq-server
        pip install celery
	in a terminal run:
		celery -A JobHandler worker --loglevel=info
