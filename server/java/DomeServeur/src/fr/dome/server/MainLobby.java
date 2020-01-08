package fr.dome.server;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.ArrayList;

public class MainLobby extends Thread {

	private static final int ERROR_SERVER = 2;
	volatile private static boolean isRunning = true;
	volatile private static ArrayList<Client> clients = new ArrayList<Client>();

	private static final int PORT = 45703;
	private static ServerSocket socket;

	private static MainLobby lobby;

	private MainLobby() {
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

	public static synchronized MainLobby getInstance() {
		if (lobby == null)
			lobby = new MainLobby();
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

	public void remove(Client client) {
		clients.remove(client);
	}

	public int getNumberOfClients() {
		return clients.size();
	}

	public Client getClient(int i) {
		return clients.get(i);
	}
}
