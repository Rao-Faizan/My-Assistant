import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# ========== SYSTEM COMMAND TABLE ==========
cursor.execute('''CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    path VARCHAR(1000)
)''')

# Insert example: Visual Studio Code (check path on your system)
cursor.execute('''INSERT OR IGNORE INTO sys_command (name, path)
                  VALUES ('Visual Studio Code', 'D:\apps installs\Downloads\VSCodeUserSetup-x64-1.98.2.exe')''')

cursor.execute('''INSERT OR IGNORE INTO sys_command (name, path)
                  VALUES ('Notepad', 'C:\Windows\notepad.exe')''')

# ========== WEB COMMAND TABLE ==========
cursor.execute('''CREATE TABLE IF NOT EXISTS web_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    url VARCHAR(1000)
)''')

# Insert popular web/social platforms
web_commands = [
    ('Twitter', 'https://twitter.com/'),
    ('Instagram', 'https://www.instagram.com/'),
    ('Facebook', 'https://www.facebook.com/'),
    ('ChatGPT', 'https://chat.openai.com/'),
    ('Grok', 'https://grok.com/'),
    ('Google Docs', 'https://docs.google.com/document/u/0/'),
    ('Google Sheets', 'https://docs.google.com/spreadsheets/u/0/'),
    ('Google Slides', 'https://docs.google.com/presentation/u/0/'),
    ('Canva', 'https://www.canva.com/'),
    ('WhatsApp Web', 'https://web.whatsapp.com/'),
    ('Youtube', 'https://www.youtube.com/')

]

for name, url in web_commands:
    cursor.execute("INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)", (name, url))

# === CONTACT TABLE (Commented for now) ===
#'''
#  cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name VARCHAR(100),
#     mobile_no VARCHAR(255),
#     email VARCHAR(255) NULL
# )''')

# # Later insert logic for CSV etc.
# '''

con.commit()
# con.close()
print("[✔] Database setup completed successfully.")
