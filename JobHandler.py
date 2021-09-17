import re

from celery import Celery

from Archiver import Archiver
from Job import Job

app = Celery('createJob', broker='amqp://guest@localhost//')


# class for calling the archiver and starting job threads
class JobHandler:
    # constructor
    def __init__(self):
        pass

    # calls archiver then starts a new job in celery
    @app.task
    def createJob(files, reportName, username, flags, batch, email, mossID):
        archiver = Archiver()
        print(files)

        # call the archiver
        archived = archiver.formatArchive(files, username, reportName, batch)
        # start the job
        job = Job(archived, reportName, username, flags, email, mossID)
        job.start()
