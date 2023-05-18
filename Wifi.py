

#    Sistem komutlarını kullanabilmemiz için alt işlemi içe aktarın.
import subprocess

#    Normal ifadeleri kullanabilmemiz için re modülünü içe aktarın.
import re

#    Python, işlevi kullanarak sistem komutlarını çalıştırmamıza izin verir
#    alt işlem modülü tarafından sağlanan;
#    (subprocess.run(<komut satırı bağımsız değişkenlerinin listesi buraya gidin>, <çıktıyı yakalamak
#    istiyorsanız ikinci bağımsız değişkeni belirtin>)).

#    Bu komut dosyası, aşağıdaki özelliklere sahip bir alt işlem oluşturan bir üst işlemdir:
#      Bir sistem komutu çalıştırır ve yalnızca alt işlem bir kez devam eder
#   tamamlandı.
#   Standart çıkış akışına gönderilen içerikleri kaydetmek için
# (terminal), öncelikle çıktıyı yakalamak istediğimizi belirtmeliyiz.
# Bunu yapmak için ikinci argümanı capture_output = Doğru olarak belirtiriz.
# Bu bilgiler stdout özniteliğinde bayt olarak depolanır ve
# Python'da String olarak kullanılmadan önce kodunun çözülmesi gerekir.
#
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

#    Normal ifadeleri kullanmak için re modülünü içe aktardık.
#  Biz sonra listelenen tüm wifi isimleri bulmak istiyorum
#  "TÜM Kullanıcı Profili :". Normal ifadeler kullanarak oluşturabiliriz
# dönüş kaçış sırası (r) görünene kadar tüm karakterlerden oluşan bir grup.
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

#    Döngünün dışında sözlüklerin bulunduğu boş bir liste oluşturuyoruz
# # içeren tüm wifi kullanıcı adları ve şifreleri kaydedilecektir.
wifi_list = []

#    Herhangi bir profil adı bulunamazsa, bu wifi bağlantılarının olduğu anlamına gelir
# # da bulunamadı. Bu yüzden kontrol etmek için bu bölümü çalıştırıyoruz
# # wifi detaylarını ve şifrelerini alıp alamayacağımızı görün.
if len(profile_names) != 0:
    for name in profile_names:
        # Her wifi bağlantısının kendi sözlüğüne ihtiyacı olacaktır.
        # değişkenine wifi_list eklenecektir.
        wifi_profile = {}
        # Artık bilgileri görmek için daha spesifik bir komut çalıştırabiliriz
        # wifi bağlantısı hakkında ve eğer Güvenlik anahtarı
        # yok ise şifreyi almak mümkün olabilir.
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        #    Normal ifadeyi yalnızca eksik vakaları aramak için kullanırız, böylece onları görmezden gelebiliriz.
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            #    Wifi profilinin ssid'sini ssözlüğe atayın.
            wifi_profile["ssid"] = name
            #    Bu vakalar yok değil ve
            #             # "key=clear" komutunun şifresini almak için.
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            #    Yakalamak için normal ifadeyi yeniden çalıştırın
            #             # grubundan sonra : (şifre olan).
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            #    Normal ifadeyi kullanarak bir şifre bulup bulmadığımızı kontrol edin.
            #             # Bazı wifi bağlantılarının şifreleri olmayabilir.
            if password == None:
                wifi_profile["password"] = None
            else:
                # Gruplandırmayı (şifrenin bulunduğu yere) şu şekilde atarız:
                # Sözlükteki şifre anahtarı ile ilgileniyoruz.
                wifi_profile["password"] = password[1]
            #    Wifi bilgilerini değişken wifi_list ekliyoruz.
            wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
    print(wifi_list[x])
