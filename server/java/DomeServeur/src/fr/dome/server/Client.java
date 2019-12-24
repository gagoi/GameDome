package fr.dome.server;

import java.io.IOException;
import java.net.Socket;

public class Client extends Thread {
	public enum State {
		LOBBY, MORPION
	};

	private static int ids = 0; // Nombre de clients qui se sont connectés au serveur.

	private final int id; // Id du client.
	private ClientCommunicationHandler communication;
	private String pseudo = null;
	private State state = State.LOBBY;
	volatile private String buffer = null;

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
		System.out.println("Client " + id + " disconnected");
	}

	/*
	 * public String read() { String str = ""; try { str = read(in); } catch
	 * (IOException e) { e.printStackTrace(); preStop(); } if (str.equals("")) {
	 * System.out.println("Client " + id + " disconnected"); } else
	 * System.out.println(id + " : " + str); return str; }
	 * 
	 */
	@Override
	public void run() {
		while (true) {
			try {
				String str = getCommunicationHandler().read();
				switch (state) {
				case LOBBY:
					if (str.startsWith("NC")) {
						pseudo = str.substring(2);
						System.out.println("Client " + id + " logged as " + pseudo);
					} else if (str.startsWith("\n")) {
						preStop();
						return;
					} else if (str.startsWith("M")) {
						state = State.MORPION;
					}
					break;
				case MORPION:
					if (str.startsWith("P")) {
						buffer = str;
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

	public State getGameState() {
		return state;
	}
}
