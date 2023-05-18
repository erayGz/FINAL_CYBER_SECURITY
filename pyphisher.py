import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Giden e-posta bilgileri
sender_email = "eraygz5858@gmail.com"
sender_password = "asdasfasamazqwqwezyras123"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Hedef e-posta bilgileri
target_email = "eray58gurbuz@gmail.com"

# E-posta içeriği
subject = "Önemli: Hesap Güncellemesi"
body = "Siber Güvenlik Testi"

def send_email():
    try:
        # E-posta mesajını oluştur
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = target_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # SMTP sunucusuna bağlan
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # E-postayı gönder
        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()

        print("Phishing e-postası gönderildi!")
    except Exception as e:
        print("Hata oluştu:", str(e))

# E-posta gönderme işlemini gerçekleştir
send_email()
