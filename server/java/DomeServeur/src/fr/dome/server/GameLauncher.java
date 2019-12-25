package fr.dome.server;

import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ArrayBlockingQueue;

import fr.dome.games.GameState;

public class GameLauncher extends Thread {

	private List<Client> clients;
	private HashMap<GameState, GamePendingList> games_list;

	public GameLauncher(List<Client> clients) {
		this.clients = clients;
	}

	@Override
	public void run() {
		super.run();

		while (true) {
			for (Client client : clients) {
				if (client.getGameState() != GameState.LOBBY) {

				}
			}

			games_list.forEach((k, v) -> {
				try {
					if (v.size() > (Integer) k.getGameClass().getMethod("getNbPlayers").invoke(null)) {
						k.getGameClass().getConstructor();
					}
				} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException
						| NoSuchMethodException | SecurityException e) {
					e.printStackTrace();
				}
			});
		}
	}

	class GamePendingList extends ArrayBlockingQueue<Client> {
		public GamePendingList() {
			super(5);
		}

		private State s;
		private Queue<Client> queue;

		public State getState() {
			return s;
		}
	}
}
