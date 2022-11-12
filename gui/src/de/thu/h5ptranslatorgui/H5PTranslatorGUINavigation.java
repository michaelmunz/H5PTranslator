package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.Arrays;
import java.util.List;

public class H5PTranslatorGUINavigation extends JPanel implements ActionListener {

    Button slideNrButton;

    JComboBox<String> languageIn, languageOut;

    List<String> fileOperations = Arrays.asList("Load", "Reload", "Save", "Close App", "Image Path");

    H5PTranslatorGUIFrame GUIFrame;

    String inFile, outFile;

    H5PTranslatorGUINavigation(H5PTranslatorGUIFrame GUIFrame) {

        this.GUIFrame = GUIFrame;
        setBackground(Color.GRAY);
        GridLayout l = new GridLayout(0, 2);
        l.setVgap(10);
        setLayout(l);

        languageIn = new JComboBox<>(GUIFrame.getLanguages());
        languageIn.setSelectedIndex(GUIFrame.getSelectedInLanguage());
        add(new Label("Orig. Language"));
        languageIn.addActionListener(this);
        add(languageIn);

        languageOut = new JComboBox<>(GUIFrame.getLanguages());
        languageOut.setSelectedIndex(GUIFrame.getSelectedOutLanguage());
        add(new Label("Trans. Language"));
        languageOut.addActionListener(this);
        add(languageOut);

        emptyLine(2);

        int i;
        Button b;
            for (i = 1; i < GUIFrame.getH5ptrans().getNrOfSlides(); i++) {
                b = new Button("Slide " + i);
                b.addActionListener(this);
                if (i == GUIFrame.getSlideNr()) {
                    b.setBackground(Color.PINK);
                    slideNrButton =  b;
                }
                else
                    b.setBackground(Color.LIGHT_GRAY);
                add(b);
            }
            if (i % 2 == 0) {
                Label label = new Label();
                label.setBackground(getBackground());
                add(label);
            }

            emptyLine(2);

        for (i = 0; i < fileOperations.size(); i++) {
            b = new Button(fileOperations.get(i));
            b.addActionListener(this);
            b.setBackground(Color.LIGHT_GRAY);
            add(b);
        }

    }

    public void emptyLine(int anzahl) {
        for (int i = 0; i < 2 * anzahl; i++)
            add(new Label());
    }

     @Override
    public void actionPerformed(ActionEvent e) {

        if (e.getSource() == languageIn) {
            GUIFrame.setSelectedInLanguage(languageIn.getSelectedIndex());
            return;
        }

        if (e.getSource() == languageOut) {
            GUIFrame.setSelectedOutLanguage(languageOut.getSelectedIndex());
            return;
        }

        Button b = (Button) (e.getSource());

        if (fileOperations.contains(b.getLabel())) {
            doFileOperations(b.getLabel());
            return;
        }

        slideNrButton.setBackground(Color.LIGHT_GRAY);

        b.setBackground(Color.PINK);
        GUIFrame.setSlideNr(Integer.parseInt(b.getLabel().substring(6)));
        slideNrButton = b;
        GUIFrame.paintNew();
    }

    private void doFileOperations(String s) {
        int dialogButton = JOptionPane.YES_NO_OPTION;
        int dialogResult;
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setCurrentDirectory(GUIFrame.getCurrentDirectory());
        int result;
        switch (s) {
            case "Load":
                result = fileChooser.showOpenDialog(this);
                if (result == JFileChooser.APPROVE_OPTION) {
                    File selectedFile = fileChooser.getSelectedFile();
                    GUIFrame.setCurrentDirectory(fileChooser.getCurrentDirectory());
                    inFile = selectedFile.getAbsolutePath();
                    int i = inFile.indexOf('_');
                    outFile = inFile.substring(0, i + 1) + GUIFrame.getLanguageOut() + ".json";
                    GUIFrame.getH5ptrans().open(inFile, outFile);
                    GUIFrame.setInFile(inFile);
                    GUIFrame.setOutFile(outFile);
                    GUIFrame.setFileOpen(true);
                    GUIFrame.paintNew();
                }
                break;
            case "Reload":
                dialogResult = JOptionPane.showConfirmDialog(null, "Would You like to reload the original file (ALL YOUR CURRENT CHANGES WILL BE LOST)?", "Closing", dialogButton);
                if (dialogResult == JOptionPane.YES_OPTION) {
                    GUIFrame.getH5ptrans().close(false);
                    GUIFrame.getH5ptrans().open(GUIFrame.getInFile(), GUIFrame.getOutFile());
                    GUIFrame.paintNew();
                }
                break;
            case "Save":
                dialogResult = JOptionPane.showConfirmDialog(null, "Would You like to save your chances?", "Saving", dialogButton);
                if (dialogResult == JOptionPane.YES_OPTION) {
                    GUIFrame.getH5ptrans().close(true);
                    GUIFrame.getH5ptrans().open(GUIFrame.getInFile(), GUIFrame.getOutFile());
                    GUIFrame.paintNew();
                }
                break;
            case "Close App":
                dialogResult = JOptionPane.showConfirmDialog(null, "Would You like to close the application (DID YOU SAVE YOUR CHANGES ALREADY?)", "Closing", dialogButton);
                if (dialogResult == JOptionPane.YES_OPTION) {
                    if (GUIFrame.isFileOpen())
                        GUIFrame.getH5ptrans().close(false);
                    System.exit(0);
                }
                break;
            case "Image Path":
                result = fileChooser.showOpenDialog(this);
                if (result == JFileChooser.APPROVE_OPTION) {
                    GUIFrame.getH5ptrans().setTranslatedImages(fileChooser.getCurrentDirectory().toString());
                }

                break;
            default:
                break;
        }
    }

}

