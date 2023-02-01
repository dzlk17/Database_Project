import PySimpleGUI as sg
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DBHOST"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
    dbname=os.getenv("DBNAME")
)
cursor = conn.cursor()


def save_user(login, name, lname, password):
    sql_ins = "INSERT INTO topo.uzytkownik (login, imie, nazwisko, haslo) VALUES(%s, %s, %s, %s)"
    val = (login, name, lname, password)
    cursor.execute(sql_ins, val)
    conn.commit()


def log_user(login, password):
    cursor.execute("SELECT login, id, haslo FROM topo.uzytkownik")
    for row in cursor:
        print(row[0], row[2])
        if row[0] == login and row[2] == password:
            logged_user = [row[1], row[0]]
            # return
            return logged_user
    raise Exception("invalid data")


def create_users_list(user_list, headings):
    user_list_window_layout = [
        [sg.Table(values=user_list, headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=True,
                  justification='right',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  tooltip='Reservations Table')]
    ]
    user_list_window = sg.Window("Lista użytkowników",
                                 user_list_window_layout, modal=True)
    while True:
        event, values = user_list_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    user_list_window.close()


def create_rank_window():
    cursor.execute("SELECT * FROM topo.ranking()")
    list = []
    for row in cursor:
        list.append(row)
    rank_layout = [[sg.Text("Ranking 5 użytkowników o największej ilości przejść:")],
                   [sg.Table(values=list, headings=['Miejsce', 'Login', 'Imię', 'Nazwisko', 'ilość przejść'])]
                   ]
    rank_window = sg.Window("Ranking", rank_layout, modal=True)
    while True:
        event, values = rank_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    rank_window.close()


def show_routes():
    print("poka")
    cursor.execute("select * from topo.droga_list(%s)", (1,))
    pop_list = []
    for row in cursor:
        pop_list.append(row)
    cursor.execute("select * from topo.droga_list(%s)", (2,))
    ar_list = []
    for row in cursor:
        ar_list.append(row)
    cursor.execute("select * from topo.droga_list(%s)", (3,))
    df_list = []
    for row in cursor:
        df_list.append(row)
    head = ["Miejsce", "Droga", "Rejon", "Wycena", "Ilość przejść"]
    pop_layout = [[sg.Table(values=pop_list, headings=head)]]
    ar_layout = [[sg.Table(values=ar_list, headings=head)]]
    df_layout = [[sg.Table(values=df_list, headings=head)]]
    routes_layout = [[sg.Text("Lista dróg:")],
                     [sg.TabGroup([[sg.Tab('Najpopularniejsze', pop_layout)],
                                   [sg.Tab('Według rejonu', ar_layout)],
                                   [sg.Tab('Według trudności', df_layout)]])]
                     ]
    routes_window = sg.Window("Lista dróg", routes_layout, modal=True)

    while True:
        event, values = routes_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    routes_window.close()


def show_areas():
    cursor.execute("SELECT * FROM topo.area_list()")
    areas_list = []
    for row in cursor:
        areas_list.append(row)
    area_list_window_layout = [[sg.Table(values=areas_list, headings=['Rejon', 'Opis', 'Ilość dróg'])]]
    area_list_window = sg.Window("Lista użytkowników",
                                 area_list_window_layout, modal=True)
    while True:
        event, values = area_list_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    area_list_window.close()


def create_reg_window():
    reg_layout = [[sg.Text("Rejestracja:")],
                  [sg.T("Login:"), sg.I(key="LOGIN")],
                  [sg.T("Imie:"), sg.I(key="NAME")],
                  [sg.T("Nazwisko:"), sg.I(key="LNAME")],
                  [sg.T("Haslo:"), sg.I(key="PASS")],
                  [sg.Button("Potwierdź")]
                  ]
    reg_window = sg.Window("Rejestracja użytkownika",
                           reg_layout, modal=True)
    while True:
        event, values = reg_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Potwierdź':
            login = values['LOGIN']
            name = values['NAME']
            lname = values['LNAME']
            password = values['PASS']
            if login == '' or name == '' or lname == '' or password == '':
                sg.PopupError("Brakujące pole", 'Uzupełnij wszystkie pola')
            else:
                try:
                    save_user(login, name, lname, password)
                    summary_list = 'Użytkownik został dodany do bazy. Przejdź do logowania'
                    sg.PopupOKCancel(summary_list)
                    break
                except:
                    sg.Popup('Użytkownik o tym loginie jest już w bazie, lub imie/nazwisko zawiera cyfry.')
    reg_window.close()


def create_log_window():
    log_layout = [[sg.Text("Logowanie:")],
                  [sg.T("Login:"), sg.I(key="LOGIN")],
                  [sg.T("Haslo:"), sg.I(key="PASS")],
                  [sg.Button("Potwierdź")]
                  ]
    log_window = sg.Window("Logowanie",
                           log_layout, modal=True)
    logged_user = None
    while True:
        event, values = log_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Potwierdź':
            login = values['LOGIN']
            password = values['PASS']
            if login == '' or password == '':
                sg.PopupError("Brakujące pole", 'Uzupełnij wszystkie pola')
            else:
                try:
                    logged_user = log_user(login, password)
                    summary_list = 'Użytkownik zalogowany. Oto twój panel użytkownika'
                    sg.PopupOKCancel(summary_list)
                    break
                except:
                    sg.Popup('Błędny login lub hasło')
                    logged_user = None
    log_window.close()
    return logged_user


def user_window(logged_user):
    cursor.execute("select * from topo.lista_droga_rejon()")
    routes_list = []
    id_routes_list = []
    for row in cursor:
        routes_list.append(row[1] + ", " + row[2])
        id_routes_list.append(row[0])
    res = []
    cursor.execute("SELECT * FROM topo.lista_przejsc(%s)", (logged_user[0],))
    for row in cursor:
        res.append([row[0], row[1]])
    club_list = []
    cursor.execute("SELECT nazwa FROM topo.klub")
    for row in cursor:
        club_list.append(row[0])
    add_asc_layout = [[sg.Combo(routes_list, key="SENT")],
                      [sg.Button("Dodaj")]]
    ascends_layout = [[sg.Table(values=res, headings=["Droga", "Rejon"])]]
    club_layout = [[sg.Combo(club_list, key="CLUB")],
                   [sg.Button("Dołącz")]]
    user_layout = [
        [sg.Text("Panel użytkownika: " + logged_user[1] + "  "), sg.Button("Wyloguj"), sg.Button("Usuń użytkownika")],
        [sg.TabGroup([[sg.Tab('Dodaj przejście', add_asc_layout),
                       sg.Tab('Lista przejść', ascends_layout, key="ASC_RES"),
                       sg.Tab('Zmień klub', club_layout),
                       ]], tab_location='left')]]
    log_window = sg.Window("Panel użytkownika",
                           user_layout, modal=True, size=(500, 400), default_element_size=(12, 1))
    while True:
        event, values = log_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED or event == "Wyloguj":
            break
        elif event == "Dodaj":
            try:
                clicked = log_window["SENT"].get()
                id = id_routes_list[routes_list.index(clicked)]
                cursor.execute("SELECT topo.dodaj_przejscie(%s, %s)", (logged_user[0], id))
                conn.commit()
                log_window.close()
                user_window(logged_user)
                sg.PopupOK("Dodano przejście.")
            except:
                sg.Popup('Zaznacz pole.')
        elif event == "Usuń użytkownika":
            ch = sg.popup_yes_no("Czy na pewno chcesz usunąć?", title="Potwierdź decyzję")
            if ch == "Yes":
                try:
                    cursor.execute("DELETE FROM topo.uzytkownik WHERE %s = topo.uzytkownik.id", (logged_user[0]))
                    conn.commit()
                    sg.PopupOK("Usunięto użytkownika.")
                    log_window.close()
                except:
                    sg.Popup('Zaznacz pole.')
            else:
                sg.PopupOK("Użytkownik nie został usunięty")
        elif event == "Dołącz":
            try:
                clicked = log_window["CLUB"].get()
                print(clicked)
                print(logged_user[0])
                cursor.execute("SELECT topo.zmien_klub(%s, %s)", (clicked, logged_user[0]))
                conn.commit()
                log_window.close()
                user_window(logged_user)
                sg.PopupOK("Zmieniono klub.")
            except:
                sg.Popup('Zaznacz pole.')
    log_window.close()


def admin_window(logged_user):
    cursor.execute("SELECT * FROM topo.rejon")
    area_list = []
    for row in cursor:
        area_list.append(row[1] + ", " + row[2])
    cursor.execute("select * from topo.lista_droga_rejon()")
    routes_list = []
    for row in cursor:
        routes_list.append(row[1] + ', ' + row[2])
    cursor.execute("SELECT login, imie, nazwisko FROM topo.uzytkownik")
    user_list = []
    for row in cursor:
        user_list.append(row[0] + ', ' + row[1] + " " + row[2])
    cursor.execute("SELECT * FROM topo.klub")
    club_list = []
    for row in cursor:
        club_list.append(row[1])
    add_route_layout = [[sg.Text("Dodaj drogę: ")],
                        [sg.T("Nazwa:"), sg.I(key="NAME")],
                        [sg.T("Wycena:"), sg.I(key="RATE")],
                        [sg.Combo(area_list, key="AREA")],
                        [sg.Button("Dodaj drogę")]
                        ]
    del_route_layout = [[sg.Text("Usuń drogę: ")],
                        [sg.Combo(routes_list, key="ROUTE")],
                        [sg.Button("Usuń drogę")]
                        ]
    add_area_layout = [[sg.Text("Dodaj rejon: ")],
                       [sg.T("Nazwa:"), sg.I(key="NAME")],
                       [sg.T("Opis:"), sg.I(key="DESC")],
                       [sg.Button("Dodaj rejon")]
                       ]
    del_area_layout = [[sg.Text("Usuń rejon: ")],
                       [sg.Combo(area_list, key="AREA")],
                       [sg.Button("Usuń rejon")]
                       ]
    del_user_layout = [[sg.Text("Usuń użytkownika: ")],
                       [sg.Combo(user_list, key="USER")],
                       [sg.Button("Usuń użytkownika")]
                       ]
    add_club_layout = [[sg.Text("Dodaj klub: ")],
                       [sg.T("Nazwa:"), sg.I(key="CLUB")],
                       [sg.Button("Dodaj klub")]
                       ]
    del_club_layout = [[sg.Text("Usuń klub: ")],
                       [sg.Combo(club_list, key="AREA")],
                       [sg.Button("Usuń klub")]
                       ]
    user_layout = [[sg.Text("Panel użytkownika: " + logged_user[1] + "  "), sg.Button("Wyloguj")],
                   [sg.TabGroup([[sg.Tab('Dodaj drogę', add_route_layout),
                                  sg.Tab('Usuń drogę', del_route_layout),
                                  sg.Tab('Dodaj rejon', add_area_layout),
                                  sg.Tab('Usuń rejon', del_area_layout),
                                  sg.Tab('Usuń użytkownika', del_user_layout),
                                  sg.Tab('Dodaj klub', add_club_layout),
                                  sg.Tab('Usuń klub', del_club_layout),
                                  ]], tab_location='left')]]
    log_window = sg.Window("Panel użytkownika",
                           user_layout, modal=True, size=(500, 400), default_element_size=(12, 1))
    while True:
        event, values = log_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED or event == "Wyloguj":
            break
        elif event == "Dodaj drogę":
            name = values['NAME']
            rate = values['RATE']
            if name == '' or rate == '':
                sg.PopupError("Brakujące pole", 'Uzupełnij wszystkie pola')
            try:
                clicked = log_window["AREA"].get()
                cursor.execute("SELECT topo.dodaj_droge(%s, %s, %s)", (name, rate, clicked.split(',')[0]))
                conn.commit()
                sg.PopupOK("Dodano drogę")
            except:
                sg.PopupError("Zaznacz pole")
        elif event == "Usuń drogę":
            try:
                clicked = log_window["ROUTE"].get()
                cursor.execute("DELETE FROM topo.droga WHERE %s = topo.droga.nazwa", (clicked.split(',')[0],))
                conn.commit()
                sg.PopupOK("Usunięto drogę")
            except:
                sg.PopupError("Zaznacz pole")
        elif event == "Dodaj rejon":
            name = values['NAME']
            desc = values['DESC']
            if name == '' or desc == '':
                sg.PopupError("Brakujące pole", 'Uzupełnij wszystkie pola')
            try:
                cursor.execute("INSERT INTO topo.rejon (nazwa, opis) VALUES (%s, %s)", (name, desc))
                conn.commit()
                sg.PopupOK("Dodano rejon")
            except:
                sg.PopupError("Błąd. Spróbuj ponownie")
        elif event == "Usuń rejon":
            try:
                clicked = log_window["AREA"].get()
                cursor.execute("DELETE FROM topo.rejon WHERE %s = topo.rejon.nazwa", (clicked.split(',')[0],))
                conn.commit()
                sg.PopupOK("Usunięto rejon")
            except:
                sg.PopupError("Zaznacz pole")
        elif event == "Usuń użytkownika":
            try:
                clicked = log_window["USER"].get()
                cursor.execute("DELETE FROM topo.uzytkownik WHERE %s = topo.uzytkownik.login", (clicked.split(',')[0],))
                conn.commit()
                sg.PopupOK("Użytkownik usunięty")
            except:
                sg.PopupError("Wybierz użytkownika")
        elif event == "Dodaj klub":
            club = values['CLUB']
            if club == '':
                sg.PopupError("Brakujące pole", 'Uzupełnij wszystkie pola')
            try:
                cursor.execute("INSERT INTO topo.klub (nazwa) VALUES (%s)", (club,))
                conn.commit()
                sg.PopupOK("Dodano klub")
            except:
                sg.PopupError("Błąd. Spróbuj ponownie")
        elif event == "Usuń klub":
            try:
                clicked = log_window["CLUB"].get()
                cursor.execute("DELETE FROM topo.klub WHERE %s = topo.klub.nazwa", (clicked,))
                conn.commit()
                sg.PopupOK("Usunięto klub")
            except:
                sg.PopupError("Zaznacz pole")

    log_window.close()
