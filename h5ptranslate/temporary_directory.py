import os
import glob
import shutil
import uuid


class TemporaryDirectory:

    tempdir_root = os.path.abspath(".")
    temp_prefix = '_temp.h5p.'

    def __init__(self):
        self.name = os.path.join(TemporaryDirectory.tempdir_root, TemporaryDirectory.temp_prefix +str(uuid.uuid1()))
        os.makedirs(self.name)

    def __del__(self):
        #self.close()
        pass

    def getPath(self):
        return self.name

    @staticmethod
    def cleanup_tempdirs():
        existing_tempdirs = glob.glob(os.path.join(TemporaryDirectory.tempdir_root, TemporaryDirectory.temp_prefix + "*"))
        if len(existing_tempdirs) > 0:
            for dir in existing_tempdirs:
                shutil.rmtree(dir)

    def close(self):
        try:
            shutil.rmtree(self.name)
        except:
            pass





