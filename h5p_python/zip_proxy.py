import subprocess
import os
class ZipProxy:

    def __init__(self):
        self.exe_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../h5p_zip_process/dist/zip_process/zip_process.exe"))

    def extract(self, zipfile, member_name, tempdirname):
        dummy = subprocess.check_output([self.exe_path, "extract", zipfile, member_name, tempdirname])
        return(0)

    def replace(self, zipfile, member_name, file):
        dummy = subprocess.check_output([self.exe_path, "replace", zipfile, member_name, file])
        return(0)

if __name__ == "__main__":
    zip = ZipProxy()
    zip.extract("C:\\Users\\micha\\THU\\H5PTranslator\\data\\course-presentation-36.h5p","content/content.json", "C:\\Users\\micha\\THU\\H5PTranslator\\data\\")
