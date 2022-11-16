package de.thu.h5ptranslate;

public interface Element{
    Float getX();
    Float getY();
    Float getWidth();
    Float getHeight();
    String getText();
    String getContentName();
    String getFile();

    String getID();
    String getHash();
    boolean isTextElement();


}