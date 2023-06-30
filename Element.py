from bs4 import BeautifulSoup
import hashlib
import json
from abc import ABC, abstractmethod


# we wrap multi information text into html tags of type span and a given class.
# this is because google translate won't translate html tag names and we can separate the information after translating again
def tag_begin(name):
    return "<span class=" + name.lower() + ">"

def tag_end():
    return "</span>"

def tag_getAll(base, name):
    return base.findAll("span", name.lower())


def tag_get(base, name):
    return base.find("span", name.lower())


class Element(ABC):
    def __init__(self, data):
        self.data = data


    def create_element(data):
        if data.get('action', None) == None:
            return None
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
        text = tag_begin("answers")
        for a in answers:
            text += tag_begin("answer")
            text += tag_begin("text") + a['text'] + tag_end()
            text += tag_begin("notChosenFeedback") + a['tipsAndFeedback']['notChosenFeedback'] + tag_end()
            text += tag_begin("chosenFeedback") + a['tipsAndFeedback']['chosenFeedback'] + tag_begin("chosenFeedback")
            text += tag_begin("tip") + a['tipsAndFeedback']['tip'] + tag_end()
            text += tag_end()
        text += tag_end()
        text += tag_begin("question") + self.data['action']['params']['question'] + tag_end()
        return text


    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for cnt,a in enumerate(tag_getAll(results, "answer")):
            self.data['action']['params']['answers'][cnt]['text'] = tag_get(a, 'text').getText()
            self.data['action']['params']['answers'][cnt]['tipsAndFeedback']['notChosenFeedback'] = tag_get(a, 'notchosenfeedback').getText()
            self.data['action']['params']['answers'][cnt]['tipsAndFeedback']['chosenFeedback'] = tag_get(a, 'chosenfeedback').getText()
        self.data['action']['params']['question'] = tag_get(results, 'question').getText()



class DragTextElement(Element):
    def getText(self):
        feedbacks = self.data['action']['params']['overallFeedback']
        text = tag_begin("feedbacks")
        for a in feedbacks:
            fb=a.get('feedback')
            if fb is None:
                continue
            text += tag_begin("feedback") + fb + tag_end()
        text += tag_end()
        text += tag_begin("textField") + self.data['action']['params']['textField'] + tag_end()
        text += tag_begin("taskDescription") + self.data['action']['params']['taskDescription'] + tag_end()
        return text


    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for cnt,a in enumerate(tag_getAll(results, "feedbacks")):
            fb = tag_get(a, 'feedback')
            if fb is not None:
                self.data['action']['params']['overallFeedback'][cnt]['feedback'] = fb.getText()
        tf = tag_get(results, 'textfield')
        if tf is not None:
            self.data['action']['params']['textField'] = tf.getText()
        td = tag_get(results, 'taskdescription')
        if td is not None:
            self.data['action']['params']['taskDescription'] = td.getText()

class DragQuestionELement(Element):
    def getText(self):
        text = tag_begin("title") + self.data['action']['metadata']['title'] + tag_end()
        elements = self.data['action']['params']['question']['task']['elements']
        text += tag_begin("elements")
        for e in elements:
            text += tag_begin("text") + e['type']['params']['text'] + tag_end()
        text += tag_end()
        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')
        self.data['action']['metadata']['title'] = tag_get(results, 'title').getText()
        elements = tag_get(results, 'elements')
        for cnt, t in enumerate(tag_getAll(elements, "text")):
            self.data['action']['params']['question']['task']['elements'][cnt]['type']['params']['text'] = t.getText()


class SingleChoiceSetElement(Element):
    def getText(self):
        text = tag_begin("title") + self.data['action']['metadata']['title'] + tag_end()
        choices = self.data['action']['params']['choices']
        text += tag_begin("choices")
        for c in choices:
            if c.get('question') is not None:
                text += tag_begin("question")+c['question']+tag_end()
            text += tag_begin("answers")
            if c.get('answers') is not None:
                answers = c['answers']
                for a in answers:
                    text += tag_begin("answer")+a+tag_end()
            text += tag_end()
        text += tag_end()
        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')

        for q_cnt, c in enumerate(tag_getAll(results, "choices")):
            q = tag_get(c, 'question')
            if q is not None:
                self.data['action']['params']['choices'][q_cnt]['question'] = q.getText()
            for a_cnt, a in enumerate(tag_getAll(c, "answers")):
                a = tag_get(a, 'answer')
                if a is not None:
                    self.data['action']['params']['choices'][q_cnt]['answers'][a_cnt] = a.getText()

        tf = tag_get(results, 'title')
        if tf is not None:
            self.data['action']['metadata']['title'] = tf.getText()

class TrueFalseElement(Element):
    def getText(self):
        text = tag_begin("question")+self.data['action']['params']['question'] +tag_end()
        text += tag_begin("confirmcheck")
        text += tag_begin("header") + self.data['action']['params']['confirmCheck']['header'] + tag_end()
        text += tag_begin("body") + self.data['action']['params']['confirmCheck']['body'] + tag_end()
        text += tag_begin("cancellabel") + self.data['action']['params']['confirmCheck']['cancelLabel'] + tag_end()
        text += tag_begin("confirmlabel") + self.data['action']['params']['confirmCheck']['confirmLabel'] + tag_end()
        text +=tag_end()
        text += tag_begin("confirmretry")
        text += tag_begin("header") + self.data['action']['params']['confirmRetry']['header'] + tag_end()
        text += tag_begin("body") + self.data['action']['params']['confirmRetry']['body'] + tag_end()
        text += tag_begin("cancellabel") + self.data['action']['params']['confirmRetry']['cancelLabel'] + tag_end()
        text += tag_begin("confirmlabel") + self.data['action']['params']['confirmRetry']['confirmLabel'] + tag_end()
        text += tag_end()
        text += tag_begin("title")+self.data['action']['metadata']['title'] +tag_end()

        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')
        tf = tag_get(results, 'question')
        if tf is not None:
            self.data['action']['params']['question'] = tf.getText()
        tf = tag_get(results, 'confirmcheck')
        if tf is not None:
            self.data['action']['params']['confirmCheck']['header'] = tag_get(tf, "header").getText()
            self.data['action']['params']['confirmCheck']['body'] = tag_get(tf, "body").getText()
            self.data['action']['params']['confirmCheck']['cancelLabel'] = tag_get(tf, "cancellabel").getText()
            self.data['action']['params']['confirmCheck']['confirmLabel'] = tag_get(tf, "confirmlabel").getText()
        tf = tag_get(results, 'confirmretry')
        if tf is not None:
            self.data['action']['params']['confirmRetry']['header'] = tag_get(tf, "header").getText()
            self.data['action']['params']['confirmRetry']['body'] = tag_get(tf, "body").getText()
            self.data['action']['params']['confirmRetry']['cancelLabel'] = tag_get(tf, "cancellabel").getText()
            self.data['action']['params']['confirmRetry']['confirmLabel'] = tag_get(tf, "confirmlabel").getText()

        tf = results.find('title')
        if tf is not None:
            self.data['action']['params']['title'] = tf.getText()

class BlanksElement(Element):
    def getText(self):
        text = tag_begin("title") + self.data['action']['metadata']['title'] + tag_end()
        text += tag_begin("questions")
        for q in self.data['action']['params']['questions']:
            text += tag_begin("question")+q+tag_end()
        text += tag_end()

        return text

    def setText(self, translated):
        results = BeautifulSoup(translated, 'html.parser')
        questions = tag_get(results, 'questions')
        if questions is not None:
            for q_cnt, q in enumerate(tag_getAll(questions, "question")):
                self.data['action']['params']['questions'][q_cnt] = q.getText()

        tf = tag_get(results, 'title')
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