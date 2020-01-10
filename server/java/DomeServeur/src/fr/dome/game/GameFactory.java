package fr.dome.game;

import java.lang.reflect.InvocationTargetException;
import java.util.List;

import fr.dome.game.games.GameState;
import fr.dome.server.Client;

public class GameFactory {

	private static GameFactory gf;
	
	public static GameFactory getInstance() {
		if (gf == null) 
			gf = new GameFactory();
		return gf;
	}
	
	public Game createGame(GameState s, String gameCode, List<Client> players) {
		try {
			return s.getGameClass().getDeclaredConstructor(String.class, List.class).newInstance(gameCode, players);
		} catch (InstantiationException | IllegalAccessException | IllegalArgumentException | InvocationTargetException
				| NoSuchMethodException | SecurityException e) {
			e.printStackTrace();
			return null;
		}
	}
}
