package fr.dome.games;

public enum GameState {
	LOBBY(null, "Lobby"), MORPION(Morpion.class, "Morpion"), PUISSANCE(Puissance4.class, "Puissance"),
	BATTLESHIP(Battleship.class, "Battleship");

	private Class<? extends Game> gameClass;
	private String startCode;

	private GameState(Class<? extends Game> gameClass, String startCode) {
		this.gameClass = gameClass;
		this.startCode = startCode;
	}

	public Class<? extends Game> getGameClass() {
		return gameClass;
	}

	public String getCode() {
		return startCode;
	}
}
