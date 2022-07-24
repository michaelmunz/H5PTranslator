package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;


public class H5PTranslatorGUITranslate extends JPanel {
    H5PTranslatorGUITranslate() {
        setLayout(new GridLayout2(4,6, 15, 10));
        setSize(800,600);
        setBackground(Color.GRAY);

        tAddHeader();
        tAdd(new String[] {"234","Hello","Hallo","23.56","4.234"});
        tAdd(new String[] {"41235","World","Welt","3.641","40.24"});
        tAdd(new String[] {"511","MTP!","MTP!","6.41","477.4"});
    }

    static int[] widthColumns = {50, 300, 300, 80, 100, 100};
    static int heightColumns = 50;

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
        tAdd(s[1]);
        tAdd(new JTextField(s[2]));
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

}



