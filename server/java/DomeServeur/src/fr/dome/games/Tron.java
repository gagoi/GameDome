package fr.dome.games;

import java.awt.Point;
import java.util.List;

import fr.dome.server.Client;

public class Tron extends Game {

	private static final int WIDTH = 15;
	private static final int HEIGHT = 10;

	public Tron(List<Client> clients) {
		super(clients, 2);
	}

	@Override
	protected void init() {
		super.init();
		System.out.println("Start Tron");
	}

	@Override
	protected void loop() {

		Client other = clients.get((turn + 1) % 2);
		actual.getCommunicationHandler().send("NOW");
		String tmp = waitforbuffer(actual);
		System.out.println(tmp);
		String[] str1 = tmp.substring(1).split("/");

		other.getCommunicationHandler().send("NOW");
		String[] str2 = waitforbuffer(other).substring(1).split("/");

		Point p1 = new Point(Integer.parseInt(str1[1]), Integer.parseInt(str1[0]));
		Point p2 = new Point(Integer.parseInt(str2[1]), Integer.parseInt(str2[0]));

		if (p1.x == -1 && p1.y == -1) {
			if (p2.x == -1 && p2.y == -1)
				winner = -1;
			else
				winner = (turn + 1) % 2;
		} else if (p2.x == -1 && p2.y == -1) {
			winner = turn;
		} else {
			actual.getCommunicationHandler().send("P" + (HEIGHT - p2.y - 1) + "/" + (WIDTH - p2.x - 1));
			other.getCommunicationHandler().send("P" + (HEIGHT - p1.y - 1) + "/" + (WIDTH - p1.x - 1));
		}
	}

	@Override
	protected void draw() {
	}

	@Override
	protected boolean hasWin() {
		return winner != 0;
	}

	@Override
	protected boolean isFull() {
		return false;
	}

	public static int getNbPlayers() {
		return 2;
	}

}
