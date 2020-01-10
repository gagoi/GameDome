package fr.dome.game;

import java.util.List;

import fr.dome.server.Client;
import fr.dome.server.Lobbies;
import fr.dome.server.MainLobby;

public abstract class Game extends Thread {

	protected List<Client> clients;
	protected int turn;
	protected int nbPlayers;
	protected boolean hasWin = false;
	protected String buffer = null;
	protected int winner;
	private String gameCode;
	
	protected boolean stop;

	protected Client actual;

	public Game(String gameCode, List<Client> clients, int nbPlayers) {
		this.nbPlayers = nbPlayers;
		this.clients = clients;
		this.gameCode = gameCode;
		this.turn = (int) (Math.random() * nbPlayers);
		actual = clients.get(turn); 
	}

	@Override
	final public void run() {
		init();

		nextTurn();
		while (!hasEnd() && !stop) {
			nextTurn();
			emergencyExit(actual); // Test de deco.
			loop();
		}
		end();
	}

	protected void init() {
		sendAll("S");
	}

	abstract protected void loop();

	protected void end() {
		if (winner == -1) {
			sendAll("E");
		} else if (winner != 0) {
			clients.get(winner).getCommunicationHandler().send("GG");
			sendAllOthers("L", clients.get(winner));
		} else {
			if (hasWin()) {
				actual.getCommunicationHandler().send("GG");
				sendAllOthers("L", actual);
			} else {
				sendAll("E");
			}
		}
		while (!clients.isEmpty()) {
			Client client = clients.get(0);
			MainLobby.getInstance().insertClient(client);
			clients.remove(client);
		}
		Lobbies.getInstance().games_list.remove(gameCode);
	}

	static public int getNbPlayers() {
		return 0;
	}

	protected void nextTurn() {
		turn = (turn + 1) % nbPlayers;
		actual = clients.get(turn);
	}

	protected String waitforbuffer(Client c) {
		try {
			synchronized (c) {
				// System.out.println("Wait");
				c.wait();
				// System.out.println("Waitplus");
			}
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		}
		String str = c.getBuffer();
		c.clearBuffer();
		return str;
	}

	protected void emergencyExit(Client actual) {
		if (!actual.isAlive()) {
			clients.remove(actual);
			sendAll("GG");
			return;
		}
	}

	protected void sendAll(String str) {
		clients.forEach((c) -> {
			c.getCommunicationHandler().write(str.toString());
			c.getCommunicationHandler().flush();
		});
	}

	protected void sendAllOthers(String str, Client client) {
		clients.forEach((c) -> {
			if (c != client) {
				c.getCommunicationHandler().write(str.toString());
				c.getCommunicationHandler().flush();
			}
		});
	}

	protected int readPlacement(String input) {
		try {
			return Integer.parseInt(input.substring(1));
		} catch (StringIndexOutOfBoundsException | NumberFormatException | NullPointerException e) {
			stop = true;
			return -1;
		}
	}

	public int getNbPlayer() {
		throw new IllegalArgumentException("Wtf plz redefine this");
	}

	protected boolean hasEnd() {
		return hasWin() || isFull();
	}

	abstract protected boolean hasWin();

	abstract protected boolean isFull();
}
