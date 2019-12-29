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

	private boolean isPlacementAvailable(int c) {
		return grid[c / 3][c % 3] == ' ';
	}

	@Override
	protected boolean isFull() {
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

	static public int getNbPlayers() {
		return 2;
	}

	@Override
	protected void init() {
		super.init();
		sendAll("S");
		System.out.println("Start Morpion");
	}

	@Override
	protected void loop() {
		actual.getCommunicationHandler().write("T");
		draw();

		int pos = readPlacement(waitforbuffer(actual));

		if (pos == 9 || pos == -1) {
			actual.getCommunicationHandler().send("L");
			clients.remove(actual);
			sendAll("GG");
			return;
		}

		if (isPlacementAvailable(pos)) {
			grid[pos / 3][pos % 3] = TOKENS[turn];
		} else {
			nextTurn(); // On fait un nextTurn en plus comme ca on revient sur le meme joueur et il
						// rejoue ce bolosse.
		}
	}

	@Override
	protected boolean hasWin() {
		return checkWin(TOKENS[(turn + 1) % 2]);
	}
}
