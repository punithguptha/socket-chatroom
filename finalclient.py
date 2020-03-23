import tkinter
import socket
from threading import Thread
import time
import errno
import sys

window=tkinter.Tk()
window.title("Chat Room")

#time.sleep(2)

def receive():
	while True:
		try:
			while True:
				msgdash=client.recv(2048).decode("utf-8")
				print(msgdash)
				msgList.insert(tkinter.END,msgdash)
				msgList.see("end")
		except IOError as e:
			if e.errono!=errno.EAGAIN and e.errno!=errno.EWOULDBLOCK:
				print("Reading Error:{}",format(str(e)))
				sys.exit()
			continue
		except Exception as e:
			print("Error occured while reading other client messages")
			sys.exit()
			break

def funct1(event=None):
	#print("Hello World")
	dummy="You"+':'+str(inputmsg.get())
	msgList.insert(tkinter.END,dummy)
	msgList.see("end")
	msgdummy=str(inputmsg.get())
	inputmsg.set("")
	client.send(bytes(msgdummy,"utf-8"))
	if msgdummy=="quit":
		client.close()
		window.quit()

def on_closing(event=None):
	inputmsg.set("quit")
	funct1()

TopFrame=tkinter.Frame(window)
TopFrame.pack()
scrollbar1=tkinter.Scrollbar(TopFrame)
scrollbar1.pack(side='right',fill=tkinter.Y)
msgList=tkinter.Listbox(TopFrame,height=15,width=50,yscrollcommand=scrollbar1.set)
msgList.pack(side="left",fill='both')
InputFrame=tkinter.Frame(window)
InputFrame.pack(side="bottom")
inputmsg=tkinter.StringVar()
msg_entry=tkinter.Entry(InputFrame,textvariable=inputmsg)
msg_entry.bind("<Return>",funct1)
msg_entry.pack(side='left')
submit_button=tkinter.Button(InputFrame,text="Submit",command=funct1)
submit_button.pack(side="left")

window.protocol("WM_DELETE_WINDOW",on_closing)

IP="127.0.0.1"
PORT=1250
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((IP,PORT))
#client.setblocking(False)

receive_thread=Thread(target=receive)
receive_thread.start()

window.mainloop()