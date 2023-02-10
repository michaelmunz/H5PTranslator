import os
import copy
import json
import shutil
import zip_h5p as zip_h5p
from TemporaryDirectory import TemporaryDirectory
from Element import Element

class H5PAccess():
    def __init__(self):
        self.path = None
        self.elements_by_id = {}
        self.elements_of_slide = []
        self.content = None
        self.content_path = None
        self.tempdir = None


    def open(self, path, postfix):
        self.tempdir = TemporaryDirectory(postfix)
        self.path = path

        if path.endswith(".json"):
            self.content_path = os.path.join(self.tempdir.name, "content/content.json")
            os.makedirs(os.path.dirname(self.content_path))
            shutil.copyfile(self.path, self.content_path)
        else:
            zip_h5p.extract(self.path, 'content/content.json', self.tempdir.name)
            self.content_path = os.path.join(self.tempdir.name, "content/content.json")
        with open(self.content_path, 'r', encoding="utf8") as jsonFile:
            contentstr = jsonFile.read()
            self.content = json.loads(contentstr)

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
        self.slide_of_element = {}

        slides = self.content['presentation']['slides']

        for slideNr,s in enumerate(slides):
            elementlist = s['elements']
            elements_of_slide = []
            for e in elementlist:
                el = Element.create_element(e)
                if el is None:
                    continue
                elements_of_slide.append(el)
                self.elements_by_id[el.getID()] = el
                self.slide_of_element[el.getID()] = slideNr
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

    def getSlideForElementID(self, id):
        return self.slide_of_element[id]

    def getTempDir(self):
        return self.tempdir.getPath()


    def __del__(self):
        self.tempdir = None

    def close(self, write_changes):
        if write_changes:
            #  write modified json data into file
            with open(self.content_path, 'w') as jsonFile:
                json.dump(self.content, jsonFile)
            if self.path.endswith(".json"):
                shutil.copyfile(self.content_path, self.path)
            else:
                zip_h5p.replace(self.path, 'content/content.json', self.content_path)


        # comment only for testing purposes
        if self.tempdir is not None:
            self.tempdir.close()


    def replaceImage(self, member_name, file):
        zip_h5p.replace(self.path, member_name, file)