package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.H5PTranslator;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class H5PTranslatorGUINavigation extends JPanel implements ActionListener {

    int slideNr = 1;
    H5PTranslatorGUIFrame h5PTranslatorGUIFrame;

     H5PTranslatorGUINavigation(H5PTranslatorGUIFrame h5PTranslatorGUIFrame, H5PTranslator h5ptrans)  {

        this.h5PTranslatorGUIFrame = h5PTranslatorGUIFrame;
        setBackground(Color.GRAY);
        GridLayout l = new GridLayout(20,1);
        l.setVgap(10);
        setLayout(l);

        Button b = new Button("Slide 1");
        b.setBackground(Color.PINK);
        b.addActionListener(this);
        add(b);
        for (int i = 2; i < h5ptrans.getNrOfSlides(); i++) {
            b = new Button("Slide " + i);
            b.addActionListener(this);
            b.setBackground(Color.LIGHT_GRAY);
            add(b);
        }

        JLabel j = new JLabel("");
        j.setBackground(b.getBackground());
        add(j); add(j);


        add(new Button("Save"));
        add(new Button("Reload"));
        add(new Button("Close"));
    }

    public int getSlideNr()  {
         return slideNr;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        for (Component component : this.getComponents())
            component.setBackground(Color.LIGHT_GRAY);
        Button b = (Button)(e.getSource());
        b.setBackground(Color.PINK);
        slideNr = Integer.parseInt(b.getLabel().substring(6));
        h5PTranslatorGUIFrame.refresh();
    }
}
