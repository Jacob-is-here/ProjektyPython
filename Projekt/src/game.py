import tkinter as tk
import random

class Wisielec:
    def __init__(self, root, mode):
        """
        :param root: Główne okno aplikacji (instancja tkinter.Tk).\n
        :param mode: Tryb gry, który określa poziom trudności (np. "easy" lub "hard").
        """
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        with open("../words_database.txt", "r") as file:
            all_words = [line.strip() for line in file.readlines()]
        if mode == "easy":
            self.words = [word for word in all_words if len(word) <= 5]
        elif mode == "hard":
            self.words = [word for word in all_words if len(word) >= 6]

        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts = 9

        self.word_label = tk.Label(root, text=self.get_word(), font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.info_label = tk.Label(root, text=f"Attempts left: {self.attempts}", font=("Helvetica", 14))
        self.info_label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Helvetica", 18))
        self.entry.pack(pady=10)

        self.guess_button = tk.Button(root, text="Guess", command=self.make_guess, font=("Helvetica", 14))
        self.guess_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.result_label.pack(pady=20)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(pady=20)
        self.draw_hangman(0)

    def get_word(self):
        """
            Generuje aktualny stan zgadywanego słowa, gdzie odgadnięte litery są widoczne,
            a nieodgadnięte litery są reprezentowane jako podkreślenia.

            :return: Łańcuch znaków reprezentujący słowo z odgadniętymi literami i podkreśleniami.
        """

        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def draw_hangman(self, stage):
        self.canvas.delete("all")
        """
            Rysuje elementy wisielca na podstawie aktualnego etapu gry.
            
            :param stage: Etap gry, który określa, ile elementów wisielca należy narysować.
        """

        if stage > 0:
            self.canvas.create_line(50, 350, 150, 350, width=3)
        if stage > 1:
            self.canvas.create_line(100, 350, 100, 50, width=3)
        if stage > 2:
            self.canvas.create_line(100, 50, 200, 50, width=3)
        if stage > 3:
            self.canvas.create_line(200, 50, 200, 100, width=3)
        if stage > 4:
            self.canvas.create_oval(175, 100, 225, 150, width=3)
        if stage > 5:
            self.canvas.create_line(200, 150, 200, 250, width=3)
        if stage > 6:
            self.canvas.create_line(200, 180, 170, 220, width=3)
        if stage > 7:
            self.canvas.create_line(200, 180, 230, 220, width=3)
        if stage > 8:
            self.canvas.create_line(200, 250, 170, 300, width=3)
        if stage > 9:
            self.canvas.create_line(200, 250, 230, 300, width=3)

    def make_guess(self):
        """
        Metoda ta obsługuje logikę zgadywania liter w grze Wisielec.

        - Pobiera literę od użytkownika z pola tekstowego.
        - Sprawdza, czy wpisana litera jest pojedynczym znakiem alfabetu.
        - Sprawdza, czy litera została już wcześniej odgadnięta.
        - Dodaje literę do zbioru odgadniętych liter.
        - Aktualizuje stan gry w zależności od tego, czy litera znajduje się w zgadywanym słowie:
          - Jeśli litera jest poprawna, wyświetla odpowiedni komunikat.
          - Jeśli litera jest błędna, zmniejsza liczbę pozostałych prób i rysuje kolejny element wisielca.
        - Aktualizuje wyświetlane słowo oraz liczbę pozostałych prób.
        - Sprawdza, czy gra została wygrana lub przegrana, i odpowiednio blokuje przycisk zgadywania.

        """
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.result_label.config(text="Please enter a single valid letter.")
            return

        if guess in self.guessed_letters:
            self.result_label.config(text="You already guessed that letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            self.result_label.config(text="Correct!")
        else:
            self.attempts -= 1
            self.result_label.config(text=f"Wrong! {self.attempts} attempts left.")
            self.draw_hangman(10 - self.attempts)

        self.word_label.config(text=self.get_word())
        self.info_label.config(text=f"Attempts left: {self.attempts}")

        if "_" not in self.get_word():
            self.result_label.config(text="Congratulations! You guessed the word!")
            self.guess_button.config(state=tk.DISABLED)

        if self.attempts == 0:
            self.result_label.config(text=f"Game over! The word was: {self.word}")
            self.guess_button.config(state=tk.DISABLED)

class ModeSelection:
    def __init__(self, root):
        """
        Główne okno aplikacji, w którym wyświetlany jest interfejs wyboru trybu gry.
        :param root:
        """
        self.root = root
        self.root.title("Select Game Mode")
        self.root.geometry("500x500")
        self.root.resizable(True, True)

        tk.Label(root, text="Select Game Mode", font=("Helvetica", 18)).pack(pady=20)

        tk.Button(root, text="Easy (Up to 5 letters)", font=("Helvetica", 14),
                  command=lambda: self.start_game("easy")).pack(pady=10)
        tk.Button(root, text="Hard (6 or more letters)", font=("Helvetica", 14),
                  command=lambda: self.start_game("hard")).pack(pady=10)

    def start_game(self, mode):
        """

        :param mode: Tryb gry, który określa poziom trudności (np. "easy" lub "hard")
        :return:
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        Wisielec(self.root, mode)

