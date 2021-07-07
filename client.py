import socket
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import Crypto.Cipher
from Crypto.Cipher import AES
import random
from main import serverPublicKey # public key of server imported

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # socket object created
socketClient.connect(("", 9998))    # socket connection is created at the port number 9998

fileCreate = open("LoginInfo.txt","a")  # file opened at append mode

selection = input("1. Register\n2. Login\n") # getting input

if(selection == '1'):
    key = rsa.generate_private_key(backend=crypto_default_backend(), public_exponent=65537, key_size=2048)      # key generator created
    privateKey = key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8,crypto_serialization.NoEncryption())     # private key created
    publicKey = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH)     # public key created

    privateKey = privateKey[28:]    # unnecessary part of private key deleted
    publicKey = publicKey[8:]       # unnecessary part of public key deleted

    username = input("Please enter your username: ")    # getting username input
    password = input("Please enter your password: ")    # getting password input

    fileCreate.write("\n")
    fileCreate.write("\n")
    fileCreate.write(username)      # write username info to LoginInfo.txt file
    fileCreate.write("\n")
    fileCreate.write(password)      # write password info to LoginInfo.txt file
    fileCreate.write("\n")
    fileCreate.write(str(publicKey))    # write publicKey info to LoginInfo.txt file

    print("Private Key:", privateKey)
    print("Public Key:" , publicKey)
elif(selection == '2'):
    fileCheck = open("LoginInfo.txt","r") # opening a LoginInfo.txt file in read mode
    registrations = fileCheck.read()    # reading all of the login information
    usernameCheck = input("Please enter your username: ")   # getting username as input
    passwordCheck = input("Please enter your password: ")   # getting password as input
    keyCheck = input("Please enter your public key: ")  # getting user's public as input

    if usernameCheck in registrations:  # checking username in records
        if passwordCheck in registrations:  # checking password in records
            if keyCheck in registrations:   # checking public key in records
                print("Access granted!")

                iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])     # creating initial vector
                aes = Crypto.Cipher.AES.new(serverPublicKey, Crypto.Cipher.AES.MODE_CBC, iv)        # creating aes object in a cbc mode

                file = open("img.png", "rb")    # opening picture in read byte mode
                print("Image file successfully opened!")
                data = file.read(1024)  # reading file in 1024 sized chunks
                encryptedData = aes.encrypt(data)   # encrypting image data
                data = encryptedData    # replacing normal data with encrypted data
                print("Encrypted!")
                while (data):
                    print("Sending...")
                    socketClient.send(data) # sending encypted data to server
                    data = file.read(1024)  # reading file in 1024 sized chunks

                file.close()
                print("Sending Completed!")
                socketClient.shutdown(socket.SHUT_WR)   # socket connection ended
                print(socketClient.recv(1024))
                socketClient.close()    # socket client closed
            else:
                print("Key not found!")
        else:
            print("Password is wrong")
    else:
        print("Username is not found")
else:
    print("You made an unknown choice, try again!")


