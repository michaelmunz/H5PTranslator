package de.thu.h5ptranslatorgui;

import javax.swing.SwingUtilities;

/**
 * main-Methode zu MTP
 * @author HG
 * @version 29.05.2022
 */
public class H5PTranslatorGUIStart
{
    public static void main(String[] args) {
        // Create the frame on the event dispatching thread.
        SwingUtilities.invokeLater(() -> {
            H5PTranslatorGUIText t1 = new H5PTranslatorGUIText("Hello", "Hallo"),
            t2 = new H5PTranslatorGUIText("world!", "Welt");

            H5PTranslatorGUIPanelText[] tf = {new H5PTranslatorGUIPanelText(t1), new H5PTranslatorGUIPanelText(t2)};
            new H5PTranslatorGUIFrame();
        });
    }
}