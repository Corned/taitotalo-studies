class Guessword:
    def __init__(self, word):
        self.__answer_word = word
        self.guessed_letters = {}

    def generate_hidden_word(self) -> str:
        return "".join(
            [c if c in self.guessed_letters else "_" for c in self.__answer_word]
        )

    def is_resolved(self) -> bool:
        return self.__answer_word == self.generate_hidden_word()

    def resolve_letter(self, letter: str):
        self.guessed_letters[letter] = True


game = Guessword("kuningas")

while not game.is_resolved():
    print(game.generate_hidden_word())
    letter = input("Kirjain? ")
    game.resolve_letter(letter)

print("Voitit!", game.generate_hidden_word())
