package fr.dome.games;

import java.util.List;

import fr.dome.server.Client;

public class Morpion extends Game {

	private static final char[] TOKENS = { 'X', 'O' };
	private char grid[][] = { { ' ', ' ', ' ' }, { ' ', ' ', ' ' }, { ' ', ' ', ' ' } };

	public Morpion(List<Client> clients) {
		super(clients, 2);
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
			c.getCommunicationHandler().write(str.toString());
			c.getCommunicationHandler().flush();
		});
	}

	private int readPlacement(String input) {
		return Integer.parseInt(input.substring(1));
	}

	private boolean isPlacementAvailable(int c) {
		return grid[c / 3][c % 3] == ' ';
	}

	private boolean isFull() {
		boolean full = true;

		for (int i = 0; i < 3; ++i)
			for (int j = 0; j < 3; ++j)
				full &= grid[i][j] != ' ';
		return full;
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
		try {
			synchronized (c) {
				c.wait();
			}
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		}
		String str = c.getBuffer();
		c.clearBuffer();
		return str;
	}

	static public int getNbPlayers() {
		return 2;
	}

	@Override
	protected void loop() {
		sendAll("S");
		System.out.println("Start");
		Client actual;
		do {
			actual = clients.get(turn);
			actual.getCommunicationHandler().write("T");
			draw();

			int pos = readPlacement(waitforbuffer(actual));

			if (isPlacementAvailable(pos)) {
				grid[pos / 3][pos % 3] = TOKENS[turn];

			} else {
				continue;
			}

			hasWin = checkWin(TOKENS[turn]) || isFull();
			nextTurn();
		} while (!hasWin);
		draw();
		if (checkWin(TOKENS[turn]) || checkWin(TOKENS[(turn + 1) % 2])) {
			actual.getCommunicationHandler().send("GG");
			clients.get(turn).getCommunicationHandler().send("L");
		} else {
			sendAll("E");
		}
	}
}
