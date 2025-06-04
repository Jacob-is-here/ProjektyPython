import tkinter as tk
from game import ModeSelection
import hashlib
import sqlite3

class LoginScreen:
    def __init__(self, root):
        """
        Inicjalizuje ekran logowania.

        Tworzy interfejs użytkownika dla logowania, logowania jako gość oraz tworzenia konta.
        Ustawia tytuł okna, jego rozmiar oraz elementy takie jak pola tekstowe, przyciski i etykiety.

        :param root: Główne okno aplikacji
        """
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        tk.Label(root, text="Login", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(root, text="Username:", font=("Helvetica", 14)).pack()
        self.username_entry = tk.Entry(root, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:", font=("Helvetica", 14)).pack()
        self.password_entry = tk.Entry(root, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=5)

        self.message_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red")
        self.message_label.pack(pady=5)

        tk.Button(root, text="Login", font=("Helvetica", 14), command=self.login).pack(pady=10)
        tk.Button(root, text="Login as Guest", font=("Helvetica", 14), command=self.login_as_guest).pack(pady=5)
        tk.Button(root, text="Create Account", font=("Helvetica", 14), command=self.create_account).pack(pady=5)

    def login(self):
        """
        Funkcja ta przyjmuje jako paramtery nazwe uzytkownika i haslo
        \nŁączy sie z baza danych przekonwertywowuje hasło na kodowanie sha1 i sprawdza czy dany uzytkownik istniej badz wpisał poprawne haslo

        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.config(text="Username and password cannot be empty.")
            return

        hashed_password = hashlib.sha1(password.encode()).hexdigest()

        try:
            con = sqlite3.connect('../moja_baza.db')
            cur = con.cursor()

            cur.execute("SELECT COUNT(*) FROM user WHERE login = ? AND haslo = ?", (username, hashed_password))
            if cur.fetchone()[0] > 0:
                self.message_label.config(text="Login successful!", fg="green")
                self.start_mode_selection()
            else:
                self.message_label.config(text="Invalid username or password.")

            con.close()
        except sqlite3.Error as e:
            self.message_label.config(text=f"Database error: {e}")

    def login_as_guest(self):
        """
        Ta metoda umożliwia zagranie w gre bez logowania sie do bazy
        """
        self.start_mode_selection()



    def create_account(self):
        """
        Funkcja ta przyjmuje jako paramtery nazwe uzytkownika i haslo
        \nŁączy sie z baza danych przekonwertywowuje hasło na kodowanie sha1 i dodaje użytkownika do bazy , chyba że użytkownik istniej to wtedy zwraca błąd

        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.config(text="Username and password cannot be empty.")
            return

        hashed_password = hashlib.sha1(password.encode()).hexdigest()

        try:
            con = sqlite3.connect('../moja_baza.db')
            cur = con.cursor()

            cur.execute("SELECT COUNT(*) FROM user WHERE login = ?", (username,))
            if cur.fetchone()[0] > 0:
                self.message_label.config(text="Username already exists.")
                return

            query = f"INSERT INTO user (login, haslo, score) VALUES ('{username}', '{hashed_password}', 0)"
            cur.execute(query)
            con.commit()

            self.message_label.config(text="Account created successfully!", fg="green")
        except sqlite3.IntegrityError:
            print(f"User {username} already exists.")
    def start_mode_selection(self):
        """
        Ta metoda usuwa wszystkie widżety z obecnego okna aplikacji (czyści interfejs użytkownika) i inicjalizuje klasę ModeSelection.
        \nW efekcie użytkownik zostaje przeniesiony do ekranu wyboru trybu gry.
        """

        for widget in self.root.winfo_children():
            widget.destroy()
        ModeSelection(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()