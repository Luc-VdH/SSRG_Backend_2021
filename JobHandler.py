from celery import Celery

from Archiver import Archiver
from Job import Job

app = Celery('createJob', broker='amqp://guest@localhost//')

class JobHandler:
	archiver = Archiver()
	
	@app.task
	def createJob(files, reportName, username, flags):
		job = Job(files, reportName, username, flags)
		job.start()
		
	def archive(self):
	    #TODO call archiver
	    return True
