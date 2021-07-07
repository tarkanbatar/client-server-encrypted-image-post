import random
import socket,os
from Crypto.Cipher import  AES

socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket server created
socketServer.bind(("", 9998))            # socket server assigned to port number 9998 at localhost
socketServer.listen(5)

file = open("img.png", "wb")        # image file opened

serverPublicKey = os.urandom(32)        # 32 byte random number created
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(32)])     # initial vector created
aes = AES.new(serverPublicKey,AES.MODE_CBC,iv)      # aes object created in cbc mode

while (1):
    c, addr = socketServer.accept()  # supplies socket object and address info
    print("Got connection from: ", addr)    # printing socket address to console
    print("Receiving...")
    data = c.recv(1024)             # receiving 1024 sized chunk from socket object

    while(data):
        decryptedData = aes.decrypt(data)   # received data decrypted and assigned to decryptedData variable
        print("Decrypting...")

    while (decryptedData):
        print("Receiving...")
        file.write(decryptedData)    # decrypted data wrote to "img.png" file
        decryptedData = c.recv(1024)    # getting received data

    file.close()    # file operator closed
    print("Done Receiving!")


    if(decryptedData):      # notification message
        print("Notification: New Image Received!")
    c.close()   # socket object is closed