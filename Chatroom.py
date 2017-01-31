class Chatroom(object):


        def __init__ (self,name, server_ip, port, room_ref,list_clients):
                self.name = name
                self.server_iP = server_ip
                self.port = port
                self.room_ref = room_ref
                self.clients = list_clients

        def add_client(self,new_client):
                self.clients.append(new_client)





