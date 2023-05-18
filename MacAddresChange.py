import subprocess

def change_mac_address(interface, new_mac_address):
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac_address])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])

# Örnek kullanım
interface = 'wlan0'
new_mac_address = '00:11:22:33:44:55'
change_mac_address(interface, new_mac_address)