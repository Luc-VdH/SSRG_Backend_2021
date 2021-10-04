import shutil, os
import sys
import unittest


#print(os.system("pwd"))

#sys.path.append('src/')
#from src.Archiver import Archiver
from src.Archiver import Archiver

class test_archiver(unittest.TestCase):
    def setupTest(self, folder):
        print("Setting up Test for: "+folder)
        path = os.path.join("test_files", folder)
        jobPath = os.path.join("job_src", "test_class","test_job_"+folder)
        if os.path.exists(jobPath):
                shutil.rmtree(jobPath)
        os.makedirs(jobPath)
        os.makedirs(jobPath+"/base")
        for f in os.listdir(path):
            shutil.copy(os.path.join(path, f), jobPath)
            
    def checkIfFilesCorrect(self, folder):
        print("Checking files Correct for: "+folder)
        os.chdir('..')
        path = os.path.join("job_src", "test_class","test_job_"+folder,"archive")
        pathCorrect = os.path.join("job_src", "test_class","test_correct_"+folder,"archive")
        files = os.listdir(path)
        filesCorrect = os.listdir(pathCorrect)
        for f in filesCorrect:
            self.assertIn(f, files)
            
    def test_Batch(self):
        self.setupTest("Batch")
        archiver = Archiver()
        archiver.formatArchive([], "test_class","test_job_Batch", 'BatchSubmissionExample.zip')
        self.checkIfFilesCorrect('Batch')
                
    def test_Files(self):
        self.setupTest("Files")
        archiver = Archiver()
        archiver.formatArchive(["STUDENT_5.zip", "STUDENT_6.zip"], "test_class","test_job_Files", "")
        self.checkIfFilesCorrect('Files')   
                 
    def test_All(self):
        self.setupTest("All")
        archiver = Archiver()
        archiver.formatArchive(["STUDENT_5.zip", "STUDENT_6.zip"], "test_class","test_job_All", 'BatchSubmissionExample.zip')
        self.checkIfFilesCorrect('All')
        
