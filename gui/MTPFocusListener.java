import java.awt.Color;
import java.awt.event.*;
import java.util.Vector;

/**
 * Beschreiben Sie hier die Klasse MTPFocusListener.
 * 
 * @author HG 
 * @version 29.05.2022
 */
public class MTPFocusListener implements FocusListener 
{
    private Vector<MTPText> vjtf = new Vector<MTPText>();

    public void add(MTPText t, MTPTextField tf1, MTPTextField tf2) {
        tf1.addFocusListener(this);
        tf2.addFocusListener(this);
        vjtf.add(t);
    }
    
     public void focusGained (FocusEvent e) {
         MTPTextField t = (MTPTextField)e.getSource();
          
        
        if (t.getBackground() == Color.red)
            t.setBackground(Color.green);
        else
            t.setBackground(Color.red); 
        }

    public void focusLost (FocusEvent e) {
        MTPTextField t = (MTPTextField)e.getSource();
          
        
        if (t.getBackground() == Color.red)
            t.setBackground(Color.green);
        else
            t.setBackground(Color.red); 
    }


}
