package fr.dome.games;

import java.util.List;
import fr.dome.server.Client;
import fr.dome.server.Lobby;

public abstract class Game extends Thread {

	protected List<Client> clients;
	protected int turn;
	protected int nbPlayers;
	protected boolean hasWin = false;
	protected String buffer = null;

	public Game(List<Client> clients, int nbPlayers) {
		this.nbPlayers = nbPlayers;
		this.clients = clients;
		this.turn = (int) (Math.random() * nbPlayers);
	}

	@Override
	public void run() {
		init();
		loop();
		end();
	}

	protected void init() {
	}

	abstract protected void loop();

	protected void end() {
		while (!clients.isEmpty()) {
			Client client = clients.get(0);
			client.clearGameState();
			Lobby.getInstance().insertClient(client);
			clients.remove(client);
		}
	}

	abstract protected void draw();

	static public int getNbPlayers() {
		return 0;
	}

	protected void nextTurn() {
		turn = (turn + 1) % nbPlayers;
	}

}
