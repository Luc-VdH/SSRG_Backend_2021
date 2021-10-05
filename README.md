### The EC2 instance
    Due the SSL and HTTPS running locally is not possible, so we have it all set up on our EC2 instance. To connect to our EC2 instance follow the steps below:
    * cd into the ssh directory
    * chmod +x aws.sh
    * ./aws.sh
    The codebase is there and should be running in a TMUX session, access the session using:
    * tmux attach -t server
    The top window is running Celery which handles the parallel jobs, the bottom window is the server handling requests. 
    You should be able to see all the jobs running and all the requests arriving. If either process is not running, use the up arrow key to run the most recent command or see the steps below. 
    Some useful commands are:
    * change active window: ctrl+b then arrow key
    * enter scrolling mode: ctrl+b then [
    * to exit the session: ctrl+b then d
    For a guide on using TMUX (scrolling, changing windows, etc.) see https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/

### To run the webserver (from the ssrg_backend directory):

	make sure flask is installed, run: pip3 install flask

	run the app.py script: python3 src/app.py
	this will start up the server similar to npm start

	open the browser and go to localhost:8000 to view the text returned from the server


### To run Celery (from within the src directory):
    need to download rabbitmq and celery:
        sudo apt-get install rabbitmq-server
        pip install celery
	in src dir run:
		celery -A JobHandler worker --loglevel=info

### Packages needed for ReportScraper
    Install beautiful soup 4:
    pip3 install bs4
		
### To run Folderizer
    need to install packages:
        pip3 install pyunpack
        pip3 install patool

### To run UnitTests
    run command from main dir:
        python3 -m unittest discover -s test 

### To run moss script:
    The MOSS script is not stored in git or on the remote repo, it is included with our submission
    * chmod ug+x moss
    * ./moss -l java file1 fil2 etc


