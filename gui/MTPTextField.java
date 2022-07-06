import javax.swing.JTextField;

/**
 * Beschreiben Sie hier die Klasse MTPTextField.
 * 
 * @author HG
 * @version 30.5.2022
 */
public class MTPTextField extends JTextField
{
    private MTPText mtpText;

    public MTPTextField(String s, MTPText t)
    {
        super(s);
        mtpText = t;
    }

    public MTPText getMtpText() 
    {
        return mtpText;
    }

}
