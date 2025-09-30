import getpass
import os
import time
import base64
import hashlib
from cryptography.fernet import Fernet
from colorama import Fore , Style, init

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

key = getpass.getpass("Insert your key: ")
sha_hash = hashlib.sha256(key.encode()).digest()
fnet_key = base64.urlsafe_b64encode(sha_hash)
cipher = Fernet(fnet_key)

clear()

init(autoreset=True)
logo=(Fore.BLUE+"""
  d8b
 88P
d88
888  ?88,.d88b,  88bd8b,d88b
?88  `?88'  ?88  88P'`?8P'?8b
 88b   88b  d8P d88  d88  88P
  88b  888888P'd88' d88'  88b
       88P'
      d88
      ?8
""")

clear()
time.sleep(0.5)
for i in range(3):
    print(".",end="")
    time.sleep(.7)
print("Success!")
time.sleep(1)
clear()

while True:
    print(logo)
    print(Fore.CYAN+Style.BRIGHT+"What would you like to do?")
    print("1. Add password manually")
    print("2. Check current passwords")
    print("3. Delete password")
    print("4. Export passwords in .txt")
    print("5. Exit")

    try:
        ans = int(input(""))
    except:
        continue

    if ans == 1:
        host = input("What website or application do you want to save a password for?\n")
        name = input("What is your username (or email)?\n")
        pwd = getpass.getpass("What is your password?\n")
        dec = name+":"+pwd
        enc = cipher.encrypt(dec.encode()).decode()
        with open("pass.enc", "a") as f:
            f.write(f"{host}:{enc}\n")
        input(Fore.GREEN+"Successfully added new login!")
        clear()

    elif ans == 2:
        if not os.path.exists("pass.enc"):
            input("No passwords saved.")
            clear()
            continue
        with open("pass.enc", "r") as f:
            for line in f:
                try:
                    host, enc = line.strip().split(":", 1)
                    dec = cipher.decrypt(enc.encode()).decode()
                    print(host + ":" + dec)
                except:
                    print(host + ": ???")
        input("")
        clear()

    elif ans == 3:
        if not os.path.exists("pass.enc"):
            input("No passwords to delete.")
            clear()
            continue
        lines = open("pass.enc", "r").readlines()
        for i, line in enumerate(lines, 1):
            host, enc = line.strip().split(":", 1)
            try:
                dec = cipher.decrypt(enc.encode()).decode()
                print(f"{i}. {host}: {dec}")
            except:
                print(f"{i}. {host}: ???")
        try:
            idx = int(input("Select number to delete: ")) - 1
            if 0 <= idx < len(lines):
                del lines[idx]
                with open("pass.enc", "w") as f:
                    f.writelines(lines)
                input("Deleted.")
            else:
                input("Invalid choice.")
        except:
            input("Invalid input.")
        clear()

    elif ans == 4:
        if not os.path.exists("pass.enc"):
            input("Nothing to export.")
            clear()
            continue
        with open("pass.enc", "r") as f:
            lines = f.readlines()
        with open("export.txt", "w") as f:
            for line in lines:
                host, enc = line.strip().split(":", 1)
                try:
                    dec = cipher.decrypt(enc.encode()).decode()
                    f.write(f"{host}:{dec}\n")
                except:
                    f.write(f"{host}:???\n")
        input("Exported to export.txt")
        clear()

    elif ans == 5:
        print("Goodbye!")
        time.sleep(1)
        clear()
        break
