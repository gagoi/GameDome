package fr.dome.games;

public enum GameState {
	LOBBY(null), MORPION(Morpion.class);
	
	private Class<? extends Game> gameClass;
	
	private GameState(Class<? extends Game> gameClass) {
		this.gameClass = gameClass;
	}
	
	public Class<? extends Game> getGameClass() {
		return gameClass;
	}
}
