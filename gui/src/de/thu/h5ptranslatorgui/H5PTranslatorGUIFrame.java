package de.thu.h5ptranslatorgui;

import de.thu.h5ptranslate.H5PTranslator;
import de.thu.h5ptranslate.H5PTranslatorFactory;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;
import java.util.Scanner;

public class H5PTranslatorGUIFrame extends JFrame {

    H5PTranslatorGUINavigation GUINavigation;
    H5PTranslatorGUITranslation GUITranslation;

    H5PTranslator h5ptrans;

    boolean fileOpen = false;

    JSplitPane pSplit;
    JPanel pLeft, pRight;
    File currentDirectory;
    String inFile = "", outFile = "";

    String[] languages = {"EN", "DE", "HU"};

    int selectedInLanguage = 0, selectedOutLanguage = 1;

    int slideNr = 1;

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

        try {
            File myObj = new File("startDirectory.txt");
            Scanner myReader = new Scanner(myObj);
            currentDirectory = new File(myReader.nextLine());
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("FileNotFoundException");
            e.printStackTrace();
        }

        // creating the H5PAccess class using the factory design pattern
        H5PTranslatorFactory factory = new H5PTranslatorFactory();
        h5ptrans = factory.create();

        paintNew();

        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent e) {
                GUINavigation.closeApp();
            }
        });

        setResizable(false);
        setSize(1900, 1000);
        setVisible(true);
    }

    public void paintNew() {

        getContentPane().removeAll();


        pSplit = new JSplitPane();
        pSplit.setDividerLocation(0.15);
        pSplit.setDividerSize(1);

        GUINavigation = new H5PTranslatorGUINavigation(this);
        pLeft = new JPanel();
        pLeft.setBackground(Color.GRAY);
        pLeft.add(GUINavigation);
        pSplit.add(pLeft, JSplitPane.LEFT);

        pRight = new JPanel();
        pRight.setBackground(Color.GRAY);
        if (isFileOpen()) {
            GUITranslation = new H5PTranslatorGUITranslation(this);
            pRight.add(GUITranslation);

        } else {
            JLabel j = new JLabel("Please check the language you want to translate to and then load a file of the form xyz_EN.json etc.");
            j.setForeground(Color.red);
            j.setFont(new Font("TimesRoman", Font.PLAIN, 30));
            pRight.add(j);
        }
        pSplit.add(pRight, JSplitPane.RIGHT);


        add(pSplit);
        validate();
        repaint();
    }

    public void refresh3() {

        pSplit.remove(pRight);

        GUITranslation = new H5PTranslatorGUITranslation(this);
        pRight = new JPanel();
        pRight.setBackground(Color.GRAY);
        pRight.add(GUITranslation);

        pSplit.add(pRight, JSplitPane.RIGHT);

        add(pSplit);
        validate();
        repaint();
    }

    public H5PTranslator getH5ptrans() {
        return h5ptrans;
    }

    public H5PTranslatorGUINavigation getGUINavigation() {
        return GUINavigation;
    }

    public H5PTranslatorGUITranslation getGUITranslation() {
        return GUITranslation;
    }

    public File getCurrentDirectory() {
        return currentDirectory;
    }

    public void setCurrentDirectory(File currentDirectory) {
        this.currentDirectory = currentDirectory;
    }

    public String getInFile() {
        return inFile;
    }

    public String getOutFile() {
        return outFile;
    }

    public void setInFile(String inFile) {
        this.inFile = inFile;
    }

    public void setOutFile(String outFile) {
        this.outFile = outFile;
    }


    public boolean isFileOpen() {
        return fileOpen;
    }

    public void setFileOpen(boolean fileOpen) {
        this.fileOpen = fileOpen;
    }

    public int getSlideNr() {
        return slideNr;
    }

    public void setSlideNr(int slideNr) {
        this.slideNr = slideNr;
    }

    public int getSelectedInLanguage() {
        return selectedInLanguage;
    }

    public void setSelectedInLanguage(int selectedInLanguage) {
        this.selectedInLanguage = selectedInLanguage;
    }

    public int getSelectedOutLanguage() {
        return selectedOutLanguage;
    }

    public void setSelectedOutLanguage(int selectedOutLanguage) {
        this.selectedOutLanguage = selectedOutLanguage;
    }

    public String[] getLanguages() {
        return languages;
    }

    public String getLanguageIn() {
        return languages[selectedInLanguage];
    }

    public String getLanguageOut() {
        return languages[selectedOutLanguage];
    }

}
