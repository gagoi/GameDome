package fr.dome.game.games;

import java.util.Arrays;

import fr.dome.game.Game;
import fr.dome.game.games.two_players.Battleship;
import fr.dome.game.games.two_players.Morpion;
import fr.dome.game.games.two_players.Puissance4;
import fr.dome.game.games.two_players.Tron;

public enum GameState {
	LOBBY(null, "Lobby", 0), MORPION(Morpion.class, "Morpion", 2), PUISSANCE(Puissance4.class, "Puissance", 2),
	BATTLESHIP(Battleship.class, "Battleship", 2), TRON(Tron.class, "Tron", 2);

	private Class<? extends Game> gameClass;
	private String startCode;
	private int nbPlayers;

	private GameState(Class<? extends Game> gameClass, String startCode, int nbPlayers) {
		this.gameClass = gameClass;
		this.startCode = startCode;
		this.nbPlayers = nbPlayers;
	}

	public Class<? extends Game> getGameClass() {
		return gameClass;
	}

	public String getCode() {
		return startCode;
	}

	public static boolean isGameCode(String str) {
		return Arrays.asList(values()).stream().anyMatch((gs) -> {
			return str.startsWith(gs.getCode());
		});
	}
	
	public int getNbPlayers() {
		return nbPlayers;
	}
}
