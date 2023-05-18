import socket

target_host = input("Hedef IP adresini girin: ")
target_ports = [80, 443, 22, 3389]  # Taramak istediğiniz portlar

for port in target_ports:
    # Yeni bir soket oluştur
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Hedefe bağlanmayı dene
        client.connect((target_host, port))
        print(f"Port {port} açık")
    except ConnectionRefusedError:
        print(f"Port {port} kapalı")
    finally:
        # Soketi kapat
        client.close()
