package fr.dome.games;

import java.awt.Point;
import java.util.ArrayList;
import java.util.List;

import fr.dome.server.Client;

public class Battleship extends Game {
	ArrayList<ArrayList<Boat>> boats = new ArrayList<ArrayList<Boat>>(2);

	public Battleship(List<Client> clients) {
		super(clients, 2);
	}

	@Override
	protected void init() {
		super.init();
		System.out.println("Start Battleship");
		boats.add(new ArrayList<Battleship.Boat>(5));
		boats.add(new ArrayList<Battleship.Boat>(5));

		for (int k = 0; k < 2; ++k) {
			System.out.println(k);
			actual.getCommunicationHandler().send("NOW");
			String str = waitforbuffer(actual).substring(1);
			String[] bs = str.split("#");
			for (String s : bs) {
				String[] positions = s.split("/");
				System.out.println(s);

				int[] poses = new int[positions.length];
				for (int j = 0; j < 4; ++j) {
					System.out.println(positions[j]);
					poses[j] = Integer.parseInt(positions[j].replace("#", ""));
				}
				boats.get(turn).add(new Boat(poses[0], poses[1], poses[2], poses[3]));

			}
			System.out.println("Fini : " + k);
			nextTurn();
			actual = clients.get(turn);
		}
		nextTurn();
		actual = clients.get(turn);
		sendAll("SS");
		actual.getCommunicationHandler().send("T-1");
	}

	@Override
	protected void loop() {
		String[] str = waitforbuffer(actual).substring(1).split("/");
		int x = Integer.parseInt(str[0]);
		int y = Integer.parseInt(str[1]);

		Client other = clients.get((turn + 1) % 2);

		ArrayList<Boat> b = boats.get((turn + 1) % 2);

		boolean hasTouch = false;
		for (Boat boat : b) {
			if (boat.isHitted(x, y)) {
				actual.getCommunicationHandler().send("BT" + x + "/" + y);
				other.getCommunicationHandler().send("PT" + x + "/" + y);
				hasTouch = true;
				if (boat.isSunk()) {
					actual.getCommunicationHandler().send("BC" + x + "/" + y);
					other.getCommunicationHandler().send("PC" + x + "/" + y);
				}
				break;
			}
		}
		
		if (!hasTouch) {
			actual.getCommunicationHandler().send("BR" + x + "/" + y);
			other.getCommunicationHandler().send("PR" + x + "/" + y);
		}

	}

	@Override
	protected void draw() {
	}

	@Override
	protected boolean hasWin() {
		return boats.get((turn + 1) % 2).stream().allMatch((b) -> b.isSunk());
	}

	@Override
	protected boolean isFull() {
		return false;
	}

	public static int getNbPlayers() {
		return 2;
	}

	private class Boat {
		private final boolean[] states;
		private final Point[] cases;

		public Boat(int x, int y, int xf, int yf) {
			if (x == xf) {
				states = new boolean[yf - y];
				cases = new Point[yf - y];
				for (int i = 0; i < cases.length; i++) {
					cases[i] = new Point(xf - x, yf - y - i);
				}
			} else {
				states = new boolean[xf - x];
				cases = new Point[xf - x];
				for (int i = 0; i < cases.length; i++) {
					cases[i] = new Point(xf - x - i, yf - y);
				}
			}
		}

		/*
		 * res = 0 : non res = 1 : touché res = 2 : coulé
		 */
		public boolean isHitted(int x, int y) {
			for (int i = 0; i < cases.length; ++i) {
				if (cases[i].x == x && cases[i].y == y) {
					states[i] = true;
					return true;
				}
			}
			return false;
		}

		public boolean isSunk() {
			for (int i = 0; i < states.length; ++i)
				if (!states[i])
					return false;
			return true;
		}

		public String toString() {
			return "Boat : " + cases[0].x + ";" + cases[0].y + " - " + cases[cases.length - 1].x + ";"
					+ cases[cases.length - 1].y;
		}

	}

}
