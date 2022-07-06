import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * Die MTP-GUI
 * 
 * @author HG
 * @version 29.05.2022
 */
public class MTPFrame extends JFrame 
{
    MTPFrame() {
        this(new MTPPanelText[0]);
    }
    
    MTPFrame(MTPPanelText[] tf) {
        // Create a new JFrame container.
        super("MedTec+");         

       setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));
       JTextField t =new JTextField("MTP rules");
       add(t);
       
       for (int i = 0; i < tf.length; i++) {
            add(tf[i]);
            // Die Buttons müssen erzeugt, mit einem ActionListener versehen
            // und eingefügt werden.
           /* sp[i] = new Button();
            sp[i].setLabel(Integer.toString(i+1));
            sp[i].setBackground(Color.LIGHT_GRAY);
            sp[i].addActionListener(al);
            add(sp[i]); */
        }
        
        // Terminate the program when the user closes the application.
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        

        // Display the frame.
        pack();
        setVisible(true);
    }
}
