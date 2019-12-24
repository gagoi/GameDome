import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.stream.Collectors;

public class Client extends Thread {
	private static int ids = 0;			// Nombre de clients qui se sont connectés au serveur.
	
	private final Socket socket;		// Socke IPV4 correspondant à ce client.
	private final int id;				// Id du client.
	private OutputStreamWriter out; 	// Objet permettant d'envoyer simplement des messages.
	private InputStream in;				// Flux d'entrée.

	private boolean isRunning = true;	// Le client est connecté.

	/**
	 * Permet de construire un client, qui correspond à un socket de connection.
	 * 
	 * @param socket Connexion au client distant.
	 * @param statement Accès à la base de données.
	 */
	public Client(Socket socket) {
		this.socket = socket;
		this.id = ++ids;
		try {
			out = new OutputStreamWriter(socket.getOutputStream());
			in = socket.getInputStream();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Ferme convenablement le socket, et arrête les traitements du thread.
	 */
	public void preStop() {
		try {
			socket.close();
			isRunning = false;
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Conversion des informations arrivant sur un flux d'entrée en une chaîne plus simple de traitement.
	 * @param input Flux d'entrée depuis lequel il faut récupérer les infos.
	 * @return L'information entrante sous forme de chaîne de caractères.
	 * @throws IOException
	 */
	public static String read(InputStream input) throws IOException {
        try (BufferedReader buffer = new BufferedReader(new InputStreamReader(input))) {
            return buffer.lines().collect(Collectors.joining("\n"));
        }
    }
	
	
	public String read() throws IOException {
		String str = read(in);
		System.out.println(id + " : " + str);
		return str;
	}

	public void send(String str) throws IOException {
		out.write(str);
		out.flush();
	}

	@Override
	public void run() {
		while (isRunning) {
			try {
				switch(read()) {
					case "NC":
						System.out.println("newplayer");
						break;
				}
			} catch (IOException e) { // Il y a un problème de connection avec le client.
				preStop(); // On déconnecte complètement.
			}
		}
	}
}
