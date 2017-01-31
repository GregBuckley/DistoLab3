def join_new_client(client_sock,message_recieved):
        #Get info from client request
        chatroom =message_recieved[0].split(":")[1]
        print(chatroom)
        print(message_recieved)
        ip = message_recieved[1].split(":")[1]
        port =message_recieved[2].split(":")[1]
        client_name = message_recieved[3].split(":")[1]
        print 'chatroom = %s' % chatroom
        print 'ip  = %s' % ip
        print 'port  = %s' % port
        print 'client_name  = %s' % client_name
        global Clients_JoinID
        Clients_JoinID = Clients_JoinID + 1
        new_client = Client.Client(client_name,ip,port,Clients_JoinID,client_sock)
        roomRef = 0
        #Add clients to chatrrom

        for x in CHATROOM_LIST:
                print("Chatroom name =" + x.name)
                print("looking for:" + chatroom)
                if x.name == chatroom:
                        print 'adding  new to chatroom!'
                        x.clients.append(new_client)
                        roomRef = x.room_ref

                        #Response to client
                        sendToClient = "JOINED_CHATROOM:%s\nSERVER_IP:%s\nPORT:%s\nROOM_REF:%s\nJOIN_ID: %s\n" % (chatroom,ip_address,port,roomRef,new_client.Join_ID)
                        client_sock.sendall(sendToClient.encode())
                        print sendToClient


                        #inform other users of new cleint
                        for y in x.clients:
                                #letting other client know
                                chat_client_soc = y.socket
                               # inform_clients = "CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:Has Joined The Chatroom!\n\n" % (x.room_ref,client_name)
                                inform_clients = "CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s has joind this chatroom.\n\n"%(roomRef,client_name,client_name)
                                chat_client_soc.sendall(inform_clients.encode())



def send_message(client_sock,message_recieved):
        room_ref = message_recieved[0].split(":")[1]
        join_id  = message_recieved[1].split(":")[1]
        client_name = message_recieved[2].split(":")[1]
        message  = message_recieved[3].split(":")[1]
        print 'room_ref = %s' % room_ref
        print 'join_id  = %s' % join_id
        print 'client_name = %s' % client_name
        print 'message  = %s' % message

        for x in CHATROOM_LIST:
                print 'room_ref"%s" != x.room_ref"%s"' % (room_ref, x.room_ref)
                if x.room_ref == room_ref:
                        print 'Room found!'
                        #inform other users of new message
                        for y in x.clients:
                         #letting other client know
                                chat_client_soc = y.socket
                                inform_clients = "CHAT:%s\nCLIENT_NAME:%s\nMESSAGE:%s\n\n" % (x.room_ref,client_name,message)
                                chat_client_soc.sendall(inform_clients.encode())



def leave_chatroom(client_sock,message_recieved):
       #Get info from client request
        room_ref =message_recieved[0].split(":")[1]
        join_id= message_recieved[1].split(":")[1]
        join_id=(str(join_id)).strip()
        client_name = message_recieved[2].split(":")[1]
        print 'room_ref = %s' % room_ref
        print 'join_id  = %s' % join_id
        print 'client_name = %s' % client_name
        #remove client from  chatrrom
        for x in CHATROOM_LIST:
                if x.room_ref == room_ref:
                        for y in x.clients:
                                #letting client know they are leaving
                                if(str(y.Join_ID) == join_id):
                                        print("hdjfdh")
                                        chat_client_soc = y.socket
                                        inform_client = "LEFT_CHATROOM:%s\nJOIN_ID:%s\n" % (x.room_ref,join_id)
                                        chat_client_soc.sendall(inform_client.encode())

                        for p in x.clients:
                                #tell everyone about client leaving
                                chat_client_soc = p.socket
                                inform_client = "CHAT:%s\nCLIENT_NAME:%s\nMESSAGE: %s has left this chatroom.\n\n"%(x.room_ref,client_name,client_name)
                                chat_client_soc.sendall(inform_client.encode())


                        for n in x.clients:
                                #remove client
                                if(n.Join_ID == join_id):
                                        x.clients.remove(y)




def respond(client_sock, portnum):
        alive =True
        #Keep checking for data until socket is closed
        while(alive == True):
                data = client_sock.recv(1000)
                message_recieved = []

                message_recieved = data.split('\n')
                for x in message_recieved:
                        print '1: %s' % x

                if("JOIN_CHATROOM" in data):
                        join_new_client(client_sock, message_recieved)

                elif("CHAT:" in data):
                        send_message(client_sock,message_recieved)

                elif("LEAVE" in data):
                        leave_chatroom(client_sock,message_recieved)

                elif("KILL_SERVICE" in data):
                        alive=False
                        client_sock.close()

                elif("HELO" in data):
                        print 'received "%s"' % data
                        print 'sending data back to the client'
                        sendtoclient = "HELO BASE_TEST\nIP:%s\nPort:%d\nStudentID:%s" % (ip_address, portnum, STUDENT_ID)
                        client_sock.sendall(sendtoclient.encode())


def main():
        parse = argparse.ArgumentParser(description='')
        parse.add_argument("-start", help="port number needed")
        argument = parse.parse_args()
        portnum = 0
        if(argument.start):
                portnum = int(argument.start)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("10.62.0.148", portnum)
        print 'starting up on %s port %s' % server_address
        sock.bind(server_address)

        #Create chatrooms
        chatroom_one = Chatroom.Chatroom(" room1",server_address,portnum," 1",[])
        chatroom_two = Chatroom.Chatroom(" room2",server_address,portnum,"2",[])

        CHATROOM_LIST.append(chatroom_one)
        CHATROOM_LIST.append(chatroom_two)

        while True:
        # Waiting for a connection
                print 'waiting for a connection'
                sock.listen(5)
                client_sock, client_address = sock.accept()
                SOCKET_LIST.append(client_sock)
                print 'added new socket'

                #locate and remove dead threads
                for x in thread_pool:
                        if not x.isAlive:
                                thread_pool.remove(x)
                                print 'removed thread'

                print 'connection from', client_address
                #call thread to perform response
                if(len(thread_pool) < max_threads):
                        thread = threading.Thread(target = respond, args=(SOCKET_LIST.pop(), portnum))
                        thread.setDaemon(True)
                        thread_pool.append(thread)
                        thread.start()

main()








