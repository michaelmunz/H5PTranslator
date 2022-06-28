package de.thu.h5paccess;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Properties;


public class Main {

    public static void main(String[] args) throws IOException {
        // setting of the python path
        Properties props = System.getProperties();
        String pythonPath = new File(System.getProperty("user.dir")+"/..").getCanonicalPath();
        props.setProperty("python.path", pythonPath);

        // creating the H5PAccess class using the factory design pattern
        H5PAccessFactory factory = new H5PAccessFactory();
        H5PAccess h5paccess = factory.create();

        // initialize the accessor
        h5paccess.initialize("C:\\Users\\micha\\Desktop\\H5PTranslator\\data\\course-presentation-36.h5p");
        System.out.println("Nr of slides: "+h5paccess.getNrOfSlides());
        int slideNr = 1;
        System.out.println("Nr of elements for slide 1: "+h5paccess.getNrOfElementsForSlide(slideNr));
        List<Element> elList = h5paccess.getElementsForSlide(slideNr);
        System.out.println("Text of first element of slide 1: "+elList.get(0).getText());


    }
}