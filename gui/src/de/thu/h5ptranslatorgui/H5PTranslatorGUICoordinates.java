package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;

public class H5PTranslatorGUICoordinates extends JPanel {
    H5PTranslatorGUICoordinates() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        setSize(100,600);
        add(new JLabel("Coordinates                           "));

        JPanel c1 = new JPanel();
        c1.setLayout(new BoxLayout(c1, BoxLayout.X_AXIS));
        c1.add(new TextField("x: 23.67"));
        c1.add(new TextField("y: 33.47"));
        add(c1);
        add(new JLabel("-"));

        JPanel c2 = new JPanel();
        c2.setLayout(new BoxLayout(c2, BoxLayout.X_AXIS));
        c2.add(new TextField("x: 23.67"));
        c2.add(new TextField("y: 33.47"));
        add(c2);
        add(new JLabel("-"));

        JPanel c3 = new JPanel();
        c3.setLayout(new BoxLayout(c3, BoxLayout.X_AXIS));
        c3.add(new TextField("x: 23.67"));
        c3.add(new TextField("y: 33.47"));
        add(c3);
        add(new JLabel("-"));
    }
}

