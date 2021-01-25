import keyboard
import sqlite3
import win32clipboard
from time import sleep

con = sqlite3.connect("copy.db")
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS copy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INT UNIQUE,
                text STR
               )""")

counts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
while True:
    for count in counts:
        if keyboard.is_pressed(f'ctrl+shift+C+{count}'):
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            print(data)
            try:
                cursor.execute("INSERT INTO copy(number, text) VALUES(?, ?)", (int(count), str(data)))
                con.commit()
            except sqlite3.IntegrityError:
                cursor.execute("UPDATE copy SET text = ? WHERE number = ? ", (str(data), int(count)))
                con.commit()
            win32clipboard.CloseClipboard()
            sleep(0.5)
        elif keyboard.is_pressed(f'ctrl+shift+V+{count}'):
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            cursor.execute(f"SELECT text FROM copy WHERE number = {count}")
            fetch = cursor.fetchone()
            win32clipboard.SetClipboardText(fetch[0])
            win32clipboard.CloseClipboard()
            print(fetch)
            sleep(0.5)

