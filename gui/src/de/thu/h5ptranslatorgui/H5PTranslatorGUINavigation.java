package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;

public class H5PTranslatorGUINavigation extends JPanel {
    H5PTranslatorGUINavigation() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        setSize(100,600);

        JPanel pm = new JPanel();
        pm.setLayout(new BoxLayout(pm, BoxLayout.X_AXIS));
        pm.add(new Button("+"));
        pm.add(new Button("-"));
        add(pm);

        add(new JLabel("-"));
        Button b = new Button("Slide 1");
        b.setBackground(Color.lightGray);
        add(b);
        add(new JLabel("-"));
        add(new Button("Slide 2"));
        add(new JLabel("-"));
        add(new Button("Slide 3"));
        add(new JLabel("-"));

        add(new Button("Save"));
        add(new Button("Reload"));
        add(new Button("Close"));
    }
}
