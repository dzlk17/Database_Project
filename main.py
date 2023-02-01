import PySimpleGUI as sg
import psycopg2
import os
from dotenv import load_dotenv
import user
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DBHOST"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
    dbname=os.getenv("DBNAME")
)
cursor = conn.cursor()

# Wyszukaj droge - po wycenie, po rejonie
#wyszukaj kluby
#dodaj klub - user
# wyszukaj kluby
# wyszukaj uczestnika - dodaj klub i login
# sekcje spróbuj dodać

data = []
headings = []
layout = [
    [sg.Text("Baza danych ", font=("Helvetica", 25), text_color='black')],
    [sg.Button("Wyświetl członków"), sg.Button("Wyświetl drogi"), sg.Button("Wyświetl rejony"), sg.Button("Ranking")],
    [sg.Button("Logowanie"), sg.Button("Rejestracja")]]

window = sg.Window("Baza danych", layout)
event, values = window.read()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Wyświetl członków':
        heading = ['Login', 'Imię', 'Nazwisko']
        cursor.execute("SELECT login, imie, nazwisko FROM topo.uzytkownik")
        for row in cursor:
            data.append([row[0], row[1], row[2]])
        user.create_users_list(data, heading)
    elif event == 'Ranking':
        user.create_rank_window()
    elif event == 'Wyświetl drogi':
        user.show_routes()
    elif event == 'Wyświetl rejony':
        user.show_areas()
    elif event == 'Rejestracja':
        user.create_reg_window()
    elif event == 'Logowanie':
        logged_user = user.create_log_window()
        if logged_user is not None:
            if logged_user[1] == 'ADMIN':
                user.admin_window(logged_user)
            else:
                user.user_window(logged_user)


