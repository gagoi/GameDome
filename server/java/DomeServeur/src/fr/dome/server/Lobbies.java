package fr.dome.server;

import java.util.ArrayList;
import java.util.HashMap;

import fr.dome.games.GameState;

public class Lobbies extends Thread {
	private HashMap<String, GameLobby> games_list = new HashMap<String, GameLobby>();
	private static Lobbies instance;

	private Lobbies() {
		this.start();
	}

	@Override
	public void run() {
		super.run();

		while (true) {
		}
	}

	public static synchronized Lobbies getInstance() {
		if (instance == null)
			instance = new Lobbies();
		return instance;
	}

	@SuppressWarnings("serial")
	class GameLobby extends ArrayList<Client> {

		private GameState s;

		public GameLobby(GameState s) {
			super(2);
			this.s = s;
		}

		public GameState getState() {
			return s;
		}
	}

	public static void insert(Client client, String str) {
		try {
			GameLobby gl = Lobbies.getInstance().new GameLobby(GameState.valueOf(str.substring(0, str.length() - 4)));
			gl.add(client);
		} catch (IllegalArgumentException e) {
			System.out.println("Impossible d'ajouter le client, le jeu n'existe pas");
		}
	}
}
