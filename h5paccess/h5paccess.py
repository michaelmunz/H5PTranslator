import json
from Tempfile import TemporaryDirectory

from de.thu.h5paccess import H5PAccess
from de.thu.h5paccess import Element

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

    def getContentName(self):
        return self.data.get('contentName', '')

    def getFile(self):
        return self.data.get('file', '')



class H5PAccessImpl(H5PAccess):
    tempdir = None


    def __init__(self):
        self.path = None
        self.elements = []

    def initialize(self, path):
        self.path = path
        import zipfile
        self.tempdir = TemporaryDirectory()

        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(self.tempdir.name)
        print(self.tempdir.name)

        with open(self.tempdir.name+"/content/content.json") as jsonFile:
            self.content = json.load(jsonFile)

        self.parse_data()

    def getNrOfSlides(self):
        return len(self.elements)

    def getNrOfElementsForSlide(self, nrSlide):
        return len(self.elements[nrSlide])

    def getElementsForSlide(self, nrSlide):
        return self.elements[nrSlide]


    def parse_data(self):
        self.elements = []
        slides = self.content['presentation']['slides']
        for s in slides:
            elementlist = s['elements']
            elements_of_slide = []
            for e in elementlist:
                el = ElementImpl(e)
                elements_of_slide.append(el)
            self.elements.append(elements_of_slide)


    def __del__(self):
        self.tempdir = None

