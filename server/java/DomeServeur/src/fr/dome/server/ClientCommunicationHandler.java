package fr.dome.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

public class ClientCommunicationHandler {

	private OutputStreamWriter out; // Objet permettant d'envoyer simplement des messages.
	private BufferedReader in; // Flux d'entrée.

	private StringBuilder builder = new StringBuilder();
	@SuppressWarnings("unused")
	private String pseudo;
	private int id;

	public ClientCommunicationHandler(int id, InputStream in, OutputStream out) {
		this.in = new BufferedReader(new InputStreamReader(in));
		this.out = new OutputStreamWriter(out);
		this.id = id;
	}

	public void setPseudo(String pseudo) {
		this.pseudo = pseudo;
	}

	@SuppressWarnings("deprecation")
	public String read() {
		try {
			String str = in.readLine();
			System.out.println("Recu : " + str.length() + " : " + str);
			return str;
		} catch (IOException e) {
			e.printStackTrace();
			Thread.currentThread().stop();
		}
		return "";
	}

	public void send(String str) {
		try {
			System.out.println("Flush " + pseudo + "(" + id + ")" +  " : " + str);
			out.write(str);
			out.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void write(String string) {
		builder.append(string);
	}

	public void flush() {
		//System.out.println("Flush " + pseudo + " : " + builder.toString());
		send(builder.toString());
		builder = new StringBuilder();
	}
}
