package fr.dome.server;

import java.util.Scanner;

public class Serveur {
	public static void main(String[] args) {
		MainLobby.getInstance().start();

		Scanner sc = new Scanner(System.in);
		while (true) {
			String str = sc.nextLine();
			switch (str) {
			case "exit":
				sc.close();
				System.exit(0);
				return;
			case "list":
				System.out.println(String.format("%d players connected.", MainLobby.getInstance().getPlayerList().size()));
				break;
			case "list -a":
				System.out.println(String.format("%d players connected.", MainLobby.getInstance().getPlayerList().size()));
				for (Client c : MainLobby.getInstance().getPlayerList())
					System.out.println("\t - " + c.getClientId() + " : " + c.getPseudo());
				break;
			case "list -g":
				for (Lobbies.GameLobby l : Lobbies.getInstance().games_list.values()) {
					System.out.println(l.size());
				}
			}
		}

	}
}
