/**
 * Beschreiben Sie hier die Klasse MTPText.
 * 
 * @author HG
 * @version 29.05.2022
 */
public class MTPText
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
    
    public MTPText(String s)
    {
        orig = s;
    }
    public MTPText(String s1, String s2)
    {
        this(s1);
        trans = s2;
    }
    

}
