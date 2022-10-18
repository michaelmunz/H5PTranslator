import os

from h5ptranslate.h5ptranslate import H5PTranslator, H5PTranslatorImpl

h5ptrans = H5PTranslatorImpl()
ori_file = os.path.abspath(r"./data/Medical Device Regulation - overview.h5p")
translate_file = os.path.abspath(r"./data/Medical Device Regulation - overview_DE.h5p")

h5ptrans.open(ori_file, translate_file)

print("Ori temp dir: "+h5ptrans.getTemporaryDir_original())
print("Translate temp dir: "+h5ptrans.getTemporaryDir_translate())

print("Nr of slides: {}".format(h5ptrans.getNrOfSlides()))
slideNr = 1
print("Nr of Elements in slide nr. {}: {}".format(slideNr, len(h5ptrans.getElementsForSlide_original(slideNr))))
#print("Text of first element: {}".format(h5ptrans.getElementsForSlide_original(slideNr)[0].getText()))


modified_ids = h5ptrans.getModifiedElementIDs()
untranslated_ids = h5ptrans.getUntranslatedElementIDs()

print("Modified ids (%d): %s" %(len(modified_ids), str(modified_ids)))
print("Untranslated ids (%d): %s" %(len(untranslated_ids), str(untranslated_ids)))
h5ptrans.setTranslation(untranslated_ids[0], "Das ist ein deutscher Text für die erste ID!")

id_autotrans = untranslated_ids[1]
elem = h5ptrans.getElementByID_original(id_autotrans)
print("Autotranslating id %d: '%s'".format(id_autotrans, elem.getText()))
autotranslated_test = h5ptrans.getAutoTranslation("en", "de", elem.getText())
print("Result: "+autotranslated_test)
h5ptrans.setTranslation(untranslated_ids[1], autotranslated_test)

src_path = r'C:\Users\micha\THU\H5PTranslator\_images'
h5ptrans.setTranslatedImages(src_path)

h5ptrans.close(True)


