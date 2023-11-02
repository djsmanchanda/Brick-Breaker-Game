package BrickBreaker;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.JPanel;
import javax.swing.Timer;

@SuppressWarnings("serial")
public class Gameplay extends JPanel implements KeyListener, ActionListener {
    private boolean play = false;
    private int score = 0;
    private int totalBricks = 28; // 4 rows, 7 columns
    private Timer timer;
    private int delay = 8;

    private int paddle = 310; // paddle position

    private int ballposX = 120; // starting coordinate of ball
    private int ballposY = 350;
    private int ballXdir = 2; // modify speed in x and y axis
    private int ballYdir = -3;

    private MapGenerator map; // generates brick layout

    public Gameplay() {
        map = new MapGenerator(4, 7); // creates 4 x 7 bricks
        addKeyListener(this);
        setFocusable(true); // to take keyboard input
        setFocusTraversalKeysEnabled(false);
        timer = new Timer(delay, this); // limits FPS and Speed of gameplay
        timer.start();
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        // Background
        g.setColor(Color.BLACK);
        g.fillRect(1, 1, 692, 592);

        // Drawing map
        map.draw((Graphics2D) g);

        // Borders
        g.setColor(Color.YELLOW);
        g.fillRect(0, 0, 3, 592);
        g.fillRect(0, 0, 692, 3);
        g.fillRect(691, 0, 3, 592);

        // Display score at the top
        g.setColor(Color.WHITE);
        g.setFont(new Font("serif", Font.BOLD, 25));
        g.drawString("Score: " + score, 590, 30);

        // The paddle
        g.setColor(Color.GREEN);
        g.fillRect(paddle, 550, 100, 8);

        // The ball
        g.setColor(Color.RED);
        g.fillOval(ballposX, ballposY, 20, 20);

        // Game condition - win
        if (totalBricks <= 0) {
            play = false;
            ballXdir = 0;
            ballYdir = 0;
            g.setColor(Color.YELLOW);
            g.setFont(new Font("serif", Font.BOLD, 30));
            g.drawString("YOU WON!", 260, 300);
            g.setFont(new Font("serif", Font.BOLD, 20));
            g.drawString("Press Enter To Restart", 230, 350);
        }

        // Ball dropped
        if (ballposY > 570) {
            play = false;
            ballXdir = 0;
            ballYdir = 0;
            g.setColor(Color.CYAN);
            g.setFont(new Font("serif", Font.BOLD, 30));
            g.drawString("Game Over, Score: " + score, 190, 300);
            g.setFont(new Font("serif", Font.BOLD, 20));
            g.drawString("Press Enter To Restart", 230, 350);
            g.setFont(new Font("serif", Font.BOLD, 20));
            g.drawString("Project by-", 80, 400);
            g.setFont(new Font("serif", Font.BOLD, 20));
            g.drawString("Divjot, Varshit, Arpit, Vedashree", 80, 450);
            g.setFont(new Font("serif", Font.BOLD, 20));
            g.drawString("131, 100, 079, 08", 80, 500);
        }
    }


    @Override
    public void actionPerformed(ActionEvent e) {
        if (play) {
            // If the ball hits the paddle
            if (new Rectangle(ballposX, ballposY, 20, 20).intersects(new Rectangle(paddle, 550, 100, 8))) {
                ballYdir = -ballYdir;
            }

            // If the ball intersects with a brick
            A: for (int i = 0; i < map.map.length; i++) {
                for (int j = 0; j < map.map[0].length; j++) {
                    if (map.map[i][j] > 0) {
                        int brickX = j * map.brickWidth + 80;
                        int brickY = i * map.brickHeight + 50;
                        int brickWidth = map.brickWidth;
                        int brickHeight = map.brickHeight;
                        Rectangle rect = new Rectangle(brickX, brickY, brickWidth, brickHeight);
                        Rectangle ballRect = new Rectangle(ballposX, ballposY, 20, 20);
                        Rectangle brickRect = rect;

                        if (ballRect.intersects(brickRect)) {
                            // If the ball touches a brick
                            if (ballposX + 18 <= brickRect.x || ballposX + 2 >= brickRect.x + brickRect.width) {
                                ballXdir = -ballXdir;
                            } else {
                                ballYdir = -ballYdir;
                            }

                            // For grey brick
                            if (map.brickVal[i][j] == 2) {
                                map.setBrickValue(1, i, j);
                                score += 5;
                            } else {
                                // For white brick
                                map.setBrickValue(0, i, j);
                                totalBricks--;
                                score += 10;
                            }

                            break A;
                        }
                    }
                }
            }

            // Changes position of the ball
            ballposX += ballXdir;
            ballposY += ballYdir;

            // If the ball touches the left or right wall
            if (ballposX < 0 || ballposX > 672) {
                ballXdir = -ballXdir;
            }
        }
        repaint();
    }

    // Functions to take keyboard input
    @Override
    public void keyTyped(KeyEvent e) {
    }

    @Override
    public void keyReleased(KeyEvent e) {
    }

    // VK_RIGHT -> Right arrow key
    // VK_LEFT  -> Left arrow key
    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
            moveRight();
        }
        if (e.getKeyCode() == KeyEvent.VK_LEFT) {
            moveLeft();
        }

        // When restarting the game
        if (e.getKeyCode() == KeyEvent.VK_ENTER && !play) {
            play = true;
            ballposX = 120;
            ballposY = 350;
            ballXdir = 2;
            ballYdir = -3;
            paddle = 310;
            score = 0;
            totalBricks = 28;
            map = new MapGenerator(4, 7);
        }
    }

    // Moves the paddle
    public void moveRight() {
        play = true;
        paddle += 20;
        if (paddle >= 600) {
            paddle = 600;
        }
    }

    public void moveLeft() {
        play = true;
        paddle -= 20;
        if (paddle < 10) {
            paddle = 10;
        }
    }
}
