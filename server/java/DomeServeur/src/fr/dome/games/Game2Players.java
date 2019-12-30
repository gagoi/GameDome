package fr.dome.games;

import java.util.List;

import fr.dome.server.Client;

abstract public class Game2Players extends Game {
	protected Client other;
	protected int otherId;
	
	public Game2Players(List<Client> clients ) {
		super(clients, 2);
		otherId = (turn + 1) % 2;
		other = clients.get(otherId);
	}

	@Override
	abstract protected void loop();

	@Override
	abstract protected boolean hasWin();
	
	protected boolean isFull() {
		return false;
	}
	
	@Override
	protected void nextTurn() {
		other = actual;
		super.nextTurn();
	}
}
