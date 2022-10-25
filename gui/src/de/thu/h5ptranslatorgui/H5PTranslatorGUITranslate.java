package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.Element;
import de.thu.h5ptranslate.H5PTranslator;

import javax.swing.*;
import java.awt.*;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.util.List;

public class H5PTranslatorGUITranslate extends JPanel implements FocusListener {

    HTMLDocumentEditor htmlDE;
    boolean htmlDocumentEditorShown = false;
    H5PTranslator h5ptrans;

    H5PTranslatorGUITranslate(H5PTranslator h5ptrans) {

        this.h5ptrans = h5ptrans;

        setLayout(new GridLayout2(4,6, 15, 10));
        setSize(1280,1024);
        setBackground(Color.GRAY);

        int nrOfSlides = h5ptrans.getNrOfSlides(), slideNr = 1;
        int nrOfElements = h5ptrans.getElementsForSlide_original(slideNr).size();
        List<Element> origList = h5ptrans.getElementsForSlide_original(slideNr);
        List<Element> transList = h5ptrans.getElementsForSlide_translate(slideNr);

        tAddHeader();



        // System.out.println("Text of first element of slide 1: "+elList.get(0).getText());
        // java.util.List<String> untranslated_element_ids = h5ptrans.getUntranslatedElementIDs();
        // System.out.println("We have "+untranslated_element_ids.size()+" untranslated elements.");
        // h5ptrans.setTranslation(untranslated_element_ids.get(0), "This is an english test for the first id!");


       // for (int i=0; i < nrOfElements; i++)
       //    tAdd(new String[] { origList.get(i).getID() , transList.get(i).getText(), "aaa","23.56","4.234"});
       //  tAdd(new String[] {"511",origList.get(0).getText(),"aaa","6.41","477.4"});
        // tAdd(new String[] { "111", "Hello", "Hallo","23.56","4.234"});
        tAdd(new String[] {"41235","World","Welt","3.641","40.24"});
    }

    static int[] widthColumns = {50, 300, 300, 80, 100, 100};
    static int heightColumns = 100;

    private void increaseCounter() {
        counterComponents++;
        if (counterComponents == 6)
            counterComponents = 0;
    }
    static int counterComponents = 0;
    private void tAdd (String s) {
        JLabel c = new JLabel(s);
        tAdd(c);
    }
    private void tAdd (Component c) {
        c.setPreferredSize(new Dimension(widthColumns[counterComponents],heightColumns));
        add(c);
        increaseCounter();
    }

    private void tAdd (String[] s) {
        tAdd(s[0]);
/*
        int k = s[1].length();
        if (k > 9) {
            tAdd(s[1].substring(0, 10));
            System.out.println(s[1].substring(0, 10));
        }
        else  */
           tAdd(s[1]);

        JTextField j = new JTextField(s[2]);
        j.addFocusListener(this);
        j.setEditable(false);
        tAdd(j);

        tAdd(new Button("Auto"));
        tAdd(s[3]);
        tAdd(s[4]);
    }

    private void tAddHeader () {
        tAdd("id");
        tAdd("English");
        tAdd("German");
        tAdd("DeepL");
        tAdd("x-coordinate");
        tAdd("y-coordinate");
    }

    public void closedHTMLDE() {
        htmlDocumentEditorShown = false;
    }

    @Override
    public void focusGained(FocusEvent e) {
        if (!htmlDocumentEditorShown) {
            JTextField j = (JTextField) e.getComponent();
            j.setBackground(Color.PINK);
            htmlDE = new HTMLDocumentEditor(this, j);
            htmlDocumentEditorShown = true;
        }
        this.requestFocus();
        htmlDE.requestFocus();
    }

    @Override
    public void focusLost(FocusEvent e) {

    }
}



