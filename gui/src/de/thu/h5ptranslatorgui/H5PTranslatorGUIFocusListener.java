package de.thu.h5ptranslatorgui;

import java.awt.Color;
import java.awt.event.*;
import java.util.Vector;

/**
 * Beschreiben Sie hier die Klasse MTPFocusListener.
 * 
 * @author HG 
 * @version 29.05.2022
 */
public class H5PTranslatorGUIFocusListener implements FocusListener
{
    private Vector<H5PTranslatorGUIText> vjtf = new Vector<H5PTranslatorGUIText>();

    public void add(H5PTranslatorGUIText t, H5PTranslatorGUITextField tf1, H5PTranslatorGUITextField tf2) {
        tf1.addFocusListener(this);
        tf2.addFocusListener(this);
        vjtf.add(t);
    }
    
     public void focusGained (FocusEvent e) {
         H5PTranslatorGUITextField t = (H5PTranslatorGUITextField)e.getSource();
          
        
        if (t.getBackground() == Color.red)
            t.setBackground(Color.green);
        else
            t.setBackground(Color.red); 
        }

    public void focusLost (FocusEvent e) {
        H5PTranslatorGUITextField t = (H5PTranslatorGUITextField)e.getSource();
          
        
        if (t.getBackground() == Color.red)
            t.setBackground(Color.green);
        else
            t.setBackground(Color.red); 
    }


}
