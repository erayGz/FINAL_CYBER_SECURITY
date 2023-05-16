#!/usr/bin/env python3
##################################################################################################
#Copyright of David Bombal, 2021                                                                 #
#https://www.davidbombal.com                                                                     #
#https://www.youtube.com/davidbombal                                                             #
#                                                                                                #
# Please note that this code can be improved by using functions. It is not programmed to cater   #
# for all situations, but to be used as a learning tool.                                         #
#                                                                                                #
# This code is provided for educational purposes only. Do good. Be Ethical.                      #
#                                                                                                #
##################################################################################################

import subprocess
import winreg
import re
import codecs

print("##############################################################")
print("1) Make sure you run this script with administrator privileges")
print("2) Make sure that the WiFi adapter is connected to a network")
print("##############################################################\n")

# Kullanmaya çalışılacak MAC Adresleri. Komut dosyası kullanıldığında birini seçeceksiniz.
# Bu listedeki isimleri değiştirebilir veya bu listeye isim ekleyebilirsiniz.
# 12 geçerli onaltılık değer kullandığınızdan emin olun.
# MAC adresi değişikliği başarısız olursa, ikinci karakteri 2 veya 6 veya A veya E olarak ayarlamayı deneyin,
# örneğin: 0A1122334455 veya 0A5544332211
# Emin değilseniz, burada listelenen MAC adreslerini olduğu gibi bırakın.
mac_to_change_to = ["0A1122334455", "0E1122334455", "021122334455", "061122334455"]

# Tüm MAC adreslerini saklayacağımız boş bir liste oluşturuyoruz.
mac_addresses = list()

# MAC adresleri için normal bir ifade (regex) oluşturarak başlıyoruz.
macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")

# Taşıma adları için bir regex oluşturuyoruz. Bu durumda işe yarayacaktır.
# # Ancak .+ veya .* kullandığınızda, açgözlü olmamayı düşünmelisiniz.
transportName = re.compile("({.+})")

# Adaptör dizinini seçmek için regex oluşturuyoruz.
adapterIndex = re.compile("([0-9]+)")

# Python, alt işlem modülü tarafından sağlanan bir işlevi kullanarak sistem komutlarını çalıştırmamızı sağlar:
# (subprocess.run(<komut satırı bağımsız değişkenlerinin listesi buraya gider>,
# <çıktıyı yakalamak istiyorsanız ikinci bağımsız değişkeni belirtin>))
# Komut dosyası bir üst işlemdir ve sistem komutunu çalıştıran bir alt işlem oluşturur,
# ve yalnızca alt işlem tamamlandıktan sonra devam eder.
# Standart çıktı akışına (terminal) gönderilen içeriği kaydetmek için,
# çıktıyı yakalamak istediğimizi belirtmeliyiz, bu yüzden ikincisini belirtelim
# argümanı capture_output = Doğru olarak. Bu bilgiler stdout özniteliğinde depolanır.
# Bilgiler bayt olarak saklanır ve kullanmadan önce Unicode'a çözmemiz gerekir
# Python'da bir dize olarak.
# Getmac komutunu çalıştırmak ve ardından çıktıyı yakalamak için Python kullanıyoruz.
# Tek tek satırlarla çalışabilmemiz için çıktıyı yeni satırda bölüyoruz
# (Mac ve taşıma adını içerecektir).
getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode().split('\n')

# Çıktıda döngü yapıyoruz
for macAdd in getmac_output:
    # Mac Adreslerini bulmak için regex kullanıyoruz.
    macFind = macAddRegex.search(macAdd)
    # Taşıma adını bulmak için regex kullanıyoruz.
    transportFind = transportName.search(macAdd)
    # Bir Mac Adresi veya Aktarım adı bulamazsanız, seçenek listelenmez.
    if macFind == None or transportFind == None:
        continue
    # Bir listeye Mac Adresi ve Taşıma adını içeren bir demet ekliyoruz.
    mac_addresses.append((macFind.group(0),transportFind.group(0)))

# Kullanıcının güncellemek istediği Mac Adresini seçmek için basit bir menü oluşturun.
print("Which MAC Address do you want to update?")
for index, item in enumerate(mac_addresses):
    print(f"{index} - Mac Address: {item[0]} - Transport Name: {item[1]}")

# Kullanıcıdan güncellemek istediği Mac Adresini seçmesini isteyin.
option = input("Select the menu item number corresponding to the MAC that you want to change:")

# Kullanıcının kullanmak üzere bir MAC adresi seçebilmesi için basit bir menü oluşturun
while True:
    print("Which MAC address do you want to use? This will change the Network Card's MAC address.")
    for index, item in enumerate(mac_to_change_to):
        print(f"{index} - Mac Address: {item}")

    # Kullanıcıdan, değiştirmek istediği MAC adresini seçmesini isteyin.
    update_option = input("Select the menu item number corresponding to the new MAC address that you want to use:")
    # Kullanıcının seçtiği seçeneğin geçerli bir seçenek olup olmadığını kontrol edin.
    if int(update_option) >= 0 and int(update_option) < len(mac_to_change_to):
        print(f"Your Mac Address will be changed to: {mac_to_change_to[int(update_option)]}")
        break
    else:
        print("You didn't select a valid option. Please try again!")

# Anahtarın ilk kısmını biliyoruz, değerleri arayacağımız klasörleri ekleyeceğiz
controller_key_part = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

# HKEY_LOCAL_MACHINE kayıt defterine bağlanıyoruz. Hiçbirini belirtirsek,
# Yerel makinenin kayıt defterine bağlandığımız anlamına gelir.
with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
    # 21 klasör için bir liste oluşturun. Bir liste anlayışı kullandım. Liste anlamanın ifade kısmı
    # üçlü işleç kullanır. Mac Adresiniz için taşıma değeri bu aralıkta olmalıdır.
    # Birden fazla satır yazabilirsiniz.
    controller_key_folders = [("\\000" + str(item) if item < 10 else "\\00" + str(item)) for item in range(0, 21)]
    # Şimdi oluşturduğumuz klasörlerin listesini tekrarlıyoruz.
    for key_folder in controller_key_folders:
        # Anahtarı açmaya çalışıyoruz. Eğer yapamazsak, sadece hariç tutarız ve geçeriz. Ama bu bir sorun olmamalı.
        try:
            # Bağlandığımız kayıt defterini, controller anahtarını belirtmeliyiz
            # (Bu, bildiğimiz controller_key_part ve oluşturduğumuz klasör (anahtar) adından oluşur
            # liste anlayışı ile).
            with winreg.OpenKey(hkey, controller_key_part + key_folder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                # Şimdi her anahtarın altındaki Değerlere bakacağız ve "NetCfgInstanceId" i bulup bulamayacağımıza bakacağız.
                # seçtiğimiz Taşıma Kimliği ile aynı Taşıma Kimliğine sahip.
                try:
                    # Değerler kayıt defterinde 0'dan başlar ve bunları saymamız gerekir.
                    # Bu, bir WindowsError alana kadar devam edecektir (Daha sonra geçeceğimiz yer)
                    # Ardından, aşağıdakileri içeren doğru anahtarı bulana kadar bir sonraki klasörle başlayacağız:
                    # Aradığımız değer.
                    count = 0
                    while True:
                        # Her bir winreg değerini ad, değer ve tür olarak açıyoruz.
                        name, value, type = winreg.EnumValue(regkey, count)
                        # Bir sonraki değere geçmek için, aradığımızı bulamadıysak, sayıyı artırırız.
                        count = count + 1
                        # "NetCfgInstanceId" değerimizin bizim için Transport numaramıza eşit olup olmadığını kontrol ediyoruz.
                        # seçilen Mac Adresi.
                        if name == "NetCfgInstanceId" and value == mac_addresses[int(option)][1]:
                            new_mac_address = mac_to_change_to[int(update_option)]
                            winreg.SetValueEx(regkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac_address)
                            print("Successly matched Transport Number")
                            # Adaptörlerin listesini alın ve devre dışı bırakmak istediğiniz adaptörün dizinini bulun.
                            break
                except WindowsError:
                    pass
        except:
            pass


# Kablosuz cihazları devre dışı bırakmak ve etkinleştirmek için kod
run_disable_enable = input("Do you want to disable and reenable your wireless device(s). Press Y or y to continue:")
# Girişi küçük harfe değiştirir ve y ile karşılaştırır. Y değilse, son parçayı içeren while işlevi asla çalışmaz.
if run_disable_enable.lower() == 'y':
    run_last_part = True
else:
    run_last_part = False

# run_last_part, yukarıdaki koda göre Doğru veya Yanlış olarak ayarlanacaktır.
while run_last_part:

    # Ağ bağdaştırıcılarını devre dışı bırakmak ve etkinleştirmek için kod
    # Tüm ağ bağdaştırıcılarının bir listesini alıyoruz. Komutun verileri döndürdüğü biçimi beğenmediği için hataları yok saymanız gerekir.
    network_adapters = subprocess.run(["wmic", "nic", "get", "name,index"], capture_output=True).stdout.decode('utf-8', errors="ignore").split('\r\r\n')
    for adapter in network_adapters:
        # Her adaptör için indeksi alıyoruz
        adapter_index_find = adapterIndex.search(adapter.lstrip())
        # Bir dizin varsa ve adaptörün açıklamasında kablosuz varsa, adaptörü devre dışı bırakıp etkinleştireceğiz
        if adapter_index_find and "Wireless" in adapter:
            disable = subprocess.run(["wmic", "path", "win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "disable"],capture_output=True)
            # Dönüş kodu 0 ise, bağdaştırıcıyı başarıyla devre dışı bıraktığımız anlamına gelir
            if(disable.returncode == 0):
                print(f"Disabled {adapter.lstrip()}")
            # Şimdi ağ bağdaştırıcısını yeniden etkinleştiriyoruz.
            enable = subprocess.run(["wmic", "path", f"win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "enable"],capture_output=True)
            # Dönüş kodu 0 ise, bağdaştırıcıyı başarıyla etkinleştirdiğimiz anlamına gelir
            if (enable.returncode == 0):
                print(f"Enabled {adapter.lstrip()}")

    # Getmac komutunu tekrar çalıştırıyoruz
    getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode()
    # Sahip olduğumuz 12 karakterlik dizeden getmac XX-XX-XX-XX-XX-XX-XX formatında ot göründüğü için Mac Adresini yeniden oluşturuyoruz. Dizeyi liste anlamalarını kullanarak 2 uzunluğundaki dizelere böldük ve sonra. Adresi yeniden oluşturmak için "-".join(list) kullanıyoruz
    mac_add = "-".join([(mac_to_change_to[int(update_option)][i:i+2]) for i in range(0, len(mac_to_change_to[int(update_option)]), 2)])
    # Değiştirdiğimiz Mac Adresinin getmac çıktısında olup olmadığını kontrol etmek istiyoruz, eğer öyleyse başarılı olduk.
    if mac_add in getmac_output:
        print("Mac Address Success")
    # While döngüsünden çıkın. Ayrıca run_last_part False olarak da değiştirebilir.
    break