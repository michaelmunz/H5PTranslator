package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.io.IOException;

/**
 * main-Methode zu H5PTranslatorGUI
 * @author HG
 * @version 29.05.2022
 */
public class H5PTranslatorGUIStart
{
    public static void main(String[] args) throws IOException  {

        //  Create the frame on the event dispatching thread.
        SwingUtilities.invokeLater(H5PTranslatorGUIFrame::new);
    }
}