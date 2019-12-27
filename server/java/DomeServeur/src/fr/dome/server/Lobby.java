package fr.dome.server;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.ArrayList;

public class Lobby extends Thread {

	private static final int ERROR_SERVER = 2;
	volatile private static boolean isRunning = true;
	volatile private static ArrayList<Client> clients = new ArrayList<Client>();

	private static final int PORT = 45703;
	private static ServerSocket socket;
	private static GameLauncher launcher;

	private static Lobby lobby;

	private Lobby() {
		launcher = new GameLauncher(clients);
		try {
			socket = new ServerSocket(PORT);
			System.out.println(socket.getInetAddress().toString());
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(ERROR_SERVER);
		}
	}

	@Override
	public void run() {
		launcher.start();
		try {
			while (isRunning) {
				Client c = new Client(socket.accept());
				clients.add(c);
				c.start();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static synchronized Lobby getInstance() {
		if (lobby == null)
			lobby = new Lobby();
		return lobby;
	}

	public void insertClient(Client c) {
		clients.add(c);
	}

	public ArrayList<Client> getPlayerList() {
		return clients;
	}

	public void disconnect(Client client) {
		synchronized (clients) {
			clients.remove(client);
		}
	}
}
