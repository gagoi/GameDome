package fr.dome.games;

import java.util.List;
import fr.dome.server.Client;

public abstract class Game extends Thread {

	protected List<Client> clients;
	protected int turn;
	protected int nbPlayers;
	protected boolean hasWin = false;
	protected String buffer = null;
	
	@Override
	abstract public void run();
	
	abstract protected void draw();
	
	protected void nextTurn() {
		turn = (turn + 1) % nbPlayers;
	}
}
