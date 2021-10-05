import os
import re
import shutil
import traceback


# class for extracting source from a vula archive
class Archiver:
    # constructor
    def __init__(self):
        self.files = []
        self.flags = []

    # run the extraction and formatting
    def formatArchive(self, files, coursecode, jobname, batch):
        print(files)
        cwd = os.getcwd()
        if cwd.split("/")[-1]=='ssrg_backend':
            os.chdir('src')
        print("Archvier CWD:")
        print(os.getcwd())
        path = os.path.join("..", "job_src", coursecode, jobname)
        zippath = os.path.join("..", "job_src", coursecode, jobname)
        pathdir = os.path.join("..", "job_src", coursecode, jobname, "archive")

        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        else:
            if os.listdir(pathdir) != []:
                os.system(f"rm -r {pathdir}/*")
        try:
            if batch != '':
                os.system(f'unzip "{zippath}/{batch}" -d "{zippath}/temp" >/dev/null')  # unzip to /temp
                
                batchname = os.path.splitext(batch)[0]
                shutil.move(os.path.join(path, "temp", batchname),
                            os.path.join(pathdir, batchname))  # move temp/batch to archive/batch
                os.remove(f"{path}/{batch}")  # remove zip
                shutil.rmtree(f"{path}/temp")  # remove temp folder
                os.system(
                    f'python3 folderizer.py {pathdir}/{batchname} {pathdir}/test >/dev/null')  # folderise to archive/test
                shutil.rmtree(os.path.join(pathdir, batchname))  # remove archive/batch
                for f in os.listdir(os.path.join(pathdir, "test")):  # move all from archive/test to arhcive
                    shutil.move(os.path.join(pathdir, "test", f), pathdir)
                shutil.rmtree(os.path.join(pathdir, "test"))  # remove test folder
        except Exception:
            traceback.print_exc()
            return "Invalid Batch Submission Archive"
        
        try:
            for f in files:
                if f == '' or "archive" == f or f=="base":
                    continue
                print("File: " + f)
                shutil.move(os.path.join(path, f), os.path.join(pathdir, f))
                # os.makedirs(os.path.join(pathdir,os.path.splitext(f)[0]))
                os.system(f'unzip "{pathdir}/{f}" -d "{pathdir}/temp" >/dev/null')
                os.remove(f"{pathdir}/{f}")
            if files !=[]:
                os.system(f'python3 folderizer.py {pathdir}/temp {pathdir} >/dev/null')  # folderise individuals to archive
                shutil.rmtree(f"{pathdir}/temp")
        except Exception:
            traceback.print_exc()
            return "Invalid Individual submission archives"

        if os.path.exists(pathdir + "/.DS_Store"):
            os.remove(pathdir + "/.DS_Store")

        print("Archived Files: " + " ".join(os.listdir(pathdir)))
        return pathdir
