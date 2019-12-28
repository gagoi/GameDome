package fr.dome.server;

import java.io.IOException;
import java.net.Socket;

import fr.dome.games.GameState;

public class Client extends Thread {

	private static int ids = 0; // Nombre de clients qui se sont connectés au serveur.

	private final int id; // Id du client.
	private ClientCommunicationHandler communication;
	private String pseudo = null;
	private GameState state = GameState.LOBBY;
	private String buffer = new String();

	public Client(Socket socket) {
		this.id = ++ids;
		try {
			this.communication = new ClientCommunicationHandler(id, socket.getInputStream(), socket.getOutputStream());
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Client " + id + " connected.");
	}

	public void preStop() {
		Lobby.getInstance().disconnect(this);
		System.out.println("Client " + id + " disconnected");
	}

	@Override
	public void run() {
		while (true) {
			try {
				String str = getCommunicationHandler().read();

				switch (state) {
				case LOBBY:
					if (str.startsWith("NC")) {
						pseudo = str.substring(2);
						getCommunicationHandler().setPseudo(pseudo);
						// System.out.println("Client " + id + " logged as " + pseudo);
					} else if (str.startsWith("\n")) {
						preStop();
						return;
					} else {
						for (GameState g : GameState.values()) {
							if (g != GameState.LOBBY)
								if (str.startsWith(g.getCode()))
									state = g;
						}
					}
					break;
				case PUISSANCE:
				case MORPION:
					if (str.startsWith("P")) {
						synchronized (this) {
							//System.out.println(str);
							buffer = str;
							notifyAll();
						}
					}
					break;
				case BATTLESHIP:
					if (str.startsWith("P") || str.startsWith("B")) {
						synchronized (this) {
							buffer = str;
							notifyAll();
						}
					}
					break;

				}
			} catch (NullPointerException e) {
				preStop();
				return;
			}
		}
	}

	public boolean isInitialized() {
		return pseudo != null;
	}

	public ClientCommunicationHandler getCommunicationHandler() {
		return communication;
	}

	public String getBuffer() {
		return buffer;
	}

	public void clearBuffer() {
		buffer = null;
	}

	public GameState getGameState() {
		return state;
	}

	public void clearGameState() {
		state = GameState.LOBBY;
	}

	public String getPseudo() {
		return pseudo;
	}

	public int getClientId() {
		return id;
	}
}
