from bs4 import BeautifulSoup
import hashlib
import json
from abc import ABC, abstractmethod


class Element(ABC):
    def __init__(self, data):
        self.data = data


    def create_element(data):
        library = data['action']['library']
        # remove version number
        library = library.split(" ")[0]

        # ignore all images and shapes
        if library == "H5P.Image" or library == "H5P.Shape":
            return None

        # MultiChoiceElement
        elif library == "H5P.MultiChoice":
            return MultiChoiceTextElement(data)

        # DragTextElement
        elif library == "H5P.DragText":
            return DragTextElement(data)

        # DragQuestionElement

        elif library == "H5P.DragQuestion":
            return DragQuestionELement(data)


        # SingleChoiceSet
        elif library == "H5P.SingleChoiceSet":
            return SingleChoiceSetElement(data)

        # TrueFalse
        elif library == "H5P.TrueFalse":
            return TrueFalseElement(data)

        elif library == "H5P.Blanks":
            return BlanksElement(data)

        else:
            return TextElement(data)

    @abstractmethod
    def getText(self):
        pass

    @abstractmethod
    def setText(self, translated):
        pass

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
        try:
            result = hashlib.md5(text.encode('utf-8')).hexdigest()
        except Exception as e:
            result

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




class MultiChoiceTextElement(Element):
    def getText(self):
        answers = self.data['action']['params']['answers']
        text = "<answers>"
        for a in answers:
            text += "<answer><text>" + a['text'] + "</text>"
            text += "<notChosenFeedback>" + a['tipsAndFeedback']['notChosenFeedback'] + "</notChosenFeedback>"
            text += "<chosenFeedback>" + a['tipsAndFeedback']['chosenFeedback'] + "</chosenFeedback>"
            text += "<tip>" + a['tipsAndFeedback']['tip'] + "</tip>"
            text += "</answer>"
        text += "</answers>"
        text += "<question>" + self.data['action']['params']['question'] + "</question>"
        return text


    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for cnt,a in enumerate(results.findAll("answer")):
            self.data['action']['params']['answers'][cnt]['text'] = a.find('text').getText()
            self.data['action']['params']['answers'][cnt]['tipsAndFeedback']['notChosenFeedback'] = a.find('notchosenfeedback').getText()
            self.data['action']['params']['answers'][cnt]['tipsAndFeedback']['chosenFeedback'] = a.find('chosenfeedback').getText()
        self.data['action']['params']['question'] = results.find('question').getText()



class DragTextElement(Element):
    def getText(self):
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


    def setText(self, translated):
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

class DragQuestionELement(Element):
    def getText(self):
        text = "<title>" + self.data['action']['metadata']['title'] + "</title>"
        elements = self.data['action']['params']['question']['task']['elements']
        text += "<elements>"
        for e in elements:
            text += "<text>" + e['type']['params']['text'] + "</text>"
        text += "</elements>"
        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')
        self.data['action']['metadata']['title'] = results.find('title').getText()
        elements = results.find('elements')
        for cnt, t in enumerate(elements.findAll("text")):
            self.data['action']['params']['question']['task']['elements'][cnt]['type']['params']['text'] = t.getText()


class SingleChoiceSetElement(Element):
    def getText(self):
        text = "<title>" + self.data['action']['metadata']['title'] + "</title>"
        choices = self.data['action']['params']['choices']
        text += "<choices>"
        for c in choices:
            if c.get('question') is not None:
                text += "<question>"+c['question']+"</question>"
            text += "<answers>"
            if c.get('answers') is not None:
                answers = c['answers']
                for a in answers:
                    text += "<answer>"+a+"</answer>"
            text += "</answers>"
        text += "</choices>"
        return text

    def setText(self, translated):
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

class TrueFalseElement(Element):
    def getText(self):
        text = "<question>"+self.data['action']['params']['question'] +"</question>"
        text += "<confirmcheck>"
        text += "<header>" + self.data['action']['params']['confirmCheck']['header'] + "</header>"
        text += "<body>" + self.data['action']['params']['confirmCheck']['body'] + "</body>"
        text += "<cancellabel>" + self.data['action']['params']['confirmCheck']['cancelLabel'] + "</cancellabel>"
        text += "<confirmlabel>" + self.data['action']['params']['confirmCheck']['confirmLabel'] + "</confirmlabel>"
        text += "</confirmcheck>"
        text += "<confirmretry>"
        text += "<header>" + self.data['action']['params']['confirmRetry']['header'] + "</header>"
        text += "<body>" + self.data['action']['params']['confirmRetry']['body'] + "</body>"
        text += "<cancellabel>" + self.data['action']['params']['confirmRetry']['cancelLabel'] + "</cancellabel>"
        text += "<confirmlabel>" + self.data['action']['params']['confirmRetry']['confirmLabel'] + "</confirmlabel>"
        text += "</confirmretry>"
        text += "<title>"+self.data['action']['metadata']['title'] +"</title>"

        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')
        tf = results.find('question')
        if tf is not None:
            self.data['action']['params']['question'] = tf.getText()
        tf = results.find('confirmcheck')
        if tf is not None:
            self.data['action']['params']['confirmCheck']['header'] = tf.find("header").getText()
            self.data['action']['params']['confirmCheck']['body'] = tf.find("body").getText()
            self.data['action']['params']['confirmCheck']['cancelLabel'] = tf.find("cancellabel").getText()
            self.data['action']['params']['confirmCheck']['confirmLabel'] = tf.find("confirmlabel").getText()
        tf = results.find('confirmretry')
        if tf is not None:
            self.data['action']['params']['confirmRetry']['header'] = tf.find("header").getText()
            self.data['action']['params']['confirmRetry']['body'] = tf.find("body").getText()
            self.data['action']['params']['confirmRetry']['cancelLabel'] = tf.find("cancellabel").getText()
            self.data['action']['params']['confirmRetry']['confirmLabel'] = tf.find("confirmlabel").getText()

        tf = results.find('title')
        if tf is not None:
            self.data['action']['params']['title'] = tf.getText()

class BlanksElement(Element):
    def getText(self):
        text = "<title>" + self.data['action']['metadata']['title'] + "</title>"
        text += "<questions>"
        for q in self.data['action']['params']['questions']:
            text += "<question>"+q+"</question>"
        text += "</questions>"

        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')
        questions = results.find('questions')
        if questions is not None:
            for q_cnt, q in enumerate(questions.findAll("question")):
                self.data['action']['params']['questions'][q_cnt] = q.getText()

        tf = results.find('title')
        if tf is not None:
            self.data['action']['params']['title'] = tf.getText()


class TextElement(Element):
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