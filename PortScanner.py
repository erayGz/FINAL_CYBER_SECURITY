import  socket
import sys
from datetime import datetime

Hedef = input(str("Hedef IP : "))
try:
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((Hedef,port))
        if result ==0:
            print("[*] Port {} Açık".format(port))
        s.close()
except KeyboardInterrupt:
        print("\n Çıkış Yapılıyor:(")
        sys.exit()
except socket.error:
        print(" \ Host Yanıt Vermiyor :(")
        sys.exit()