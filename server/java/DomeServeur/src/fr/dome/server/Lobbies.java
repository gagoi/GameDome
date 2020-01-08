package fr.dome.server;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import fr.dome.game.games.GameState;

public class Lobbies {
	public HashMap<String, GameLobby> games_list = new HashMap<String, GameLobby>();
	private static Lobbies instance;

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

	public void insert(Client client, String str) {
		String key = str.substring(str.length() - 4, str.length());
		String game = str.substring(0, str.length() - 4);

		
		if (Lobbies.getInstance().games_list.containsKey(key)) {
			Lobbies.getInstance().games_list.get(key).add(client);
			if (Lobbies.getInstance().games_list.get(key).size() == GameState.valueOf(game.toUpperCase()).getNbPlayers()) {
				try {
					Lobbies.getInstance().games_list.get(key).getState().getGameClass().getConstructor(List.class).newInstance(Lobbies.getInstance().games_list.get(key)).start();
				} catch (InstantiationException | IllegalAccessException | IllegalArgumentException
						| InvocationTargetException | NoSuchMethodException | SecurityException e) {
					e.printStackTrace();
				}
			}
		} else {
			try {
				GameLobby gl = new GameLobby(GameState.valueOf(game.toUpperCase()));
				gl.add(client);
				Lobbies.getInstance().games_list.put(key, gl);
			} catch (IllegalArgumentException e) {
				System.out.println("Impossible d'ajouter le client, le jeu n'existe pas");
			}
		}
	}
}
