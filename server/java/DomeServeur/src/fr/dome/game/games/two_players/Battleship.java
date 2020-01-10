package fr.dome.game.games.two_players;

import java.awt.Point;
import java.util.ArrayList;
import java.util.List;

import fr.dome.server.Client;

public class Battleship extends Game2Players {
	ArrayList<ArrayList<Boat>> boats = new ArrayList<ArrayList<Boat>>(2);

	public Battleship(String gameCode, List<Client> clients) {
		super(gameCode, clients);
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
			String str;
			try {
				str = waitforbuffer(actual).substring(1);
			} catch (StringIndexOutOfBoundsException e) {
				actual.getCommunicationHandler().send("L");
				other.getCommunicationHandler().send("GG");
				stop = true;
				return;
			}
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
		}
		nextTurn();
		sendAll("SS");
		actual.getCommunicationHandler().send("Kkkkkkk");
	}

	@Override
	protected void loop() {
		String[] str = waitforbuffer(actual).substring(1).split("/");
		int x = Integer.parseInt(str[0]);
		int y = Integer.parseInt(str[1]);

		ArrayList<Boat> b = boats.get((turn + 1) % 2);

		boolean hasTouch = false;
		for (Boat boat : b) {
			if (boat.isHitted(x, y)) {
				hasTouch = true;

				nextTurn();
				if (boat.isSunk()) {
					if (hasWin()) {
						nextTurn();
						winner = turn;
						return;
					}
					actual.getCommunicationHandler().send("BC" + boat.getStart().x + "/" + boat.getStart().y + "/"
							+ boat.getEnd().x + "/" + boat.getEnd().y);
					other.getCommunicationHandler().send("PC" + boat.getStart().x + "/" + boat.getStart().y + "/"
							+ boat.getEnd().x + "/" + boat.getEnd().y);
				} else {
					actual.getCommunicationHandler().send("BT" + x + "/" + y);
					other.getCommunicationHandler().send("PT" + x + "/" + y);
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
	protected boolean hasWin() {
		return boats.get(turn).stream().allMatch((b) -> b.isSunk());
	}

	public static int getNbPlayers() {
		return 2;
	}

	private class Boat {
		private final boolean[] states;
		private final Point[] cases;

		public Boat(int x, int y, int xf, int yf) {
			System.out.println("Bateau");
			if (x == xf) {
				states = new boolean[yf - y + 1];
				cases = new Point[yf - y + 1];
				for (int i = 0; i < cases.length; i++) {
					cases[i] = new Point(x, y + i);
					System.out.println("\t" + cases[i].x + ";" + cases[i].y);
				}
			} else {
				states = new boolean[xf - x + 1];
				cases = new Point[xf - x + 1];
				for (int i = 0; i < cases.length; i++) {
					cases[i] = new Point(x + i, y);
					System.out.println("\t" + cases[i].x + ";" + cases[i].y);
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

		public Point getStart() {
			return cases[0];
		}

		public Point getEnd() {
			return cases[cases.length - 1];
		}

	}

}
