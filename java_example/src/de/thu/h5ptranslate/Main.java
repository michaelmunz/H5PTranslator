package de.thu.h5ptranslate;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Properties;


public class Main {

    public static void main(String[] args) throws IOException {
        // setting of the python path
        Properties props = System.getProperties();
        String pythonPath = new File(System.getProperty("user.dir")+"/../").getCanonicalPath();
        System.out.println("Setting python.path to: "+pythonPath);
        props.setProperty("python.path", pythonPath);
        String syspath = props.getProperty("sys.path");
        syspath+= "; "+new File(System.getProperty("user.dir")+"/../env/").getCanonicalPath();
        props.setProperty("sys.path", syspath);


        // creating the H5PAccess class using the factory design pattern
        H5PTranslatorFactory factory = new H5PTranslatorFactory();
        H5PTranslator h5ptrans = factory.create();

        // initialize the accessor
        h5ptrans.open("C:\\Users\\micha\\THU\\H5PTranslator\\data\\course-presentation-58.h5p", "C:\\Users\\micha\\THU\\H5PTranslator\\data\\course-presentation-58_DE.h5p");
        System.out.println("Nr of slides: "+h5ptrans.getNrOfSlides());
        int slideNr = 1;
        System.out.println("Nr of elements for slide 1: "+h5ptrans.getElementsForSlide_original(slideNr).size());
        List<Element> elList = h5ptrans.getElementsForSlide_original(slideNr);
        //System.out.println("Text of first element of slide 1: "+elList.get(0).getText());

        List<String> untranslated_element_ids = h5ptrans.getUntranslatedElementIDs();
        System.out.println("We have "+untranslated_element_ids.size()+" untranslated elements.");

        h5ptrans.setTranslation(untranslated_element_ids.get(0), "This is an english test for the first id!");

        Element element = h5ptrans.getElementByID_original(untranslated_element_ids.get(0));

        String autotranslated = h5ptrans.getAutoTranslation("en", "de", element.getText());
        System.out.println("Auto translated: "+autotranslated);


        h5ptrans.close(true);

    }
}