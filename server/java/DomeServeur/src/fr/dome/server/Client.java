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
		try {
			this.communication = new ClientCommunicationHandler(socket.getInputStream(), socket.getOutputStream());
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.id = ++ids;
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
						//System.out.println("Client " + id + " logged as " + pseudo);
					} else if (str.startsWith("\n")) {
						preStop();
						return;
					} else if (str.startsWith("M")) {
						state = GameState.MORPION;
					}
					break;
				case MORPION:
					if (str.startsWith("P")) {
						synchronized (this) {
							buffer = str;
							notify();
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
