package de.thu.h5ptranslatorgui;

public class H5PTranslatorGUIText
{
    private String orig, trans;

    /**
     * Konstruktor für Objekte der Klasse MTPText
     */
    String getOrig() {
        return orig;
    }
    
    String getTrans() {
        return trans;
    }
    
    public H5PTranslatorGUIText(String s)
    {
        orig = s;
    }
    public H5PTranslatorGUIText(String s1, String s2)
    {
        this(s1);
        trans = s2;
    }
    

}
