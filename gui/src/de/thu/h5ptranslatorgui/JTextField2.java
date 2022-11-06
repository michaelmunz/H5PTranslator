package de.thu.h5ptranslatorgui;

import org.jsoup.Jsoup;
import javax.swing.*;

public class JTextField2 extends JTextField {
        String htmlText;

        public String getHtmlText() {
            return htmlText;
        }

    public void setHtmlText(String htmlText) {
        this.htmlText = htmlText;
        setText(removeTags(htmlText));
    }

    public JTextField2(String s) {
            setText(removeTags(s));
            setHtmlText(s);
    }

    public static String removeTags(String in) {
        return Jsoup.parse(in).text();
    }

}
