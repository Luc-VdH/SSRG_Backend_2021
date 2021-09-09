import os
import shutil

# class for extracting source from a vula archive TODO currently not functional
class Archiver:
    # constructor
    def __init__(self):
        self.files = []
        self.flags = []

    # run the extraction and formatting
    def formatArchive(self, files, coursecode, jobname, batch):
        print(files)
        
        path = os.path.join(".","job_src", coursecode, jobname)
        pathdir = os.path.join(".","job_src", coursecode, jobname, "archive")
        
        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        else:
            if os.listdir(pathdir) != []:
                os.system(f"rm -r {pathdir}/*")  
              
        if batch != '':
            os.system(f'unzip "{path}/{batch}" -d "{path}/temp" >/dev/null')
            #for f in os.listdir(os.path.join(path,"temp",os.path.splitext(batch)[0])):
            #    shutil.move(os.path.join(path,"temp",os.path.splitext(batch)[0], f), os.path.join(pathdir, f))
            batchname = os.path.splitext(batch)[0]
            shutil.move(os.path.join(path,"temp",batchname), os.path.join(pathdir,batchname))
            os.remove(f"{path}/{batch}")
            shutil.rmtree(f"{path}/temp")
            os.system(f'python3 folderizer.py {pathdir}/BatchSubmissionExample {pathdir}/test >/dev/null')
            shutil.move(os.path.join(pathdir,"test",batchname), pathdir)
            shutil.rmtree(os.path.join(pathdir,"BatchSubmissionExample"))
            shutil.rmtree(os.path.join(pathdir,"test"))
            
        for f in files:
            if f == '' or "archive" == f:
                continue
            print("File: " + f)
            shutil.move(os.path.join(path,f), os.path.join(pathdir,f))
            #os.makedirs(os.path.join(pathdir,os.path.splitext(f)[0]))
            os.system(f'unzip "{pathdir}/{f}" -d "{pathdir}" >/dev/null')
            os.remove(f"{pathdir}/{f}")
        
        if os.path.exists(pathdir + "/.DS_Store"):
              os.remove(pathdir + "/.DS_Store")
        
        print ("Archived Files: "+" ".join(os.listdir(pathdir)))
        return pathdir
