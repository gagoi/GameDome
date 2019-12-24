package fr.dome.games;
import java.util.ArrayList;

import fr.dome.server.Client;

public class Morpion extends Game {

	private static final char[] TOKENS = {'X', 'O'};
	private char grid[][] = { { ' ', ' ', ' ' }, { ' ', ' ', ' ' }, { ' ', ' ', ' ' } };

	public Morpion(Client j1, Client j2) {
		clients = new ArrayList<Client>(2);
		clients.add(j1);
		clients.add(j2);
		turn = (int) (Math.random() * 2);
		nbPlayers = 2;
	}

	@Override
	public void run() {
		sendAll("S");
		System.out.println("Start");
		Client actual;
		do {
			actual = clients.get(turn);
			buffer = null;
			actual.getCommunicationHandler().send("T");
			draw();

			int pos = readPlacement(waitforbuffer(actual));
			
			if (isPlacementAvailable(pos)) {
				grid[pos / 3][pos % 3] = TOKENS[turn];
				
			} else {
				continue;
			}
			
			hasWin = checkWin(TOKENS[turn]);
			nextTurn();
		} while (!hasWin);
		draw();
		actual.getCommunicationHandler().send("GG");
		clients.get(turn).getCommunicationHandler().send("L");
	}

	protected void draw() {
		StringBuilder str = new StringBuilder();
		str.append('G');
		for (int i = 0; i < 3; ++i)
			for (int j = 0; j < 3; ++j)
				str.append(grid[i][j]);

		sendAll(str.toString());
	}

	private void sendAll(String str) {
		clients.forEach((c) -> {
			c.getCommunicationHandler().send(str.toString());
		});
	}

	private int readPlacement(String input) {
		return Integer.parseInt(input.substring(1));
	}
	
	private boolean isPlacementAvailable(int c) {
		return grid[c/3][c % 3] == ' ';
	}
	
	private boolean checkWin(char token) {
		boolean l1 = grid[0][0] == grid[0][1] && grid[0][1] == grid[0][2] && grid[0][0] == token;
		boolean l2 = grid[1][0] == grid[1][1] && grid[1][1] == grid[1][2] && grid[1][0] == token;
		boolean l3 = grid[2][0] == grid[2][1] && grid[2][1] == grid[2][2] && grid[2][0] == token;

		boolean c1 = grid[0][0] == grid[1][0] && grid[1][0] == grid[2][0] && grid[0][0] == token;
		boolean c2 = grid[0][1] == grid[1][1] && grid[1][1] == grid[2][1] && grid[0][1] == token;
		boolean c3 = grid[0][2] == grid[1][2] && grid[1][2] == grid[2][2] && grid[0][2] == token;
		
		boolean d1 = grid[0][0] == grid[1][1] && grid[1][1] == grid[2][2] && grid[0][0] == token; 
		boolean d2 = grid[0][2] == grid[1][1] && grid[1][1] == grid[2][0] && grid[0][2] == token; 
		
		return l1 || l2 || l3 || c1 || c2 || c3 || d1 || d2;
	}
	
	public String waitforbuffer(Client c) {
		while (c.getBuffer() == null) {
			try {
				Thread.sleep(50);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		String str = c.getBuffer();
		c.clearBuffer();
		return str;
	}
}
