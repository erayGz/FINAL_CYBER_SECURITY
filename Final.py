
import subprocess
import pyfiglet
import os
import sys
import socket
import winreg
import re
import codecs
import optparse
import random
from datetime import datetime

text = pyfiglet.figlet_format("FİNAL PROJESİ")
print(text)
print("1) Host/Port Tarama")
print("2) Mac Adresi Değiştirme")
print("3) Çıkış")
Secim=input("Seçiminizi Giriniz : ")


if(Secim=="1"):
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
if(Secim=="2"):
    print("##############################################################")
    print("1) Bu komut dosyasını yönetici ayrıcalıklarıyla çalıştırdığınızdan emin olun")
    print("2) WiFi bağdaştırıcının bir ağa bağlı olduğundan emin olun")
    print("##############################################################\n")


    mac_to_change_to = ["0A1122334455", "0E1122334455", "021122334455", "061122334455"]
    mac_addresses = list()
    macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")
    transportName = re.compile("({.+})")
    adapterIndex = re.compile("([0-9]+)")
    getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode().split('\n')

    for macAdd in getmac_output:
        macFind = macAddRegex.search(macAdd)
        transportFind = transportName.search(macAdd)
        if macFind == None or transportFind == None:
            continue
        mac_addresses.append((macFind.group(0), transportFind.group(0)))
    print("Hangi MAC Adresini güncellemek istiyorsunuz?")
    for index, item in enumerate(mac_addresses):
        print(f"{index} - Mac Address: {item[0]} - Transport Name: {item[1]}")
    option = input("Değiştirmek istediğiniz MAC'e karşılık gelen menü öğesi numarasını seçin:")
    while True:
        print("Hangi MAC adresini kullanmak istiyorsunuz? Bu, Ağ Kartının MAC adresini değiştirir.")
        for index, item in enumerate(mac_to_change_to):
            print(f"{index} - Mac Address: {item}")
        update_option = input("Kullanmak istediğiniz yeni MAC adresine karşılık gelen menü öğesi numarasını seçin:")
        if int(update_option) >= 0 and int(update_option) < len(mac_to_change_to):
            print(f"Mac Adresiniz şu şekilde değiştirilecektir: {mac_to_change_to[int(update_option)]}")
            break
        else:
            print("Geçerli bir seçenek belirlemediniz. Lütfen tekrar deneyin!")
    controller_key_part = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
        controller_key_folders = [("\\000" + str(item) if item < 10 else "\\00" + str(item)) for item in range(0, 21)]
        for key_folder in controller_key_folders:
            try:
                with winreg.OpenKey(hkey, controller_key_part + key_folder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                    try:
                        count = 0
                        while True:
                            name, value, type = winreg.EnumValue(regkey, count)
                            count = count + 1
                            if name == "NetCfgInstanceId" and value == mac_addresses[int(option)][1]:
                                new_mac_address = mac_to_change_to[int(update_option)]
                                winreg.SetValueEx(regkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac_address)
                                print("Başarıyla eşleştirilen Taşıma Numarası")
                                break
                    except WindowsError:
                        pass
            except:
                pass

    run_disable_enable = input("Kablosuz cihaz(lar)ınızı devre dışı bırakmak ve yeniden etkinleştirmek istiyor musunuz? Devam etmek için Y veya y tuşuna basın:")
    if run_disable_enable.lower() == 'y':
        run_last_part = True
    else:
        run_last_part = False
    while run_last_part:
        network_adapters = subprocess.run(["wmic", "nic", "get", "name,index"], capture_output=True).stdout.decode(
            'utf-8', errors="ignore").split('\r\r\n')
        for adapter in network_adapters:
            adapter_index_find = adapterIndex.search(adapter.lstrip())
            if adapter_index_find and "Wireless" in adapter:
                disable = subprocess.run(
                    ["wmic", "path", "win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call",
                     "disable"], capture_output=True)
                if (disable.returncode == 0):
                    print(f"Disabled {adapter.lstrip()}")
                enable = subprocess.run(
                    ["wmic", "path", f"win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call",
                     "enable"], capture_output=True)
                if (enable.returncode == 0):
                    print(f"Enabled {adapter.lstrip()}")
        getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode()
        mac_add = "-".join([(mac_to_change_to[int(update_option)][i:i + 2]) for i in
                            range(0, len(mac_to_change_to[int(update_option)]), 2)])
        if mac_add in getmac_output:
            print("Mac Address Başarılı")
        break
if (Secim==3):    {os.system('cls' if os.name == 'nt' else 'clear')}
else:
    {os.system('cls' if os.name == 'nt' else 'clear')}
