package fr.dome.server;

import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.UnknownHostException;
import java.util.ArrayList;

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
}
