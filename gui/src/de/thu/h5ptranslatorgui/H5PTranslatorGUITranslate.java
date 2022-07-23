package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;

public class H5PTranslatorGUITranslate extends JPanel {
    H5PTranslatorGUITranslate() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        setSize(400,600);

        JPanel c1 = new JPanel();
        c1.setLayout(new BoxLayout(c1, BoxLayout.X_AXIS));
        c1.add(new JLabel("id English                          German                  "));
        add(c1);

        JPanel c2 = new JPanel();
        c2.setLayout(new BoxLayout(c2, BoxLayout.X_AXIS));
        c2.add(new JLabel("234"));
        c2.add(new TextField("Hello"));
        c2.add(new TextField("Hallo"));
        c2.add(new Button("T"));
        add(c2);
        add(new JLabel("-"));

        JPanel c3 = new JPanel();
        c3.setLayout(new BoxLayout(c3, BoxLayout.X_AXIS));
        c3.add(new JLabel("234"));
        c3.add(new TextField("World"));
        c3.add(new TextField("Welt"));
        c3.add(new Button("T"));
        add(c3);
        add(new JLabel("-"));

        JPanel c4 = new JPanel();
        c4.setLayout(new BoxLayout(c4, BoxLayout.X_AXIS));
        c4.add(new JLabel("234"));
        c4.add(new TextField("MTP!"));
        c4.add(new TextField("MTP!"));
        c4.add(new Button("T"));
        add(c4);
        add(new JLabel("-"));

    }
}



