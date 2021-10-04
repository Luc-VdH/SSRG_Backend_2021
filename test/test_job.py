import shutil, os
import sys
import unittest

os.chdir("..")
from src.Job import Job
os.chdir("ssrg_backend/src")
print(os.getcwd())

#unittest class to test the Job Class
class test_job(unittest.TestCase):
    #creates a global job
    job = Job("../job_src/test_class/test_correct_All/archive", 
        ["../job_src/test_class/test_correct_All/base/base1.java", "../job_src/test_class/test_correct_All/base/base2.java"],
        "test_correct_All", "test_class", "cc", True, "795955383")
    #variable used to check if the upload has been done yet
    uploadComplete = False 
        
    #unittest for the correct behavior of an invalid submission
    def test_Invalid_Upload(self):
        jobFail = Job("Invalid Submission", "", "testFail", "test_class", "cc", False, '795955383')
        self.assertFalse(jobFail.uploadFilesToMoss())
        self.assertFalse(jobFail.scrapeReport())
        self.assertTrue(jobFail.updateReportDAO())
        self.assertFalse(jobFail.emailJobComplete())
            
    #unittest for the correct behavior for uploading a moss submission
    def test_moss(self):
        if test_job.uploadComplete == False:
            test_job.uploadComplete = self.job.uploadFilesToMoss()
        self.assertTrue(test_job.uploadComplete, "Upload Files to Moss Failed: "+self.job.urlOfRawReport)
        
                
    #unittest for the correct behavior of calling the report scrapper
    def test_scrape(self):
        if test_job.uploadComplete == False:
            test_job.uploadComplete = test_job.job.uploadFilesToMoss()   
        if test_job.uploadComplete == False:
            self.assertFalse(test_job.job.scrapeReport())
        else:
            self.assertTrue(test_job.job.scrapeReport())
        
                 
    #unittest for the correct behavior of calling to update the ReportDAO object
    def test_update_reportDAO(self):
        self.assertTrue(test_job.job.updateReportDAO())
            
    #unittest for the correct behavior of calling to email the user about a compelete job
    def test_send_email(self):
        self.assertTrue(test_job.job.emailJobComplete())
        
