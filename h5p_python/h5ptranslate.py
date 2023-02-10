import copy
import json
import shutil
import uuid
import os
import hashlib
from bs4 import BeautifulSoup

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


    def getMultiChoiceText(self):
        answers = self.data['action']['params']['answers']
        text = "<answers>"
        for a in answers:
            text +="<answer><text>"+a['text']+"</text>"
            text +="<notChosenFeedback>"+a['tipsAndFeedback']['notChosenFeedback']+"</notChosenFeedback>"
            text +="<chosenFeedback>"+a['tipsAndFeedback']['chosenFeedback']+"</chosenFeedback>"
            text += "<tip>" + a['tipsAndFeedback']['tip'] + "</tip>"
            text +="</answer>"
        text += "</answers>"
        text += "<question>" + self.data['action']['params']['question'] + "</question>"
        return text


    def setMultiChoiceText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for cnt,a in enumerate(results.findAll("answer")):
            self.data['action']['params']['answers'][cnt]['text'] = a.find('text').getText()
            self.data['action']['params']['answers'][cnt]['tipsAndFeedback']['notChosenFeedback'] = a.find('notchosenfeedback').getText()
            self.data['action']['params']['answers'][cnt]['tipsAndFeedback']['chosenFeedback'] = a.find('chosenfeedback').getText()
        self.data['action']['params']['question'] = results.find('question').getText()


    def getDragTextText(self):
        feedbacks = self.data['action']['params']['overallFeedback']
        text = "<feedbacks>"
        for a in feedbacks:
            fb=a.get('feedback')
            if fb is None:
                continue
            text +="<feedback>"+fb+"</feedback>"
            text +="</feedback>"
        text += "</feedbacks>"
        text += "<textField>" + self.data['action']['params']['textField'] + "</textField>"
        text += "<taskDescription>" + self.data['action']['params']['taskDescription'] + "</taskDescription> "
        return text


    def setDragTextText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for cnt,a in enumerate(results.findAll("feedbacks")):
            fb = a.find('feedback')
            if fb is not None:
                self.data['action']['params']['overallFeedback'][cnt]['feedback'] = fb.getText()
        tf = results.find('textfield')
        if tf is not None:
            self.data['action']['params']['textField'] = tf.getText()
        td = results.find('taskdescription')
        if td is not None:
            self.data['action']['params']['taskDescription'] = td.getText()


    def getDragQuestionText(self):
        return self.data['action']['metadata'].get('title', None)

    def setDragQuestionText(self, translated):
        self.data['action']['metadata']['title'] = translated

    def getSingleChoiceSetText(self):
        text = "<title>" + self.data['action']['metadata']['title'] + "</title>"
        choices = self.data['action']['params']['choices']
        text += "<choices>"
        for c in choices:
            text += "<question>"+c['question']+"</question>"
            text += "<answers>"
            answers = c['answers']
            for a in answers:
                text += a
            text += "</answers>"
        return text

    def setSingleChoiceSetText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for q_cnt, c in enumerate(results.findAll("choices")):
            q = c.find('question')
            if q is not None:
                self.data['action']['params']['choices'][q_cnt]['question'] = q.getText()
            for a_cnt, a in enumerate(c.findAll("answers")):
                a = a.find('answer')
                if a is not None:
                    self.data['action']['params']['choices'][q_cnt]['answers'][a_cnt] = a.getText()

        tf = results.find('title')
        if tf is not None:
            self.data['action']['metadata']['title'] = tf.getText()



    def getText(self):
        if self.isMultiChoiceElement():
            text = self.getMultiChoiceText()
        elif self.isDragTextElement():
            text = self.getDragTextText()
        elif self.isDragQuestionElement():
            text = self.getDragQuestionText()
        elif self.isSingleChoiceSet():
            text = self.getSingleChoiceSetText()
        else:
            text = self.data['action']['params'].get('text', None)
            if text is None:
                text = self.data['action']['params'].get('question', None)
            if text is None:
                text = self.data['action']['params'].get('textField', None)

            if text is None:
                text = ''
        return text

    def setText(self, text):
        if self.isMultiChoiceElement():
           self.setMultiChoiceText(text)
        elif self.isDragTextElement():
            self.setDragTextText(text)
        elif self.isDragQuestionElement():
            self.setDragQuestionText(text)
        elif self.isSingleChoiceSet():
            self.setSingleChoiceSetText(text)
        else:
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
        return self.data['action']['subContentId']

    def getLibrary(self):
        return self.data['action']['library']

    def isTextElement(self):
        return self.getLibrary() != "H5P.Image 1.1" and \
               self.getLibrary() != "H5P.Shape 1.0"

    def isMultiChoiceElement(self):
        return self.getLibrary() == "H5P.MultiChoice 1.16"

    def isDragTextElement(self):
        return self.getLibrary() == "H5P.DragText 1.10"

    def isDragQuestionElement(self):
        return self.getLibrary() == "H5P.DragQuestion 1.14"

    def isSingleChoiceSet(self):
        return self.getLibrary() == "H5P.SingleChoiceSet 1.11"

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
                el = Element(e)
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
        self.access_ori.close(False)
        self.access_translate.close(write_changes)
        self.isOpen = False

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

    def translate_element(self, source_language, target_language, id):
        elem = self.getElementByID_original(id)
        text = elem.getText()
        translated = self.auto_translator.translate(text, dest=target_language, src=source_language)
        self.setTranslation(id, translated.text)
        return translated.text

    def replace_images(self, source_language, target_language, image_path):
        if not os.path.exists(os.path.join(image_path, source_language)):
            return False
        if not os.path.exists(os.path.join(image_path, target_language)):
            return False

        # match all images of source_language with the images in H5P file using hashes
        # first calculate the hashes of all images contained in h5p
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