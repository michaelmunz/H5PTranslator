package de.thu.h5ptranslate;


import java.util.List;

public interface H5PTranslator {
    boolean open(String ori_file, String translate_file);
    void close(boolean write_changes);

    List<String> getUntranslatedElementIDs();
    List<String> getTranslatedElementIDs();
    List<String> getModifiedElementIDs();

    int getNrOfSlides();

    List<Element> getElementsForSlide_original(int nrSlide);
    List<Element> getElementsForSlide_translate(int nrSlide);

    String getTemporaryDir_original();
    String getTemporaryDir_translate();

    void setTranslation(String id, String text_translated);


}
