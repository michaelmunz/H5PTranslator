import javax.swing.*;

/**
 * Beschreiben Sie hier die Klasse MTPPanelText.
 * 
 * @author HG   
 * @version 30.05.2022
 */

public class MTPPanelText extends MTPPanel
{
    private MTPTextField orig, trans;
    private MTPFocusListener fl = new MTPFocusListener();
        
    MTPPanelText(MTPText t) {
        super();
        orig = new MTPTextField(t.getOrig(), t);
        trans = new MTPTextField(t.getTrans(), t);
        add(orig);
        add(trans);
        fl.add(t, orig, trans);
   }
}
