package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.H5PTranslator;
import de.thu.h5ptranslate.H5PTranslatorFactory;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Properties;

public class H5PTranslatorGUIFrame extends JFrame {

    H5PTranslatorGUINavigation h5PTranslatorGUINavigation;
    H5PTranslator h5ptrans;

    H5PTranslatorGUIFrame() {
        super("MedTec+");

        Properties props = System.getProperties();
        String pythonPath = "";
        try {
            pythonPath = new File(System.getProperty("user.dir") + "/..").getCanonicalPath();
        } catch (IOException i) {
            System.out.println("IOException");
        }

        props.setProperty("python.path", pythonPath);

        // creating the H5PAccess class using the factory design pattern
        H5PTranslatorFactory factory = new H5PTranslatorFactory();
        h5ptrans = factory.create();
        h5ptrans.open("C:\\Users\\gross\\Documents\\GitHub\\H5PTranslator\\data\\content.json", "C:\\Users\\gross\\Documents\\GitHub\\H5PTranslator\\data\\content_DE.json");

        h5PTranslatorGUINavigation = new H5PTranslatorGUINavigation(this, h5ptrans);

        JMenuBar menuBar = new JMenuBar();
        menuBar.add(new JMenu("File"));
        menuBar.add(new JMenu("Edit"));
        menuBar.add(new JMenu("Navigate"));
        menuBar.add(new JMenu("Tools"));
        setJMenuBar(menuBar);

        refresh();

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

   public void refresh() {
       JPanel pLeft = new JPanel();
       pLeft.setBackground(Color.GRAY);
       pLeft.add(h5PTranslatorGUINavigation);

       JPanel pRight = new JPanel();
       pRight.setBackground(Color.GRAY);
       pRight.add(new H5PTranslatorGUITranslate(h5ptrans, h5PTranslatorGUINavigation.getSlideNr()-1));

       JSplitPane pSplit = new JSplitPane();
       pSplit.setDividerLocation(0.15);
       pSplit.setDividerSize(1);
       pSplit.add(pLeft, JSplitPane.LEFT);
       pSplit.add(pRight, JSplitPane.RIGHT);

       getContentPane().removeAll();
       add(pSplit);
       validate();
       repaint();
   }
}
