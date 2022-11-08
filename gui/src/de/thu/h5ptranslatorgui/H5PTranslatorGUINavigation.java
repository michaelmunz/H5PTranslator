package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class H5PTranslatorGUINavigation extends JPanel implements ActionListener {

    int slideNr = 1;
    Button slideNrButton;
    static String[] languages = {"en", "de", "hu"};

    JComboBox<String> languageIn, languageOut ;
    String languageInString = "en", languageOutString = "en";


    H5PTranslatorGUIFrame GUIFrame;
     H5PTranslatorGUINavigation(H5PTranslatorGUIFrame GUIFrame)  {

        this.GUIFrame = GUIFrame;
        setBackground(Color.GRAY);
        GridLayout l = new GridLayout(20,1);
        l.setVgap(10);
        setLayout(l);

         languageIn = new JComboBox<>(languages);
         add(new Label("Orig. Language"));
         languageIn.addActionListener(this);
         add(languageIn);

         languageOut = new JComboBox<>(languages) ;
         add(new Label("Trans. Language"));
         languageOut.addActionListener(this);
         add(languageOut);

         emptyLine(2);

        Button b = new Button("Slide 1");
        b.setBackground(Color.PINK);
        b.addActionListener(this);
        add(b);
        slideNrButton = b;
        for (int i = 2; i < GUIFrame.getH5ptrans().getNrOfSlides(); i++) {
            b = new Button("Slide " + i);
            b.addActionListener(this);
            b.setBackground(Color.LIGHT_GRAY);
            add(b);
        }

        emptyLine(2);

        add(new Button("Save"));
        add(new Button("Reload"));
        add(new Button("Close"));
    }

    public void emptyLine(int anzahl) {
         for (int i = 0; i < 2*anzahl; i++)
             add(new Label());
    }

    public int getSlideNr()  {
         return slideNr;
    }

    public String getLanguageIn()  {
        return languageInString;
    }

    public String getLanguageOut()  {
        return languageOutString;
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        if (e.getSource() == languageIn) {
            languageInString = languageIn.getSelectedItem().toString();
            return;
        }

        if (e.getSource() == languageOut) {
            languageOutString = languageOut.getSelectedItem().toString();
            return;
        }

        slideNrButton.setBackground(Color.LIGHT_GRAY);

        Button b = (Button)(e.getSource());
        b.setBackground(Color.PINK);
        slideNr = Integer.parseInt(b.getLabel().substring(6));
        slideNrButton = b;
        GUIFrame.refresh();
    }
}

