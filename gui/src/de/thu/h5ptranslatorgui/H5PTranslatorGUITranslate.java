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

    static int[] widthColumns = {250, 310, 310, 80, 100, 100};
    static int heightColumns = 50;

    H5PTranslatorGUITranslate(H5PTranslator h5ptrans, int slideNr) {

        this.h5ptrans = h5ptrans;

        int nrOfElements = h5ptrans.getElementsForSlide_original(slideNr).size();
        List<Element> origList = h5ptrans.getElementsForSlide_original(slideNr);
        List<Element> transList = h5ptrans.getElementsForSlide_translate(slideNr);

        int nrRows = nrOfElements+1;
        setLayout(new GridLayout2(nrRows, 6, 15, 10));

        // setSize(1920, 1080);
        setBackground(Color.GRAY);

        tAddHeader();
        for (int i = 0; i < nrOfElements; i++) {
            Element aktElement = origList.get(i);
            tAdd(new String[]{aktElement.getID(),
                    aktElement.getText(),
                    transList.get(i).getText(),
                    "2",
                    "3"});
        }
    }

    private void increaseCounter() {
        counterComponents++;
        if (counterComponents == 6)
            counterComponents = 0;
    }

    int counterComponents = 0;

    private void tAdd(String s) {
        JLabel c = new JLabel(s);
        tAdd(c);
    }

    private void tAdd(Component c) {
        c.setPreferredSize(new Dimension(widthColumns[counterComponents], heightColumns));
        add(c);
        increaseCounter();
    }

    private void tAdd(String[] s) {
        tAdd(s[0]);
        tAdd(s[1]);

        JTextField j = new JTextField(s[2]);
        j.addFocusListener(this);
        j.setEditable(false);
        tAdd(j);

        tAdd(new Button("Auto"));
        tAdd(s[3]);
        tAdd(s[4]);
    }

    private void tAddHeader() {
        tAdd("id");
        tAdd("English");
        tAdd("German");
        tAdd("Google Translator");
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
        JTextField j = (JTextField) e.getComponent();
        j.setBackground(null);
    }
}



