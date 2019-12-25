package fr.dome.server;

import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.UnknownHostException;
import java.util.ArrayList;

import fr.dome.games.GameState;
import fr.dome.games.Morpion;

public class Lobby implements Runnable {

	private static final int ERROR_SERVER = 2;
	volatile private ArrayList<Client> clients = new ArrayList<Client>();

	private final int PORT = 45703;
	private ServerSocket socket;
	private boolean isRunning = true;
	private GameLauncher launcher;

	public static void main(String[] args) {
		try {
			System.out.println(InetAddress.getLocalHost());
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
		Lobby s = new Lobby();
		Thread t = new Thread(s);
		t.start();
	}

	public Lobby() {
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
		try {
			while (isRunning) {
				Client c = new Client(socket.accept());
				clients.add(c);
				c.start();
				if (clients.size() == 2)
					break;
			}
			while (isRunning) {
				if (clients.stream().allMatch((c1) -> c1.isInitialized() && c1.getGameState() == GameState.MORPION)) {
					ArrayList<Client> cli = new ArrayList<Client>(2);
					cli.add(clients.get(1));
					cli.add(clients.get(0));
					Morpion m = new Morpion(cli);
					clients.remove(1);
					clients.remove(0);
					m.start();
					break;
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		run();
	}
}
