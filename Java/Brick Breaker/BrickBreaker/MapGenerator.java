package BrickBreaker;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
//class to refresh display
public class MapGenerator {
    public int map[][];
    public int brickWidth;
    public int brickHeight;
    public int brickVal[][];
	//generate layout of bricks
    public MapGenerator(int row, int col) {
        map = new int[row][col];
        brickVal = new int[row][col];

        for (int i = 0; i < map.length; i++) {
            for (int j = 0; j < map[0].length; j++) {
                map[i][j] = 1;
				if((i+j)%2==1)//sets alternate bricks grey and white
                brickVal[i][j] = 2;
				else
				brickVal[i][j] = 1;
            }
        }
		//size of bricks
        brickWidth = 540 / col;
        brickHeight = 200 / row;
    }

    public void draw(Graphics2D g) {
        for (int i = 0; i < map.length; i++) {
            for (int j = 0; j < map[0].length; j++) {
                //displays all remaining bricks
				if (map[i][j] > 0) {
                    if (brickVal[i][j] == 1) {
                        g.setColor(Color.white);//displays white bricks;
                    } else {
                        g.setColor(Color.gray);//displays grey brick;
                    }
                    g.fillRect(j * brickWidth + 80, i * brickHeight + 50, brickWidth, brickHeight);
                    //black gap between bricks
					g.setStroke(new BasicStroke(3));
                    g.setColor(Color.black);
                    g.drawRect(j * brickWidth + 80, i * brickHeight + 50, brickWidth, brickHeight);
                }
            }
        }
    }
	// turns grey brick to white, and white to black
    public void setBrickValue(int value, int row, int col) {
        brickVal[row][col] = value;
		if(brickVal[row][col] == 0)
		map[row][col]=0;
    }
}
