word_to_be_guessed = "hirsipuu"
guessed_letters = {}


def ask():
    return input("Arvaa kirjain (tai koko sana): ").lower()


def main():
    while True:
        obscured_word = ""
        for c in word_to_be_guessed:
            if guessed_letters.get(c):
                obscured_word += c
            else:
                obscured_word += "_"

        if obscured_word == word_to_be_guessed:
            print(f"Onneksi olkoon! Olet arvannut sanan '{word_to_be_guessed}' oikein!")
            break

        print("")
        # print(f"Arvatut kirjaimet: {', '.join(list(guessed_letters.keys()))}")
        print(f"Piilotettu sana: {obscured_word}")

        while True:
            guess = ask()
            if guess == word_to_be_guessed:
                for c in word_to_be_guessed:
                    guessed_letters[c] = True
                break

            if len(guess) == 1:
                if guess in guessed_letters:
                    print(f"Olet jo arvannut kirjaimen '{guess}'.")
                    continue

                if guess in word_to_be_guessed:
                    print(f"Kirjain '{guess}' on sanassa!")
                else:
                    print(f"Kirjain '{guess}' ei ole sanassa.")

                guessed_letters[guess] = True
                break
            else:
                print("Arvaa yksi kirjain tai koko sana.")


if __name__ == "__main__":
    main()
