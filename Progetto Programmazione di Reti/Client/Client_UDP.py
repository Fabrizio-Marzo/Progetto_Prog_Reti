import socket as sk
import sys
import os
import time


def Status(string, ClientSocket):
    StatusCode = string[9:12]
    if(StatusCode == '200'):
        print(string)
    elif(StatusCode == '404'):
        print(string)
    elif(StatusCode == '500'):
        print(string)
        ClientSocket.close()
        sys.exit()


def SendCommand(string):
    sent = ClientSocket.sendto(command.__str__().encode('utf8'), ServerAddress)


commands = ['ls', 'download', 'upload', 'exit']
ClientSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
ServerAddress = ('localhost', 10000)

while True:

    print("")
    print('Commands available: %s' % (commands.__str__()))
    command = input("Choose one of them : ")

    try:

        if commands.__contains__(command):
            lista = os.listdir(os.path.join(os.getcwd(), "ClientFiles"))
        
            
            if command == "upload":

                while True:
                    
                    print('You have these files: %s' % (lista.__str__()))
                    FileToUpload = input('Write a file to upload :')
                    if lista.__contains__(FileToUpload):
                        break
                    else:
                        print("This file doesn't exists! Try Again")
                        print("")

            SendCommand(command)
            
            if command=='upload':
               
               time.sleep(2)
               
               print('Waiting ok from Server to Upload')
               
               
               data, server = ClientSocket.recvfrom(4096)
               ServerResponse = data.decode('utf8')
               Status(ServerResponse, ClientSocket)
               
               sent = ClientSocket.sendto(
                FileToUpload.__str__().encode('utf8'), ServerAddress)

               PathFolder = os.path.join(os.getcwd(),"ClientFiles")
               PathFile = os.path.join(PathFolder,""+FileToUpload+"")
               File = open(PathFile, 'r')
               sent = ClientSocket.sendto(
               File.read().__str__().encode('utf8'), ServerAddress)
               File.close()

               print('Waiting ending of upload')
               data = ClientSocket.recv(4096)
               time.sleep(2)
               ServerResponse = data.decode('utf8')
               Status(ServerResponse, ClientSocket)


            elif command == 'ls':
               
               #SendCommand(command)
               
               print('Waiting to receive list of files from Server ')
               data, server =ClientSocket.recvfrom(4096)
               ServerFiles=data.decode('utf8')
               time.sleep(2)
            
               data = ClientSocket.recv(4096)
               ServerResponse=data.decode('utf8')
               print(ServerResponse)
               Status(ServerResponse,ClientSocket)
               print('Files on server are : %s' % (ServerFiles.__str__()))
            
            elif command=='download':
               #SendCommand(command)
            
               data , server = ClientSocket.recvfrom(4096)
               ServerFiles = data.decode('utf8')
            
               print('Choose a file to Download: %s' %ServerFiles.__str__())
               FileToDownload = input('Digit the file to Download: ')
               
               sent=ClientSocket.sendto(FileToDownload.encode('utf8'), ServerAddress)
            
               print('Waiting cheking of exist file..')
               
               data = ClientSocket.recv(4096)
               ServerResponse = data.decode('utf8')
               time.sleep(1)
               Status(ServerResponse, ClientSocket)
            
               if ServerResponse[9:12] == "200":
                
                  print('Waiting ending of download')
                  PathFolder = os.path.join(os.getcwd(), "ClientFiles")
                  PathFolder = os.path.join(PathFolder,""+FileToDownload+"")
                
                  File=open(""+PathFolder+"",'w')
                  data=ClientSocket.recv(4096)
                  File.write(data.decode('utf8'))            
                  File.close()
                
                
                  data = ClientSocket.recv(4096)
                  ServerResponse=data.decode('utf8')
                  time.sleep(1)
                  Status(ServerResponse, ClientSocket)
                  
                
                
            elif command=="exit":
              print('\n\rExit with success..')
              ClientSocket.close()
              sys.exit()
            
        else: 
            print('Command Error') 



    except Exception as Info:
         print(Info)







