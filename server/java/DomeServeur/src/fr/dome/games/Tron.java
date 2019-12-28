package fr.dome.games;

import java.util.List;

import fr.dome.server.Client;

public class Tron extends Game {

	public Tron(List<Client> clients, int nbPlayers) {
		super(clients, nbPlayers);
	}

	@Override
	protected void init() {
		super.init();
		
	}
	
	@Override
	protected void loop() {
	}

	@Override
	protected void draw() {
	}

	@Override
	protected boolean hasWin() {
		return false;
	}

	@Override
	protected boolean isFull() {
		return false;
	}
	
	
	public static int getNbPlayers() {
		return 2;
	}

}
