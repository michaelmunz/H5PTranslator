from h5paccess import H5PAccessImpl

h5pa = H5PAccessImpl()
h5pa.initialize(r"C:\Users\micha\Desktop\H5PTranslator\data\course-presentation-36.h5p")
print("Nr of slides: {}".format(h5pa.getNrOfSlides()))
slideNr = 1
print("Nr of Elements in slide nr. {}: {}".format(slideNr, h5pa.getNrOfElementsForSlide(slideNr)))
print("Text of first element: {}".format(h5pa.getElementsForSlide(slideNr)[0].getText()))
