package de.thu.h5ptranslatorgui;

import javax.swing.*;

/**
 * Die MTP-GUI
 * 
 * @author HG
 * @version 29.05.2022
 */
public class H5PTranslatorGUIFrame extends JFrame
{

    H5PTranslatorGUIFrame() {
        // Create a new JFrame container.
        super("MedTec+");         

       setLayout(new BoxLayout(getContentPane(), BoxLayout.X_AXIS));
       add (new H5PTranslatorGUINavigation());
       add (new H5PTranslatorGUITranslate());
       add (new H5PTranslatorGUICoordinates());

       // Terminate the program when the user closes the application.
       setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Display the frame.
        setSize(800,600);
        setVisible(true);
    }
}
