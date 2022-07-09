package de.thu.h5ptranslatorgui;

import javax.swing.JTextField;

public class H5PTranslatorGUITextField extends JTextField
{
    private H5PTranslatorGUIText mtpText;

    public H5PTranslatorGUITextField(String s, H5PTranslatorGUIText t)
    {
        super(s);
        mtpText = t;
    }

    public H5PTranslatorGUIText getMtpText()
    {
        return mtpText;
    }

}
