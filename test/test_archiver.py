import shutil, os
import sys
import unittest

if os.getcwd()[-1] == "ssrg_backend":
    os.chdir('src')
from Archiver import Archiver
print(os.getcwd()[-1])
if os.getcwd()[-1] == "src":
    os.chdir('..')

#unittest class to test the Archiver Class
class test_archiver(unittest.TestCase):
    #moves the test files into the correct folder to simulate a file upload
    def setupTest(self, folder):
        print("Setting up Test for: "+folder)
        path = os.path.join("test_files", folder)
        jobPath = os.path.join("job_src", "test_class","test_job_"+folder)
        #removes any previous files in the directory
        if os.path.exists(jobPath):
                shutil.rmtree(jobPath)
        #copies the files in
        os.makedirs(jobPath)
        os.makedirs(jobPath+"/base")
        for f in os.listdir(path):
            shutil.copy(os.path.join(path, f), jobPath)
            
    #helper method to check all the correct files are present for a given folder
    def checkIfFilesCorrect(self, folder):
        print("Checking files Correct for: "+folder)
        os.chdir('..')
        path = os.path.join("job_src", "test_class","test_job_"+folder,"archive")
        pathCorrect = os.path.join("job_src", "test_class","test_correct_"+folder,"archive")
        files = os.listdir(path)
        filesCorrect = os.listdir(pathCorrect)
        #checks if all required files are present
        for f in filesCorrect:
            self.assertIn(f, files)
            
    #unittest for the correct archival of the Batch submission
    def test_Batch(self):
        self.setupTest("Batch")
        archiver = Archiver()
        archiver.formatArchive([], "test_class","test_job_Batch", 'BatchSubmissionExample.zip')
        self.checkIfFilesCorrect('Batch')
                
    #unittest for the correct archival of the Batch submission
    def test_Files(self):
        self.setupTest("Files")
        archiver = Archiver()
        archiver.formatArchive(["STUDENT_5.zip", "STUDENT_6.zip"], "test_class","test_job_Files", "")
        self.checkIfFilesCorrect('Files')   
                 
    #unittest for the correct archival of the Batch submission
    def test_All(self):
        self.setupTest("All")
        archiver = Archiver()
        archiver.formatArchive(["STUDENT_5.zip", "STUDENT_6.zip"], "test_class","test_job_All", 'BatchSubmissionExample.zip')
        self.checkIfFilesCorrect('All')
        
