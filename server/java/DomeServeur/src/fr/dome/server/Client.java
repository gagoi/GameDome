package fr.dome.server;

import java.io.IOException;
import java.net.Socket;

import fr.dome.games.GameState;

public class Client extends Thread {

	private static int ids = 0; // Nombre de clients qui se sont connectés au serveur.

	private final int id; // Id du client.
	private ClientCommunicationHandler communication;
	private String pseudo = null;
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
		MainLobby.getInstance().disconnect(this);
		System.out.println("Client " + id + " disconnected");
	}

	@Override
	public void run() {
		while (true) {
			try {
				String str = getCommunicationHandler().read();
				if (str.startsWith("NC")) { // Choix du pseudo
					pseudo = str.substring(2);
					getCommunicationHandler().setPseudo(pseudo);
					// System.out.println("Client " + id + " logged as " + pseudo);
				} else if (str.startsWith("\n")) { // Déconnexion
					preStop();
					return;
				} else if (str.startsWith("P") || str.startsWith("B")) { // Game Letters
					synchronized (this) {
						buffer = str;
						notifyAll();
					}
				} else if (str.startsWith("Q")) { // Insertion dans une partie
					Lobbies.insert(this, str);
					MainLobby.getInstance().remove(this);
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

	public String getPseudo() {
		return pseudo;
	}

	public int getClientId() {
		return id;
	}
}
