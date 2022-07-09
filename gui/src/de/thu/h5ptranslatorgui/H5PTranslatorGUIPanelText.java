package de.thu.h5ptranslatorgui;

public class H5PTranslatorGUIPanelText extends H5PTranslatorGUIPanel
{
    private H5PTranslatorGUITextField orig, trans;
    private H5PTranslatorGUIFocusListener fl = new H5PTranslatorGUIFocusListener();
        
    H5PTranslatorGUIPanelText(H5PTranslatorGUIText t) {
        super();
        orig = new H5PTranslatorGUITextField(t.getOrig(), t);
        trans = new H5PTranslatorGUITextField(t.getTrans(), t);
        add(orig);
        add(trans);
        fl.add(t, orig, trans);
   }
}
