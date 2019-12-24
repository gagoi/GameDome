import socket
import time as t

# HOST = '127.0.0.1'
# PORT = 8081
HOST = '192.168.43.254'
PORT = 45703

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print('Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.')

message = 'NCnyrvana\n'
print('Envoi de :' + message)
n = client.send(bytes(message, 'utf-8'))
if (n != len(message)):
    print( 'Erreur envoi.')
else:
    print( 'Envoi ok.')

client.send(bytes("message\n", 'utf-8'))
t.sleep(3000000)
print('Deconnexion.')
client.close()