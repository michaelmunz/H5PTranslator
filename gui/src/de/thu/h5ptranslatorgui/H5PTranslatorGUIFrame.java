package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.H5PTranslator;
import de.thu.h5ptranslate.H5PTranslatorFactory;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Properties;

/**
 * Die MTP-GUI
 * 
 * @author HG
 * @version 29.05.2022
 */
public class H5PTranslatorGUIFrame extends JFrame
{

     H5PTranslatorGUIFrame()  {
        super("MedTec+");

         Properties props = System.getProperties();
         String pythonPath ="";
         try {
             pythonPath = new File(System.getProperty("user.dir") + "/..").getCanonicalPath();
         }
         catch (IOException i)
         {}

         props.setProperty("python.path", pythonPath);

         // creating the H5PAccess class using the factory design pattern
         H5PTranslatorFactory factory = new H5PTranslatorFactory();
         H5PTranslator h5ptrans = factory.create();

         // initialize the accessor
         h5ptrans.open("C:\\Users\\gross\\Documents\\GitHub\\H5PTranslator\\course-presentation-36_DE.h5p", "C:\\Users\\gross\\Documents\\GitHub\\H5PTranslator\\course-presentation-36_EN.h5p");

        JMenuBar menuBar = new JMenuBar();
        menuBar.add(new JMenu("File"));
        menuBar.add(new JMenu("Edit"));
        menuBar.add(new JMenu("Navigate"));
        menuBar.add(new JMenu("Tools"));
        setJMenuBar(menuBar);

        JPanel pLeft = new JPanel();
        pLeft.setBackground(Color.GRAY);
        pLeft.add(new H5PTranslatorGUINavigation());

        JPanel pRight = new JPanel();
        pRight.setBackground(Color.GRAY);
        pRight.add(new H5PTranslatorGUITranslate(h5ptrans));

        JSplitPane pSplit = new JSplitPane();
        pSplit.setDividerLocation(0.25);
        pSplit.setDividerSize(1);
        pSplit.add(pLeft, JSplitPane.LEFT);
        pSplit.add(pRight, JSplitPane.RIGHT);
        add(pSplit);

       // setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         addWindowListener(new java.awt.event.WindowAdapter() {
             public void windowClosing(java.awt.event.WindowEvent e) {
                 h5ptrans.close(false);
                 System.exit(0);
             }
         });

        setResizable(false);
        setSize(1200,800);
        setVisible(true);
    }
}
