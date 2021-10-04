import shutil, os
import sys
import unittest

from src.Job import Job

class test_job(unittest.TestCase):
    job = Job("../job_src/test_class/test_correct_All/archive", 
        ["../job_src/test_class/test_correct_All/base/base1.java", "../job_src/test_class/test_correct_All/base/base2.java"],
        "test_correct_All", "test_class", "cc", True, "795955383")
    uploadComplete = False
        
    def test_Invalid_Upload(self):
        jobFail = Job("Invalid Submission", "", "testFail", "test_class", "cc", False, '795955383')
        self.assertFalse(jobFail.uploadFilesToMoss())
        self.assertFalse(jobFail.scrapeReport())
        self.assertTrue(jobFail.updateReportDAO())
        self.assertFalse(jobFail.emailJobComplete())
            
    def test_moss(self):
        if test_job.uploadComplete == False:
            test_job.uploadComplete = self.job.uploadFilesToMoss()
        self.assertTrue(test_job.uploadComplete, "Upload Files to Moss Failed: "+self.job.urlOfRawReport)
        
                
    def test_scrape(self):
        if test_job.uploadComplete == False:
            test_job.uploadComplete = test_job.job.uploadFilesToMoss()   
        if test_job.uploadComplete == False:
            self.assertFalse(test_job.job.scrapeReport())
        else:
            self.assertTrue(test_job.job.scrapeReport())
        
                 
    def test_update_reportDAO(self):
        self.assertTrue(test_job.job.updateReportDAO())
            
    def test_send_email(self):
        self.assertTrue(test_job.job.emailJobComplete())
        
