import os
import shutil

from h5p_python.h5ptranslate import H5PTranslator

h5ptrans = H5PTranslator()
ori_file = os.path.abspath(r"./data/course-presentation-36.h5p")
translate_file = os.path.abspath(r"./data/course-presentation-36_DE.h5p")


#ori_file = os.path.abspath(r"./data/course-presentation-81.h5p")
#translate_file = os.path.abspath(r"./data/course-presentation-81_DE.h5p")


#ori_file = os.path.abspath(r"./data/content.json")
#translate_file = os.path.abspath(r"./data/content_DE.json")

h5ptrans.open(ori_file, translate_file)

print("Ori temp dir: "+h5ptrans.getTemporaryDir_original())
print("Translate temp dir: "+h5ptrans.getTemporaryDir_translate())

print("Nr of slides: {}".format(h5ptrans.getNrOfSlides()))
slideNr = 0
print("Nr of Elements in slide nr. {}: {}".format(slideNr, len(h5ptrans.getElementsForSlide_original(slideNr))))
for cnt,e in enumerate(h5ptrans.getElementsForSlide_original(slideNr)):
    print("Text of element {}: {}".format(cnt, e.getText()))

modified_ids = h5ptrans.getModifiedElementIDs()
untranslated_ids = h5ptrans.getUntranslatedElementIDs()

print("Modified ids (%d): %s" %(len(modified_ids), str(modified_ids)))
print("Untranslated ids (%d): %s" %(len(untranslated_ids), str(untranslated_ids)))
#h5ptrans.setTranslation(untranslated_ids[0], "Das ist ein deutscher Text für die erste ID!")

#untranslated_ids = []
for id in untranslated_ids:
    elem = h5ptrans.getElementByID_original(id)
    print("Autotranslating id '{}': '{}'".format(id, elem.getText()))
    autotranslated_text = h5ptrans.translate_element("en", "de", id)
    print("Result: "+autotranslated_text)

src_path = r'C:\Users\micha\THU\H5PTranslator\_images'


#h5ptrans.replace_images("en", "de", r"C:\Users\micha\THU\H5PTranslator\data\images")

h5ptrans.close(True)


