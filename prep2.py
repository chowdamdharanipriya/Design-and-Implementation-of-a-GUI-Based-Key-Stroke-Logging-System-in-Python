import tkinter as tk
from pynput import keyboard
import json
from datetime import datetime

root = tk.Tk()
root.geometry("360x300")
root.title("Educational Key Logger")
root.configure(bg="black")

key_list = []
listener = None
logging_active = False

status = tk.StringVar()
status.set("Status : Stopped")

def update_txt_file(text):
    with open("logs.txt", "a") as f:
        f.write(text)

def update_json_file():
    with open("logs.json", "w") as f:
        json.dump(key_list, f, indent=4)

def on_press(key):
    if logging_active:
        timestamp = datetime.now().strftime("%H:%M:%S")
        key_list.append({"Time": timestamp, "Pressed": str(key)})
        update_json_file()

def on_release(key):
    if logging_active:
        timestamp = datetime.now().strftime("%H:%M:%S")
        key_list.append({"Time": timestamp, "Released": str(key)})
        update_json_file()

        if hasattr(key, 'char'):
            update_txt_file(key.char)
        else:
            update_txt_file(f"[{key}]")

def start_logger():
    global listener, logging_active
    if not logging_active:
        logging_active = True
        status.set("Status : Running")
        update_txt_file("\n--- New Session Started ---\n")
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

def stop_logger():
    global listener, logging_active
    if listener:
        logging_active = False
        status.set("Status : Stopped")
        listener.stop()

def clear_logs():
    global key_list
    key_list = []
    open("logs.txt", "w").close()
    open("logs.json", "w").close()
    status.set("Status : Logs Cleared")

tk.Label(root, text="Key Logger", font="Verdana 12 bold", bg="black").pack(pady=15)
tk.Label(root, textvariable=status, bg="pink", fg="blue").pack(pady=5)

tk.Button(root, text="Start Logging", width=20, command=start_logger).pack(pady=5)
tk.Button(root, text="Stop Logging", width=20, command=stop_logger).pack(pady=5)
tk.Button(root, text="Clear Logs", width=20, command=clear_logs).pack(pady=5)

root.mainloop()
