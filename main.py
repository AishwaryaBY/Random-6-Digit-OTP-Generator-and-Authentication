# InstaPass OTP Generator (Python Programming - Mini Project)

"""
Team Members:
1. Boya Sanjay Kumar - 25BTRPW025
2. Aniketh Chavare - 25BTRPM014
3. Kartikeya Pradhan - 25BTRPW053
4. Aishwarya BY - 25BTRPW007
5. Danaj Raj - 25BTRPM029
6. D Kiran - 25BTRPM027

Unique Features:
1. Keystroke Dynamics (Behavioral Biometrics)
2. Multi-Factor "Master PIN + OTP" Combination
3. Self-Destructing/Limited-View OTP
4. Send the OTP via email.
"""

# Imports
import os
import hmac
import time
import secrets
import getpass
import hashlib
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

# Loading .env Variables
load_dotenv()

# Variables
master_pin = ""

# Helper Functions
hash_pin = lambda pin: hashlib.sha3_256(pin.encode("utf-8")).hexdigest()

# Main Application
print("==================================================")
print("   WELCOME TO INSTAPASS OTP GENERATOR")
print("==================================================")

while True:
    print("\n==========\n MAIN MENU\n==========")
    print("1. Set Master PIN")
    print("2. Generate OTP via Terminal")
    print("3. Generate OTP via Email")
    print("4. Exit")

    choice = input("\nEnter Your Choice: ").strip()

    if choice == '1':
        master_pin_input = getpass.getpass(prompt="\nEnter Master PIN: ", echo_char="*")

        if master_pin_input.isdigit() and len(master_pin_input) == 4:
            master_pin = hash_pin(master_pin_input)
            print("✔ The master PIN has been set!")
        else:
            print("✖ The master PIN must be exactly 4 numbers!")

    elif choice in ("2", "3"):
        if not master_pin:
            print("✖ Please set a Master PIN first!")
            continue

        otp = f"{secrets.randbelow(1_000_000):06d}"

        if choice == '2':
            print(f"\nGenerated OTP: {otp}", end="", flush=True)
            time.sleep(5)
            print("\rGenerated OTP: ******")
        else:
            email_id = input("\nEnter Your Email ID: ").strip()

            message = EmailMessage()
            message["From"] = "instapass.otp.generator@gmail.com"
            message["To"] = email_id
            message["Subject"] = "Your InstaPass OTP"
            message.set_content(f"Your OTP is {otp}. Please enter this to log in.")

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login("instapass.otp.generator@gmail.com", os.getenv("APP_PASSWORD"))
                    server.send_message(message)
            except Exception as e:
                print(f"✖ Failed to send email: {e}")
                continue

        attempts = 0

        while attempts < 3:
            start_time = time.time()
            code = input("Enter the Code (Master PIN + OTP): ").strip()
            time_taken = time.time() - start_time

            if time_taken < 1.0:
                print("✖ Code entered too fast! Automated input detected.")
                break
            elif time_taken > 20.0:
                print("✖ Input timed out! Took too long to enter.")
                break

            if not code.isdigit() or len(code) != 10:
                print("✖ The code must be exactly 10 numbers!\n")
                attempts += 1
            elif not hmac.compare_digest(hash_pin(code[:4]), master_pin):
                print("✖ The master PIN is incorrect!\n")
                attempts += 1
            elif not hmac.compare_digest(otp, code[4:]):
                print("✖ The OTP is incorrect!\n")
                attempts += 1
            else:
                print("✔ You are successfully logged in!")
                break
        else:
            print("✖ Maximum login attempts exceeded (3 attempts)")

    elif choice == '4':
        break
    else:
        print("✖ You have entered an invalid choice!")
