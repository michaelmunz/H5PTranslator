import copy
import json
import shutil
import uuid
import zipfile
import os
import hashlib


##########################################################
# switch  import if running in python!!!
#from h5ptranslate.temporary_directory import TemporaryDirectory
from temporary_directory import TemporaryDirectory
##########################################################

from de.thu.h5ptranslate import H5PTranslator
from de.thu.h5ptranslate import Element


class ElementImpl(Element):
    def __init__(self, data):
        self.data = data

    def getX(self):
        return self.data.get('x', '')

    def getY(self):
        return self.data.get('y', '')

    def getWidth(self):
        return self.data.get('width', '')

    def getHeight(self):
        return self.data.get('height', '')

    def getText(self):
        action = self.data['action']
        params = action['params']
        return params.get('text', '')

    def setText(self, text):
        self.data['action']['params']['text'] = text

    def getContentName(self):
        return self.data.get('contentName', '')

    def getFile(self):
        return self.data.get('file', '')

    def getID(self):
        return self.getMetaData().get('h5pt.id', None)


    def getMetaData(self):
        return self.data['action']['metadata']

    def getHash(self):
        return self.getMetaData().get('h5pt.hash', None)

    def verifyID(self):
        id = self.getID()
        if id == None:
            id = str(uuid.uuid1())
            self.getMetaData()['h5pt.id'] = id

    def setHash(self, hash):
        self.getMetaData()['h5pt.hash'] = hash


    def isTextModified(self):
        hash_ori = self.getHash()
        hash_current = self.calculateHash(self.getText())
        return hash_ori != hash_current


    def calculateHash(self, text):
        # convert to byte and calculate hash
        result = hashlib.md5(text.encode()).hexdigest()
        return result

    def set_data_to_merge(self, merge_data):
        self.setText(merge_data["text"])
        self.setHash(merge_data["hash"])
        self.setX(merge_data["x"])
        self.setY(merge_data["y"])
        self.setWidth(merge_data["width"])
        self.setHeight(merge_data["height"])


    def get_data_to_merge(self):
        return {"text": self.getText(), "hash": self.getHash(), "x": self.getX(), "y": self.getY(), "width" : self.getWidth(), "height": self.getHeight()}


class H5PAccessImpl():
    def __init__(self):
        self.path = None
        self.elements_by_id = {}
        self.elements_of_slide = []
        self.content = None
        self.content_path = None
        self.tempdir = None

    def open(self, path):
        self.tempdir = TemporaryDirectory()
        self.path = path

        with zipfile.ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall(self.tempdir.name)

        self.content_path = os.path.join(self.tempdir.name, "content/content.json")
        with open(self.content_path, 'r') as jsonFile:
            self.content = json.load(jsonFile)

    def getNrOfSlides(self):
        return len(self.elements_of_slide)

    def getNrOfElementsForSlide(self, nrSlide):
        return len(self.elements_of_slide[nrSlide])

    def getElementsForSlide(self, nrSlide):
        return self.elements_of_slide[nrSlide]

    def getElementByID(self, id):
        return self.elements_by_id.get(id, None)

    def getAllElements(self):
        return self.elements_by_id

    def getContent(self):
        return self.content

    def parseData(self):
        self.elements_by_id = {}
        self.elements_of_slide = []

        slides = self.content['presentation']['slides']

        for s in slides:
            elementlist = s['elements']
            elements_of_slide = []
            for e in elementlist:
                el = ElementImpl(e)
                el.verifyID()
                elements_of_slide.append(el)
                self.elements_by_id[el.getID()] = el
            self.elements_of_slide.append(elements_of_slide)


    def mergeData(self, new_content, translated_elementIDs):
        # get the data to merge from the current file
        merge_data = {}
        for id in translated_elementIDs:
            merge_data[id] = self.getElementByID(id).get_data_to_merge()

        # content of translated file is re-parsed with content from "original" file
        self.content = copy.deepcopy(new_content)
        self.parseData()

        # replace any already translated element by the previous translation from the temporary merge file
        for id in translated_elementIDs:
            self.getElementByID(id).set_data_to_merge(merge_data[id])


    def getTempDir(self):
        return self.tempdir.getPath()


    def __del__(self):
        self.tempdir = None

    def close(self, write_changes):
        if write_changes:
            #  write modified json data into file
            with open(self.content_path, 'w') as jsonFile:
                json.dump(self.content, jsonFile)

        shutil.make_archive(self.path, 'zip', self.getTempDir())
        self.tempdir.close()



class H5PTranslatorImpl(H5PTranslator):
    def __init__(self):
        self.access_ori = H5PAccessImpl()
        self.access_translate = H5PAccessImpl()
        TemporaryDirectory.cleanup_tempdirs()

    def open(self, ori_file, translate_file):


        # initialize accessors (data is not yet parsed). Files are opened and data is read
        self.access_ori.open(ori_file)
        self.access_translate.open(translate_file)

        # Afterwards,parse data
        self.access_ori.parseData()
        self.access_translate.parseData()

        # now me merge the data
        tranlated_elements = self.getTranslatedElementIDs()
        self.access_translate.mergeData(self.access_ori.getContent(), tranlated_elements)


    def close(self, write_changes):
        self.access_ori.close(write_changes)
        self.access_translate.close(write_changes)



    def getElementIDsByTranslation(self, isTranslated):
        ids = []
        trans_el = self.access_translate.getAllElements()

        for e in trans_el.values():
            if isTranslated == True and e.getHash() is not None:
                ids.append(e.getID())
            elif isTranslated == False and e.getHash() is None:
                ids.append(e.getID())
        return ids


    def getUntranslatedElementIDs(self):
        return self.getElementIDsByTranslation(isTranslated = False)

    def getTranslatedElementIDs(self):
        return self.getElementIDsByTranslation(isTranslated = True)

    def getModifiedElementIDs(self):
        modified_ids = []
        ori_el = self.access_ori.getAllElements()

        for e in ori_el.values():
            if e.isTextModified():
                modified_ids.append(e.getID())
        return modified_ids


    def getNrOfSlides(self):
        return self.access_ori.getNrOfSlides()

    def getElementsForSlide_original(self, nrSlide):
        return self.access_ori.getElementsForSlide(nrSlide)

    def getElementsForSlide_translate(self, nrSlide):
        return self.access_translate.getElementsForSlide(nrSlide)

    def getTemporaryDir_original(self):
        return self.access_ori.getTempDir()

    def getTemporaryDir_translate(self):
        return self.access_translate.getTempDir()


    def setTranslation(self, id, text_translated):
        el = self.access_translate.getElementByID(id)
        el.setText(text_translated)
        ori_text = self.access_ori.getElementByID(id).getText()
        hash = el.calculateHash(ori_text)
        el.setHash(hash)


