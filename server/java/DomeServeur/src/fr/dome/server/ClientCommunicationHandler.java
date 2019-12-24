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
	
	public ClientCommunicationHandler(InputStream in, OutputStream out) {
		this.in = new BufferedReader(new InputStreamReader(in));
		this.out = new OutputStreamWriter(out); 
	}
	

	public String read() {
		try {
			String str = in.readLine();
			System.out.println("Recu : " + str.length() + " : " + str);
			return str;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return "";
	}

	public void send(String str) {
		try {
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
		send(builder.toString());
		builder = new StringBuilder();
	}
}

