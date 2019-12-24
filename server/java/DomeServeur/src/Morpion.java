import java.util.ArrayList;

public class Morpion extends Thread {

	private static final char[] TOKENS = {'X', 'O'};
	ArrayList<Client> clients = new ArrayList<Client>();
	private char grid[][] = { { ' ', ' ', ' ' }, { ' ', ' ', ' ' }, { ' ', ' ', ' ' } };
	private boolean hasWin = false;

	public Morpion(Client j1, Client j2) {
		clients.add(j1);
		clients.add(j2);
	}

	@Override
	public void run() {
		int turn = (int) (Math.random() * 2);
		sendAll("S");
		System.out.println("Start");
		do {
			clients.get(turn).send("T");
			sendGrid();
			int c = readPlacement(turn);
			if (isPlacementAvailable(c)) {
				grid[c / 3][c % 3] = TOKENS[turn];
			}
			hasWin = checkWin(TOKENS[turn]);
			turn++;
			turn %= 2;
		} while (!hasWin);
	}

	private void sendGrid() {
		StringBuilder str = new StringBuilder();
		str.append('G');
		for (int i = 0; i < 3; ++i)
			for (int j = 0; j < 3; ++j)
				str.append(grid[i][j]);

		sendAll(str.toString());
	}

	private void sendAll(String str) {
		clients.forEach((c) -> {
			c.send(str.toString());
		});
	}

	private int readPlacement(int turn) {
		String str = clients.get(turn).read();
		if (str.startsWith("P")) return Integer.parseInt(str.substring(1));
		else return -1;
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
}
