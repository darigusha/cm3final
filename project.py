import random
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")  # Serve files from 'static' folder
CORS(app)

# Hangman game logic
WORDS = ["python", "hangman", "challenge", "developer", "programming"]

class Hangman:
    def __init__(self):
        self.word = random.choice(WORDS).upper()
        self.guessed_letters = set()
        self.lives = 5
        self.correct_guesses = set()

    def display_word(self):
        return " ".join(letter if letter in self.correct_guesses else "_" for letter in self.word)

    def make_guess(self, letter):
        letter = letter.upper()

        if self.has_won():  # If already won, always return win message
            return "Congratulations! You've won!"

        if letter in self.guessed_letters:
            return "You already guessed that letter."

        self.guessed_letters.add(letter)

        if letter in self.word:
            self.correct_guesses.add(letter)
            if self.has_won():
                return "Congratulations! You've won!"
            return "Good guess!"
        else:
            self.lives -= 1
            if self.lives <= 0:  # Ensure game over message is returned
                return f"Game over! The word was {self.word}."
            return "Wrong guess!"

    def guess_word(self, guessed_word):
        guessed_word = guessed_word.upper()
        if guessed_word == self.word:
            self.correct_guesses = set(self.word)
            return "Congratulations! You've won!"
        else:
            self.lives -= 1
            if self.lives == 0:
                return f"Game over! The word was {self.word}."
            return "Wrong word!"

    def has_won(self):
        return set(self.word) == self.correct_guesses

    def get_lives(self):
        return self.lives

    def get_word(self):
        return self.word

game = Hangman()

# API Routes
@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    letter = data.get("letter", "").strip()
    message = game.make_guess(letter)
    return jsonify({"message": message, "word": game.display_word(), "lives": game.get_lives()})

@app.route("/guess_word", methods=["POST"])
def guess_word():
    data = request.get_json()
    guessed_word = data.get("word", "").strip()
    message = game.guess_word(guessed_word)
    return jsonify({"message": message, "word": game.display_word(), "lives": game.get_lives()})

@app.route("/restart", methods=["GET"])
def restart():
    global game
    game = Hangman()
    return jsonify({"message": "Game restarted!", "word": game.display_word(), "lives": game.get_lives()})

# Route to serve HTML file
@app.route("/")
def serve_html():
    return send_from_directory("static", "user.html")  # Serves user.html

if __name__ == "__main__":
    app.run(debug=True)
