package de.thu.h5ptranslatorgui;

import javax.swing.*;
import java.awt.*;

/**
 * Die MTP-GUI
 * 
 * @author HG
 * @version 29.05.2022
 */
public class H5PTranslatorGUIFrame extends JFrame
{

    H5PTranslatorGUIFrame() {
        super("MedTec+");

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
        pRight.add(new H5PTranslatorGUITranslate());

        JSplitPane pSplit = new JSplitPane();
        pSplit.setDividerLocation(0.25);
        pSplit.setDividerSize(1);
        pSplit.add(pLeft, JSplitPane.LEFT);
        pSplit.add(pRight, JSplitPane.RIGHT);
        add(pSplit);

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        setResizable(false);
        setSize(1200,800);
        setVisible(true);
    }
}
