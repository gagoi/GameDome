import java.io.IOException;
import java.net.ServerSocket;
import java.util.ArrayList;

public class Serveur implements Runnable {

	private static final int ERROR_SERVER = 2;
	private ArrayList<Client> clients = new ArrayList<Client>();

	private final int PORT = 45703;
	private ServerSocket socket;
	private boolean isRunning = true;

	public static void main(String[] args) {
		Serveur s = new Serveur();
		Thread t = new Thread(s);
		t.start();
	}

	public Serveur() {
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
				if (clients.size() == 2 && clients.stream().allMatch((c1) -> c1.isInitialized())) {
					Morpion m = new Morpion(clients.get(0), clients.get(1));
					clients.remove(0);
					clients.remove(1);
					m.start();
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void kill() {

	}
}
