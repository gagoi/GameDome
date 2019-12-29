package fr.dome.server;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;

import fr.dome.games.GameState;

public class GameLauncher extends Thread {

	
	private List<Client> clients;
	private HashMap<GameState, GamePendingList> games_list = new HashMap<GameState, GameLauncher.GamePendingList>();

	public GameLauncher(List<Client> clients) {
		this.clients = clients;
		for (GameState g : GameState.values())
			if (g != GameState.LOBBY)
			games_list.put(g, new GamePendingList());
	}

	@Override
	public void run() {
		super.run();

		while (true) {
			for (int i = 0; i < clients.size(); ++i) {
				Client client = clients.get(i);
				if (client.getGameState() != GameState.LOBBY) {
					games_list.get(client.getGameState()).add(client);
					clients.remove(client);
				}
			}

			games_list.forEach((k, v) -> {
				try {
					int nb = (int) k.getGameClass().getMethod("getNbPlayers").invoke(null);
					if (v.size() >= nb ) {
						ArrayList<Client> new_game = new ArrayList<Client>(nb);
						for (int i = 0; i < nb; i++) {
							new_game.add(v.poll());
						}
						k.getGameClass().getConstructor(List.class).newInstance(new Object[] {new_game}).start();
					}
				} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException
						| NoSuchMethodException | SecurityException | InstantiationException e) {
					e.printStackTrace();
				}
			});
		}
	}

	@SuppressWarnings("serial")
	class GamePendingList extends ArrayBlockingQueue<Client> {
		public GamePendingList() {
			super(5);
		}

		private State s;

		public State getState() {
			return s;
		}
	}
}
