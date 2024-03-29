from termcolor import colored, cprint
import argparse
import platform
import random
import sys
import os

def getWords(lenght, file) :
    with open(file, "r") as f :
        allWords = f.read().split("\n")
    
    correctWords = []

    for word in allWords :
        if len(word) == lenght :
            correctWords.append(word.lower().strip())
    
    return correctWords

def printGuessed(guessed, solution, guesses) :
    id = 0

    solution = solution.upper()

    for guess in guessed :
        id += 1
        print("%s. " % (str(id).zfill(len(str(guesses)))), end="") #Adding leading zeros to large numbers. (001, 002, 003)

        i = -1
        removed = 0
        solutionList = list(solution)

        for letter in guess : #Makes sure a word with a two of the same letter gets marked correctly.
            i += 1

            letter = letter.upper()

            if letter == solution[i] :
                solutionList.pop(i - removed)
                removed += 1
        
        i = -1

        for letter in guess :
            i += 1

            letter = letter.upper()

            if letter == solution[i] :
                textColor = "white"
                background = "on_green"
            elif letter in solutionList :
                textColor = "grey"
                background = "on_yellow"
                solutionList.pop(i - removed)
                removed += 1
            else :
                textColor = "white"
                background = "on_grey"

            cprint(letter.upper(), textColor, background, end="")
        print("")

def wordee(worldLenght, guesses, wordsFile="words.txt", cheater=False, forceSolution=None) :
    if not os.path.isfile(file) :
        print(f"{file} was not found.")
        input("Press [ENTER] to exit.")
        return False

    words = getWords(worldLenght, wordsFile)

    if len(words) < 1 :
        print(f"Oh no! There weren't any {worldLenght} letter words found in {file}.")
        input("Press [ENTER] to exit.")
        return False

    if not forceSolution :
        solution = random.choice(words)
        wordlistCheck = True
    else :
        solution = forceSolution.lower().strip()
        wordlistCheck = True

        if not solution in words :
            wordlistCheck = False

    print("Welcome to Wordee!")

    if cheater :
        print("=== SOLUTION: %s ===" % (solution))

    input("Press [ENTER] to start.")

    guessed = []
    text = ""

    guessID = 0
    over = False
    while True :
        if platform == "Windows" : #Clear the screen
            os.system("cls")
        else :
            os.system("clear")

        printGuessed(guessed, solution, guesses)
        print(text, end="")

        if over :
            break

        guess = input("Guess %d: " % (guessID+1)).strip()
        text = ""

        if not len(guess) == len(solution) :
            text = "Invalid lenght! You are looking for a %d letter word.\n" % (len(solution))
            continue

        if wordlistCheck and not guess.lower() in words :
            text = "Not found in wordlist.\n"
            continue

        guessed.append(guess)
        guessID += 1

        if guess.lower() == solution :
            text = "\nYou won! The solution was %s.\n" % (solution)
            over = True

        if guessID == guesses :
            text = "\nYou ran out of guesses. The solution was %s. Better luck next time!\n" % (solution)
            over = True

    input("Press [ENTER] to exit..")
    return True


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--guesses", help="Amount of allowed guesses")
    parser.add_argument("-l", "--lenght", help="Word lenght")
    parser.add_argument("-f", "--file", help="Wordlist file")
    #parser.add_argument("-c", "--cheater", help="Show the correct solution")
    parser.add_argument("-s", "--solution", help="Force a solution")
    args = parser.parse_args()


    guesses = args.guesses
    lenght = args.lenght
    file = args.file
    forceSolution = args.solution

    if not guesses :
        guesses = 6
    if not lenght :
        lenght = 5
    if not file :
        file = "words.txt"

    try :
        guesses = int(guesses)
        lenght = int(lenght)
    except ValueError :
        print("Invalid arguments.")
        sys.exit()

    try :
        wordee(lenght, guesses, wordsFile=file, cheater=False, forceSolution=forceSolution)
    except KeyboardInterrupt :
        sys.exit()