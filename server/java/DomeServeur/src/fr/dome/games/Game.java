package fr.dome.games;

import java.util.List;
import fr.dome.server.Client;

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
	abstract public void run();
	
	abstract protected void draw();
	
	static public int getNbPlayers() {
		return 0;
	}
	
	protected void nextTurn() {
		turn = (turn + 1) % nbPlayers;
	}
	
}
