import copy
import json
import shutil
import uuid
import os
import hashlib

from h5p_python.temporary_directory import TemporaryDirectory
import h5p_python.autotranslate
import h5p_python.zip_h5p as zip_h5p
import h5p_python.zipfile2 as zip

class Element():
    def __init__(self, data):
        self.data = data

    def getX(self):
        val = self.data.get('x', None)
        if val is not None:
            val = float(val)
        return val

    def getY(self):
        val = self.data.get('y', None)
        if val is not None:
            val = float(val)
        return val

    def getWidth(self):
        val = self.data.get('width', None)
        if val is not None:
            val = float(val)
        return val

    def getHeight(self):
        val = self.data.get('height', None)
        if val is not None:
            val = float(val)
        return val

    def getText(self):
        text = self.data['action']['params'].get('text', None)
        if text is None:
            text = self.data['action']['params'].get('question', None)
        if text is None:
            text = self.data['action']['params'].get('textField', None)

        if text is None:
            text = ''

        return text

    def setText(self, text):
        cur_text = self.data['action']['params'].get('text', None)
        if cur_text is not None:
            self.data['action']['params']['text'] = text
            return

        cur_text = self.data['action']['params'].get('question', None)
        if cur_text is not None:
            self.data['action']['params']['question'] = text
            return

        cur_text = self.data['action']['params'].get('textField', None)
        if cur_text is not None:
            self.data['action']['params']['textField'] = text
            return

    def setX(self, val):
        self.data['x'] = str(val)

    def setY(self, val):
        self.data['y'] = str(val)

    def setWidth(self, val):
        self.data['width'] = str(val)

    def setHeight(self, val):
        self.data['height'] = str(val)

    def getContentName(self):
        return self.data.get('contentName', '')

    def getFile(self):
        return self.data.get('file', '')

    def getID(self):
        return self.getMetaData('h5pt.id')


    def isTextElement(self):
        return self.data['action']['library'] != "H5P.Image 1.1" and \
               self.data['action']['library'] != "H5P.Shape 1.0"



    def getMetaData(self, key):
        metadatastr = self.data['action']['metadata'].get('authorComments', "{}")
        metadatastr = metadatastr.replace("&quot;", '"')
        metadata = json.loads(metadatastr)
        return metadata.get(key, None)

    def setMetaData(self, key, value):
        metadatastr = self.data['action']['metadata'].get('authorComments', "{}")
        metadatastr = metadatastr.replace("&quot;", '"')
        metadata = json.loads(metadatastr)
        metadata[key] = value
        jsonstr = json.dumps(metadata)
        self.data['action']['metadata']['authorComments'] = jsonstr



    def getHash(self):
        return self.getMetaData('h5pt.hash')

    def verifyID(self):
        id = self.getID()
        if id == None:
            id = str(uuid.uuid1())
            self.setMetaData('h5pt.id', id)

    def setHash(self, hash):
        self.setMetaData('h5pt.hash', hash)





    def isTextModified(self, el_translated):
        hash_current = self.calculateHash(self.getText())
        hash_translated = el_translated.getHash()
        if hash_translated is None:
            return False
        return hash_translated != hash_current


    def calculateHash(self, text):
        # convert to byte and calculate hash
        result = hashlib.md5(text.encode('utf-8')).hexdigest()
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
        self.slide_of_element = {}

        slides = self.content['presentation']['slides']

        for slideNr,s in enumerate(slides):
            elementlist = s['elements']
            elements_of_slide = []
            for e in elementlist:
                el = Element(e)
                el.verifyID()
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


    def replaceImage(self, file, target_filename):
        filename = 'content/images/' + os.path.basename(target_filename)
        zip_h5p.replace(self.path, filename, file)


class H5PTranslator():
    def __init__(self):
        self.access_ori = H5PAccess()
        self.access_translate = H5PAccess()
        TemporaryDirectory.cleanup_tempdirs()
        self.auto_translator = h5p_python.autotranslate.Translator()
        self.isOpen = False


    def open(self, ori_file, translate_file):
        # initialize accessors (data is not yet parsed). Files are opened and data is read
        self.access_ori.open(ori_file, 'ori')
        if not os.path.exists(translate_file):
            shutil.copyfile(ori_file, translate_file)
        self.access_translate.open(translate_file, 'translate')

        # Afterwards,parse data
        self.access_ori.parseData()
        self.access_translate.parseData()

        # now me merge the data
        tranlated_elements = self.getTranslatedElementIDs()
        self.access_translate.mergeData(self.access_ori.getContent(), tranlated_elements)
        self.isOpen = True


    def close(self, write_changes):
        self.access_ori.close(write_changes)
        self.access_translate.close(write_changes)
        self.isOpen = False

    def isopen(self):
        return self.isOpen



    def getElementIDsByTranslation(self, isTranslated):
        ids = []
        trans_el = self.access_translate.getAllElements()

        for e in trans_el.values():
            if not e.isTextElement():
                continue
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
            # fetch corresponding element from translated data
            e_trans = self.access_translate.getElementByID(e.getID())
            # if no translated element has been found: ignore
            if e_trans is None:
                continue
            # if hashes do not match: add to modified ids
            if e.isTextModified(e_trans):
                modified_ids.append(e.getID())
        return modified_ids

    def getElementByID_original(self, id):
        return self.access_ori.getElementByID(id)

    def getElementByID_translate(self, id):
        return self.acces_translate.getElementByID(id)


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

    def getSlideForElementID_original(self, id):
        return self.access_ori.getSlideForElementID(id)

    def getSlideForElementID_translate(self, id):
        return self.access_translate.getSlideForElementID(id)


    def setTranslation(self, id, text_translated):
        el = self.access_translate.getElementByID(id)
        el.setText(text_translated)
        ori_text = self.access_ori.getElementByID(id).getText()
        hash_str = el.calculateHash(ori_text)
        el.setHash(hash_str)


    def getAutoTranslation(self, source_language, target_language, text):
        if text == "":
            return text
        translated = self.auto_translator.translate(text, source_language, target_language)
        return translated.text

    def replace_images(self, source_language, target_language, image_path):
        if not os.path.exists(os.path.join(image_path, source_language)):
            return False
        if not os.path.exists(os.path.join(image_path, target_language)):
            return False

        # match all images of source_language with the images in H5P file using hashes


        # calculate the hashes of all images contained in h5p
        imgFiles_ori = []
        hashes_en = {}
        with zip.ZipFile(self.access_ori.path, 'r') as zipFile:
            names = zipFile.namelist()
            for f in names:
                if f.find("content/images")>=0:
                    imgFiles_ori.append(f)
            for f in imgFiles_ori:
                img = zipFile.read(f)
                hash = hashlib.md5(img).hexdigest()
                hashes_en[hash] = f

        # calculate all hashes of the source images
        imgdir_source = os.path.join(image_path, source_language)
        files_src = os.listdir(imgdir_source)
        hashes_target = {}
        for fn in files_src:
            filename = os.path.join(imgdir_source, fn)
            with open(filename, "rb") as f:
                img = f.read()
                hash = hashlib.md5(img).hexdigest()
                hashes_target[hash] = os.path.join(image_path, target_language, fn)

        # match the hashes and replace the files in the target h5p file
        for h in hashes_target.keys():
            f_h5p = hashes_en.get(h)
            if f_h5p is not None:
                file = hashes_target[h]
                self.access_translate.replaceImage(f_h5p, file)

        return True