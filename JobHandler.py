from celery import Celery

from Archiver import Archiver
from Job import Job

app = Celery('createJob', broker='amqp://guest@localhost//')

class JobHandler:
	
	@app.task
	def createJob(files, reportName, username, flags):
		archiver = Archiver()
		print(files)
		archived = archiver.formatArchive(files, username, reportName, flags)
		job = Job(files, reportName, username, flags)
		job.start()

