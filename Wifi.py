import subprocess
import re

def get_wifi_password(bssid):
    command = "sudo grep -A 3 -B 2 '{}' /etc/NetworkManager/system-connections/* | grep psk=".format(bssid)
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    password = re.search(r'psk=(\S+)', output)
    if password:
        return password.group(1)
    else:
        return None

bssid = "BSSID"  # BSSID'yi buraya yapıştırın
password = get_wifi_password(bssid)
if password:
    print("Wi-Fi şifresi: {}".format(password))
else:
    print("Şifre bulunamadı.")
