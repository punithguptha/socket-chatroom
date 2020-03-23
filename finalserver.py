import socket
from threading import Thread

def accept_connections():
	while True:
			client_socket,client_address=server_socket.accept()
			print(f"Client {client_address} is connected to server!!..")
			client_socket.send(bytes("Welcome to server.Enter your name to continue..","utf-8"))
			Thread(target=handle_client,args=(client_socket,)).start()

def handle_client(client_sock):
	username=client_sock.recv(2048).decode("utf-8")
	clients[client_sock]=username
	msg=f"User {username} has joined the chat!!.."
	print(msg)
	broadcast_message(msg,client_sock)
	socket_list.append(client_sock)	
	while True:
		receivedmessage=client_sock.recv(2048).decode("utf-8")
		actualreceivedmessage=receivedmessage
		receivedmessage=clients[client_sock]+":"+receivedmessage
		print(receivedmessage)
		if actualreceivedmessage!="quit":
			print("Inside if of handle_client method")
			broadcast_message(receivedmessage,client_sock)
		else:
			msgdummy=f"User {clients[client_sock]} has left"
			print(msgdummy)
			client_sock.close()
			del clients[client_sock]
			socket_list.remove(client_sock)
			broadcast_message(msgdummy,client_sock)
			break

def broadcast_message(message,client_socket):
	for socket in socket_list:
		if socket!=client_socket:
			socket.send(bytes(message,"utf-8"))

clients={}
socket_list=[]

HOST=''
PORT=1250
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))

if __name__=="__main__":
	server_socket.listen(5)
	print("Waiting for connection!!..")
	MAIN_THREAD=Thread(target=accept_connections)
	MAIN_THREAD.start()
	MAIN_THREAD.join()
	server_socket.close()

