package fr.dome.server;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Scanner;

public class Serveur {
	public static void main(String[] args) {
		try {
			System.out.println(InetAddress.getLocalHost());
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
		Lobby.getInstance().start();

		Scanner sc = new Scanner(System.in);
		while (true) {
			String str = sc.nextLine();
			switch (str) {
			case "exit":
				sc.close();
				System.exit(0);
				return;
			case "list":
				System.out.println(String.format("%d players connected.", Lobby.getInstance().getPlayerList().size()));
				break;
			case "list -a":
				System.out.println(String.format("%d players connected.", Lobby.getInstance().getPlayerList().size()));
				for (Client c : Lobby.getInstance().getPlayerList())
					System.out.println("\t - " + c.getClientId() + " : " + c.getPseudo());
				break;
			}
		}
		
	}
}
