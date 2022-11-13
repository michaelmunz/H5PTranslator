package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.Element;
import de.thu.h5ptranslate.H5PTranslator;

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

    List<String> fileOperations = Arrays.asList("Load", "Reload", "Save", "Close App", "Image Path", "AutoTranslate All");

    H5PTranslatorGUIFrame GUIFrame;
    H5PTranslator h5ptrans;

    String inFile, outFile;

    H5PTranslatorGUINavigation(H5PTranslatorGUIFrame GUIFrame) {

        this.GUIFrame = GUIFrame;
        h5ptrans = GUIFrame.getH5ptrans();
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
        Button button ;
        for (i = 1; i < h5ptrans.getNrOfSlides(); i++) {
            button = new Button("Slide " + i);
            button.addActionListener(this);
            if (i == GUIFrame.getSlideNr()) {
                button.setBackground(Color.PINK);
                slideNrButton = button;
            } else
                button.setBackground(Color.LIGHT_GRAY);
            add(button);
        }
        if (i % 2 == 0) {
            Label label = new Label();
            label.setBackground(getBackground());
            add(label);
        }
        emptyLine(2);

        for (i = 0; i < fileOperations.size(); i++) {
            button = new Button(fileOperations.get(i));
            button.addActionListener(this);
            button.setBackground(Color.LIGHT_GRAY);
            add(button);
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
          switch (s) {
            case "Load":
                loadFile();
                break;
            case "Reload":
                reloadFile();
                break;
            case "Save":
                saveFile();
                break;
            case "Close App":
                closeApp();
                break;
            case "Image Path":
                setImagePath();
                break;
            case "AutoTranslate All":
                autoTranslateAll();
                break;
            default:
                break;
        }
    }

    private void autoTranslateAll() {
        int dialogButton = JOptionPane.YES_NO_OPTION, dialogResult;
        dialogResult = JOptionPane.showConfirmDialog(null, "Would you like to autotranslate all untranslated elements?", "Closing", dialogButton);
        if (dialogResult == JOptionPane.YES_OPTION) {
            for (String id : h5ptrans.getUntranslatedElementIDs()) {
                Element elem = h5ptrans.getElementByID_original(id);
                String autotransText = h5ptrans.getAutoTranslation(GUIFrame.getLanguageIn(), GUIFrame.getLanguageOut(), elem.getText());
                h5ptrans.setTranslation(id, autotransText);
            }
        }
    }

    private  void setImagePath() {
        JFileChooser fileChooser = new JFileChooser(GUIFrame.getCurrentDirectory());
        int result;
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        fileChooser.setAcceptAllFileFilterUsed(false);
        result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            h5ptrans.setTranslatedImages(fileChooser.getCurrentDirectory().toString());
        }
    }

    public void closeApp() {
        int dialogButton = JOptionPane.YES_NO_OPTION, dialogResult;
        dialogResult = JOptionPane.showConfirmDialog(null, "Would you like to close the application (DID YOU SAVE YOUR CHANGES ALREADY?)", "Closing", dialogButton);
        if (dialogResult == JOptionPane.YES_OPTION) {
            if (GUIFrame.isFileOpen())
                h5ptrans.close(false);
            System.exit(0);
        }
    }

    private void saveFile() {
        int dialogButton= JOptionPane.YES_NO_OPTION, dialogResult;
        dialogResult = JOptionPane.showConfirmDialog(null, "Would You like to save your chances?", "Saving", dialogButton);
        if (dialogResult == JOptionPane.YES_OPTION) {
            h5ptrans.close(true);
            h5ptrans.open(GUIFrame.getInFile(), GUIFrame.getOutFile());
            GUIFrame.paintNew();
        }
    }

    private void reloadFile() {
        int dialogButton = JOptionPane.YES_NO_OPTION, dialogResult;
        dialogResult = JOptionPane.showConfirmDialog(null, "Would You like to reload the original file (ALL YOUR CURRENT CHANGES WILL BE LOST)?", "Closing", dialogButton);
        if (dialogResult == JOptionPane.YES_OPTION) {
            h5ptrans.close(false);
            h5ptrans.open(GUIFrame.getInFile(), GUIFrame.getOutFile());
            GUIFrame.paintNew();
        }
    }
    private void loadFile() {
        JFileChooser fileChooser = new JFileChooser(GUIFrame.getCurrentDirectory());
        int result;
        result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            GUIFrame.setCurrentDirectory(fileChooser.getCurrentDirectory());
            inFile = selectedFile.getAbsolutePath();
            int i = inFile.indexOf('_');
            outFile = inFile.substring(0, i + 1) + GUIFrame.getLanguageOut() + ".json";
            h5ptrans.open(inFile, outFile);
            GUIFrame.setInFile(inFile);
            GUIFrame.setOutFile(outFile);
            GUIFrame.setFileOpen(true);
            GUIFrame.paintNew();
        }
    }
}