import random

def play_game(): #defines a function that can be called to at any point in the code. parameters can be added in ()

    attempts = 0
    number = random.randint(1,100) #random number between 1 and 100
    print("Let's play a guessing game! ")

    while True: #this runs the loop
        try:
            guess = int(input("Guess a number between 1 and 100: "))
            attempts += 1

            if guess < number:
                print("Too Low! Try again ")
            elif guess > number:
                print("Too High! Try again ")
            else:
                print("Good job, you guessed it in " + str(attempts) + " attempts!")
                break #this stops the loop
        except ValueError: #this catches errors
            print("That's not a number. Try again: ")

while True:
    play_game() #this calls the previously defined function
    again = input("Would you like to play again? (yes/no): ").strip().lower() #removes spaces and converts to lower case
    if again not in ("yes", "y"): #this allows the playing to keep going until they want to stop
        print("Thanks for playing!")
        break