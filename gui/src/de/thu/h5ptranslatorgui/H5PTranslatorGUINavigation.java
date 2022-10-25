package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;

public class H5PTranslatorGUINavigation extends JPanel {
    H5PTranslatorGUINavigation() {
        setBackground(Color.GRAY);
        GridLayout l = new GridLayout(20,1);
        l.setVgap(10);
        setLayout(l);

        JPanel pm = new JPanel();
        pm.add(new Button("+"));
        pm.add(new Button("-"));
        pm.setBackground(Color.GRAY);
        add(pm);

        Button b = new Button("Slide 1");
        add(b);
        add(new Button("Slide 2"));
        add(new Button("Slide 3"));
        JLabel j = new JLabel("");
        j.setBackground(b.getBackground());
        add(j); add(j);
        b.setBackground(Color.PINK);

        add(new Button("Save"));
        add(new Button("Reload"));
        add(new Button("Close"));
    }
}
