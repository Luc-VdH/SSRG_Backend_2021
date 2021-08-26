import os


# class for extracting source from a vula archive TODO currently not functional
class Archiver:
    # constructor
    def __init__(self):
        self.files = []
        self.flags = []

    # run the extraction and formatting
    def formatArchive(self, files, username, jobname, flags):
        print(flags)
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == ".zip":
                os.system("unzip " + file.split("/")[-1])
                # for f in os.listdir(filename): # go through files in archive
                #     studentfolder = os.path.join(filename, f)
                #     if not os.path.isfile(studentfolder):
                #         for fi in os.listdir(studentfolder): # go though files in subfolder
                #             studentfile = os.path.join(studentfolder, fi)
                #             sfilename, sfile_extension = os.path.splitext(studentfile)
                #             if sfile_extension == ".zip":
                #                 os.system("unzip" + file)
                #             elif sfile_extension == ".gz":
                #                 pass
                os.system("cp -r " + filename + "/*." + flags + " .")

        return True
