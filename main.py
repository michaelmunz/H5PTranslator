import os

from h5ptranslate.h5ptranslate import H5PTranslator, H5PTranslatorImpl

h5ptrans = H5PTranslatorImpl()
ori_file = os.path.abspath(r"./data/course-presentation-36_DE.h5p")
translate_file = os.path.abspath(r"./data/course-presentation-36_EN.h5p")

h5ptrans.open(ori_file, translate_file)

print("Ori temp dir: "+h5ptrans.getTemporaryDir_original())
print("Translate temp dir: "+h5ptrans.getTemporaryDir_translate())

print("Nr of slides: {}".format(h5ptrans.getNrOfSlides()))
slideNr = 1
print("Nr of Elements in slide nr. {}: {}".format(slideNr, h5ptrans.getNrOfElementsForSlide(slideNr)))
#print("Text of first element: {}".format(h5ptrans.getElementsForSlide_original(slideNr)[0].getText()))


modified_ids = h5ptrans.getModifiedElementIDs()
untranslated_ids = h5ptrans.getUntranslatedElementIDs()

print("Modified ids: "+str(modified_ids))
print("Untranslated ids: "+str(untranslated_ids))
h5ptrans.setTranslation(untranslated_ids[0], "This is an english test for the first id!")
h5ptrans.close(True)
