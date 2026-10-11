import tkinter as tk
from tkinter import messagebox
import random

class GuessingGame:
    """A Tkinter application incorporating difficulty selection and a guessing game."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the application, creating the difficulty selection interface.

        :param root: The main Tkinter window.
        """
        self.root = root
        self.root.title("Guess the Number")
        self.root.geometry("300x200")

        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(expand=True)

        tk.Label(self.difficulty_frame, text="Select Difficulty:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.difficulty_frame, text="Easy (10 guesses)", command=lambda: self.start_game(10)).pack(pady=5)
        tk.Button(self.difficulty_frame, text="Medium (7 guesses)", command=lambda: self.start_game(7)).pack(pady=5)
        tk.Button(self.difficulty_frame, text="Hard (5 guesses)", command=lambda: self.start_game(5)).pack(pady=5)

        self.game_frame: tk.Frame | None = None
        self.secret_number: int = 0
        self.guesses_left: int = 0
        self.guess_entry: tk.Entry | None = None
        self.result_label: tk.Label | None = None
        self.counter_label: tk.Label | None = None

    def start_game(self, guesses: int) -> None:
        """
        Sets up the game logic and switches the UI to the game interface.

        :param guesses: The total number of guesses allowed for the selected difficulty.
        """
        self.guesses_left = guesses
        self.secret_number = random.randint(1, 100)
        
        self.difficulty_frame.pack_forget()

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True)

        tk.Label(self.game_frame, text="Guess a number (1-100):", font=("Arial", 12)).pack(pady=10)
        
        self.guess_entry = tk.Entry(self.game_frame)
        self.guess_entry.pack(pady=5)

        tk.Button(self.game_frame, text="Guess", command=self.check_guess).pack(pady=5)

        self.counter_label = tk.Label(self.game_frame, text=f"Guesses left: {self.guesses_left}")
        self.counter_label.pack(pady=5)

        self.result_label = tk.Label(self.game_frame, text="")
        self.result_label.pack(pady=5)
        
        self.guess_entry.bind('<Return>', lambda event: self.check_guess())

    def check_guess(self) -> None:
        """Processes the user's guess, updates the game state, and handles win/loss conditions."""
        if not self.guess_entry or not self.result_label or not self.counter_label:
            return

        try:
            guess_val = int(self.guess_entry.get())
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")
            self.guess_entry.delete(0, tk.END)
            return

        self.guesses_left -= 1
        self.guess_entry.delete(0, tk.END)

        if guess_val == self.secret_number:
            messagebox.showinfo("Game Over", f"Congratulations! You guessed {self.secret_number}!")
            self.reset_to_menu()
        elif self.guesses_left == 0:
            messagebox.showinfo("Game Over", f"Sorry, you ran out of guesses. The number was {self.secret_number}.")
            self.reset_to_menu()
        elif guess_val < self.secret_number:
            self.result_label.config(text="Too low!", fg="blue")
            self.counter_label.config(text=f"Guesses left: {self.guesses_left}")
        else:
            self.result_label.config(text="Too high!", fg="blue")
            self.counter_label.config(text=f"Guesses left: {self.guesses_left}")

    def reset_to_menu(self) -> None:
        """Removes the game interface and brings back the difficulty selection screen."""
        if self.game_frame:
            self.game_frame.pack_forget()
            self.game_frame.destroy()
        self.difficulty_frame.pack(expand=True)

if __name__ == "__main__":
    root_win = tk.Tk()
    app = GuessingGame(root_win)
    root_win.mainloop()