import socket as sk
import os
import sys
import time


SocketServer = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
ServerAddress = ('localhost', 10000)
SocketServer.bind(ServerAddress)
print('The Server strating up on %s port: %s' % ServerAddress)

while True:

    print("\n\r waiting to receive message...")
    
    data, address = SocketServer.recvfrom(4096)
    print('\n\r received %s bytes from %s' % (len(data), address))
    request = data.decode('utf8')
    print( request)

    try:
        if len(request)>0:

            if request == "ls":

                ServerFiles = os.listdir(
                    os.path.join(os.getcwd(), "ServerFiles"))
                sent = SocketServer.sendto(
                    ServerFiles.__str__().encode('utf8'), address)
                #ServerResponse="HTTP1.1 200 OK Server Files Sended"
                sent = SocketServer.sendto(
                       "HTTP1.1 200 OK Server Files Sended".encode(), address)
                print("Server Filse: %s " % ServerFiles.__str__())

            elif request == "upload":

                ServerResponse='HTTP/1.1 200 OK Ready To Receive File'
                
                sent = SocketServer.sendto(ServerResponse.encode(), address)
                
                print("Waiting the uploading of file...")
                data = SocketServer.recv(4096)
                fileToUpload = data.decode('utf8')
                
                Pathfolder = os.path.join(os.getcwd(),"ServerFiles")
                Pathfile = os.path.join(Pathfolder,""+fileToUpload+"")
                
                File = open(""+Pathfile+"",'w')
                data = SocketServer.recv(4096)
                File.write(data.decode('utf8'))
                File.close()
                
                print('File Uploaded with success')
                
                ServerResponse='HTTP/1.1 200 OK Uploaded File Done'
                sent = SocketServer.sendto(ServerResponse.encode(), address)

            elif request == "download":

                 
                 ServerFiles = os.listdir(
                     os.path.join(os.getcwd(),"ServerFiles"))
                 
                 sent = SocketServer.sendto(
                     ServerFiles.__str__().encode('utf8'), address)
                 
                 print("Waiting to know how files to send...")
                 data = SocketServer.recv(4096)
                 file = data.decode('utf8')
                 
                 PathFolder = os.path.join(os.getcwd(),"ServerFiles")
                 PathFolder = os.path.join(PathFolder,""+file+"")

                 if os.path.exists(PathFolder):

                    responseServer = 'HTTP/1.1 200 OK File is on the Server'
                    sent = SocketServer.sendto(responseServer.encode(), address)

                    file = open(""+PathFolder+"",'r')
                    sent = SocketServer.sendto(
                        file.read().__str__().encode('utf8'), address)
                    time.sleep(2)

                    responseServer ='HTTP/1.1 200 OK File Downloaded'
                    sent = SocketServer.sendto(responseServer.encode(), address)

                 else:
                     
                    time.sleep(2)
                    responseServer = 'HTTP/1.1 404 Error File Not Found'
                    sent = SocketServer.sendto(responseServer.encode(), address)

        else:
                print("\n\r The message received is empty")
                   

    except Exception as e:
           responseServer = 'HTTP/1.1 500 Internal Server Error'
           sent = SocketServer.sendto(responseServer.encode('utf8'), address)
           
           print(e)
           
           SocketServer.close()
           sys.exit()              
               
                
                
