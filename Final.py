
import pyfiglet
import os


text = pyfiglet.figlet_format("FİNAL PROJESİ")
print(text)
print("1) Port Tarama")
print("2) Mac Adresi Değiştirme")
print("3) DDoS")
print("4) Wifi bağlanan cihazların Mobil erişim noktasının şifresini gösterme ")
print("5) Çıkış")
Secim=input("Seçiminizi Giriniz : ")


if(Secim=="1"):
    import PortScanner
    print(PortScanner)
if(Secim=="2"):
    import MacAddresChange
    print(MacAddresChange)
if(Secim=="3"):
    import DDoS
    print(DDoS)
if (Secim=="4"):
    import Wifi
    print(Wifi)
if (Secim=="5"):
    {os.system('cls' if os.name == 'nt' else 'clear')}

