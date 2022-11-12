package de.thu.h5ptranslatorgui;

import org.jsoup.Jsoup;

import javax.swing.*;

public class JTextField2 extends JTextField {

    String ID;
    String htmlText;
    String origHtmlText;

    public String getHtmlText() {
        return htmlText;
    }

    public void setHtmlText(String htmlText) {
        this.htmlText = htmlText;
        setText(removeTags(htmlText));
    }

    public JTextField2(String ID, String origHtmlText, String htmlText) {
        this.ID = ID;
        setHtmlText(htmlText);
        this.origHtmlText = origHtmlText;
    }

    public static String removeTags(String in) {
        return Jsoup.parse(in).text();
    }

    public String getID() {
        return ID;
    }


}
