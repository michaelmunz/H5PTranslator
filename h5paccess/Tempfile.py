import os
import shutil
import uuid


class TemporaryDirectory:
    def __init__(self):
        #self.name = '_temp.h5p'+str(uuid.uuid1())
        self.name = '_temp'

        if os.path.exists(self.name):
            shutil.rmtree(self.name)
        os.makedirs(self.name)

    def __del__(self):
        shutil.rmtree(self.name)





