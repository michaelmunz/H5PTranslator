import shutil

import os
import hashlib

import h5p_python.TemporaryDirectory
import h5p_python.autotranslate

import h5p_python.zipfile2 as zip
import h5p_python.H5PAccess

class H5PTranslator():
    def __init__(self):
        self.access_ori = h5p_python.H5PAccess()
        self.access_translate = h5p_python.H5PAccess()
        h5p_python.TemporaryDirectory.cleanup_tempdirs()
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