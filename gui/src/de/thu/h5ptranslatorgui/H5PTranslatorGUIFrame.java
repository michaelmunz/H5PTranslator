package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.H5PTranslator;
import de.thu.h5ptranslate.H5PTranslatorFactory;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Properties;

public class H5PTranslatorGUIFrame extends JFrame {

    H5PTranslatorGUIFrame() {
        super("MedTec+");

        Properties props = System.getProperties();
        String pythonPath = "";
        try {
            pythonPath = new File(System.getProperty("user.dir") + "/..").getCanonicalPath();
        } catch (IOException i) {
        }
        System.out.println("Setting python.path to: "+pythonPath);
        props.setProperty("python.path", pythonPath);

        // creating the H5PAccess class using the factory design pattern
        H5PTranslatorFactory factory = new H5PTranslatorFactory();
        H5PTranslator h5ptrans = factory.create();

        h5ptrans.open("U:\\source\\MedTec\\H5PTranslator\\data\\course-presentation-36.h5p", "U:\\source\\MedTec\\H5PTranslator\\data\\course-presentation-36_DE.h5p");

        System.out.println("Anfang vom Öffnen");





        JMenuBar menuBar = new JMenuBar();
        menuBar.add(new JMenu("File"));
        menuBar.add(new JMenu("Edit"));
        menuBar.add(new JMenu("Navigate"));
        menuBar.add(new JMenu("Tools"));
        setJMenuBar(menuBar);

        JPanel pLeft = new JPanel();
        pLeft.setBackground(Color.GRAY);
        pLeft.add(new H5PTranslatorGUINavigation(h5ptrans));

        JPanel pRight = new JPanel();
        pRight.setBackground(Color.GRAY);
        pRight.add(new H5PTranslatorGUITranslate(h5ptrans));

        JSplitPane pSplit = new JSplitPane();
        pSplit.setDividerLocation(0.15);
        pSplit.setDividerSize(1);
        pSplit.add(pLeft, JSplitPane.LEFT);
        pSplit.add(pRight, JSplitPane.RIGHT);
        add(pSplit);

        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent e) {
                h5ptrans.close(false);
                System.exit(0);
            }
        });

        setResizable(false);
        setSize(1980, 1024);
        setVisible(true);
    }

    void newSlide(int slideNr) {

    }
}
