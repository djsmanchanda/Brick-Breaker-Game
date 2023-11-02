package BrickBreaker;
import javax.swing.JFrame;
public class Main {

	public static void main(String[] args) {
		JFrame obj = new JFrame();
		Gameplay gameplay=new Gameplay();
		obj.setBounds(10, 10, 710, 610); //size of window
		obj.setTitle("Brick Breaker Project"); // name of application
		obj.setResizable(false);
		obj.setVisible(true);// able to see game
		obj.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		obj.add(gameplay);
	}

}
