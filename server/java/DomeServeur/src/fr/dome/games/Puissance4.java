package fr.dome.games;

import java.util.List;

import fr.dome.server.Client;

public class Puissance4 extends Game {

	private int[][] grid = new int[6][7];
	private int lastP, lastY;

	public Puissance4(List<Client> clients) {
		super(clients, 2);
	}

	@Override
	protected void init() {
		super.init();

		System.out.println("Start Puissance 4");
		actual.getCommunicationHandler().send("T-1");
	}

	@Override
	protected void loop() {
		int pos = readPlacement(waitforbuffer(actual));

		if (pos == 9 || pos == -1) {
			actual.getCommunicationHandler().send("L");
			clients.remove(actual);
			sendAll("GG");
			return;
		} else {
			sendAllOthers("T" + pos, actual);

			int y;
			for (y = 0; y < 6 && grid[y][pos] != 0; ++y)
				;
			grid[y][pos] = turn + 1;

			lastP = pos;
			lastY = y;
			
			if (!hasWin())
				sendAllOthers("C1", actual);
			else
				sendAllOthers("C0", actual);
		}
	}

	@Override
	protected void draw() {

	}

	static public int getNbPlayers() {
		return 2;
	}

	protected boolean hasWin() {
		return hasWin((turn + 1) % 2, lastP, lastY, grid);
	}

	private static boolean hasWin(int turn, int p, int y, int[][] grid) {
		return hasWinHorizontal(turn, grid, p, y) || hasWinVertical(turn, grid, p, y) || hasWinD1(turn, grid, p, y)
				|| hasWinD2(turn, grid, p, y);
	}

	private static boolean hasWinHorizontal(int turn, int[][] grid, int p, int y) {
		int cpt = 1;
		for (int i = p + 1; i < Math.min(p + 4, 7) && grid[y][i] == turn + 1; ++i)
			cpt++;
		for (int i = p - 1; i >= Math.max(p - 4, 0) && grid[y][i] == turn + 1; --i)
			cpt++;
		return cpt >= 4;
	}

	private static boolean hasWinVertical(int turn, int[][] grid, int p, int y) {
		int cpt = 1;
		for (int i = y - 1; i >= Math.max(y - 4, 0) && grid[i][p] == turn + 1; --i)
			cpt++;
		return cpt >= 4;
	}

	private static boolean hasWinD1(int turn, int[][] grid, int p, int y) {
		int cpt = 1;
		for (int i = p + 1, j = y + 1; i < Math.min(p + 4, 7) && j < Math.min(y + 4, 6)
				&& grid[j][i] == turn + 1; ++i, ++j)
			cpt++;
		for (int i = p - 1, j = y - 1; i >= Math.max(p - 4, 0) && j >= Math.max(y - 4, 0)
				&& grid[j][i] == turn + 1; --i, --j)
			cpt++;
		return cpt >= 4;
	}

	private static boolean hasWinD2(int turn, int[][] grid, int p, int y) {
		int cpt = 1;
		for (int i = p + 1, j = y - 1; i < Math.min(p + 4, 7) && j >= Math.max(y - 4, 0)
				&& grid[j][i] == turn + 1; ++i, --j)
			cpt++;
		for (int i = p - 1, j = y + 1; i >= Math.max(p - 4, 0) && j < Math.min(y + 4, 6)
				&& grid[j][i] == turn + 1; --i, ++j)
			cpt++;
		return cpt >= 4;
	}

	protected boolean isFull() {
		for (int j = 0; j < 7; ++j)
			if (grid[5][j] == 0)
				return false;
		return true;
	}

}
