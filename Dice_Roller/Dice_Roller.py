import random

yes = ['yes', 'y', 'yeah', 'ye', 'yep']

def roll_dice():
    while True:
        try:
            number_of_dice = int(input("How many dice do you want to roll? "))
            if number_of_dice < 1:
                print("Please enter a number greater than 0.")
            else:
                break
        except ValueError:
            print("Please enter a whole number.")

    same_sides = input("Are all the dice the same? (yes/no): ").strip().lower()
    if same_sides in yes:
        while True:
            try:
                sides = int(input("How many sides do the dice have? "))
                if sides < 2:
                    print("Each die must have at least 2 sides.")
                else:
                    dice_sides = [sides] * number_of_dice
                    break #stops the full loop
            except ValueError:
                print("Please enter a whole number.")
    else:
        while True:
            number_of_sides = input("Enter the number of sides for each die, separated by spaces (e.g. 6 8 4): ")
            dice_sides = number_of_sides.split() #.split() splits a string into elements of a list
            if len(dice_sides) != number_of_dice:
                print(f'You need to enter exactly {number_of_dice} numbers.')
                continue #continue skips the rest of the current loop and goes to the next one. i.e. if an incorrect number of numbers is entered it runs the loop again

            try:
                dice_sides = [int(sides) for sides in dice_sides] #this converts each element of the list into an integer
                if any(s <= 1 for s in dice_sides): #s is just used here as a placeholder while it loops through each number in the list
                    print('Each die must have at least 2 sides.')
                    continue
                break
            except ValueError:
                print("Please make sure all numbers are positive integers.")

    outcomes = [random.randint(1, sides) for sides in dice_sides] #list comprehension. This rolls each die and adds it to a new list, all in one line

    print(f"Your die rolls are: {outcomes}")
    print(f"Total: {sum(outcomes)}")

while True:
    roll_dice()
    again = input("\nWould you like to go again? (yes/no): ").strip().lower()
    if again not in yes:
        print("Thanks for playing!")
        break