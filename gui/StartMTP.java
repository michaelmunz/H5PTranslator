import javax.swing.SwingUtilities;
import javax.swing.JFrame;
import javax.swing.JTextField;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

/**
 * main-Methode zu MTP
 * @author HG
 * @version 29.05.2022
 */
public class StartMTP
{
    public static void main(String args[]) {
        // Create the frame on the event dispatching thread.
        SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    MTPText t1 = new MTPText("Hello", "Hallo"),
                    t2 = new MTPText("world!", "Welt");

                    MTPPanelText[] tf = {new MTPPanelText(t1), new MTPPanelText(t2)};
                    new MTPFrame(tf);
                }
            });
    }
}