import smtplib
import time
print('''
      __        __           __  ___     _ __       
 ___ / /__ ____/ /________  /  |/  /__ _(_) /__ ____
/ -_) / -_) __/ __/ __/ _ \/ /|_/ / _ `/ / / -_) __/ ver2.0
\__/_/\__/\__/\__/_/  \___/_/  /_/\_,_/_/_/\__/_/   
                                                    
github.com/emiralper
''')

# Dictionary to map email domains to SMTP servers
smtp_servers = {
    "gmail.com": ("smtp.gmail.com", 465, "ssl"),
    "yahoo.com": ("smtp.mail.yahoo.com", 587, "tls"),
    "oguzkaan.k12.tr": ("smtp.gmail.com", 465, "ssl"),
    "outlook.com": ("smtp.office365.com", 587, "tls")
    # Ek SMTP sunucularını ve bilgilerini buraya ekleyin
}

def select_smtp_server(sender_email):
    # Kullanıcının girdiği e-posta adresini kullanarak SMTP sunucusunu seçin
    domain = sender_email.split('@')[-1]
    if domain in smtp_servers:
        return smtp_servers[domain]
    else:
        print(f"{domain} için SMTP sunucusu bulunamadı.")
        return None

def send_email(sender_email, sender_password, receiver_email, subject, message, smtp_server_info):
    if smtp_server_info is None:
        return

    smtp_server, smtp_port, encryption = smtp_server_info
    msg = f"Subject: {subject}\n\n{message}"

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        if encryption.lower() == 'tls':
            smtp.starttls()
        elif encryption.lower() == 'ssl':
            smtp.ehlo()
            smtp.starttls()

        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, msg)

# Kullanıcıdan giriş alın
try:
    with open("credentials.txt", "r") as credentials_file:
        lines = credentials_file.readlines()
        if len(lines) >= 2:
            sender_email = lines[0].strip()
            sender_password = lines[1].strip()
        else:
            raise Exception("Dosya eksik bilgi içeriyor.")
except FileNotFoundError:
    print("credentials.txt dosyası bulunamadı.")
    exit(1)
except Exception as e:
    print(f"Dosya okuma hatası: {str(e)}")
    exit(1)

receiver_email = input("Alıcı e-posta adresi: ")
subject = input("E-posta konusu: ")
message = input("E-posta mesajı: ")

# SMTP sunucusunu seç
smtp_server_info = select_smtp_server(sender_email)

# E-postayı gönder
if smtp_server_info:
    while True:
        send_email(sender_email, sender_password, receiver_email, subject, message, smtp_server_info)
        print("E-posta gönderildi.")
        time.sleep(1)  # Her bir saniyede bir e-posta gönder
else:
    print("E-posta gönderimi başarısız. SMTP sunucusu seçilemedi.")


