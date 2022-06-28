package de.thu.h5paccess;


import java.util.List;

public interface H5PAccess {
    boolean initialize(String file);
    int getNrOfSlides();
    int getNrOfElementsForSlide(int slideNr);
    List<Element> getElementsForSlide(int slideNr);




}
