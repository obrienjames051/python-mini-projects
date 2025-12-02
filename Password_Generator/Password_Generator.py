import random
import string #string is a set of pre-written lists of character types, so you don't have to write them out
from pathlib import Path

BASE_DIR = Path(__file__).parent
FILENAME = BASE_DIR / "passwords.txt"

def load_list():
    try: #try to do this, if not then move to except
        with open(FILENAME, "r") as file: #opens FILENAME in read mode "r"
            return [line.strip() for line in file.readlines()] #this loops through each line in the file
    except FileNotFoundError: #incase the file doesn't exist yet
        return [] #start with an empty file

def save_list(password_list): #password_list is used inside this function as it makes it reusable and not locked to a global variable
    with open(FILENAME, "w") as file: #opens FILENAME in write mode "w"
        for item in password_list: #loops over every string in the list
            file.write(item + "\n") #writes each item followed by a new line \n

passwords = load_list() #this is the main list variable

def show_list():
    if not passwords:
        print("\nYour password list is empty.")
    else:
        print('\nHere is your List of passwords: ')
        for item in passwords:
            print(item)

def generate_password(length):
    lower = random.choice(string.ascii_lowercase) #these choose one from each set
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice(string.punctuation)

    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + string.punctuation
    remaining_chars = [random.choice(all_chars) for _ in range(remaining_length)] #this chooses the remaining characters and puts them in a list
    password_list = [lower, upper, digit, special] + remaining_chars #this combines all the characters for the password
    random.shuffle(password_list) #this mixes it all up to make sure the password doesn't always start with lower, upper, digit, special
    password = "".join(password_list) #this combines all the characters

    return password

while True:
    view = input("\nWould you like to see your saved passwords, generate a new one, delete an entry or end? (see/generate/delete/end): ").strip().lower()
    if view == "see":
        show_list()
    elif view == "generate":
        while True: #this is the general loop for generating passwords
            try:
                length = int(input("\nHow many characters would you like your password to be? "))
                if length < 4:
                    print("Password must be at least 4 characters to include all character types.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")

        generated = generate_password(length)
        print("Your password is: ",generated)  # generated used instead of password as password only exists within the function

        add_file = input("Would you like to add this to your passwords file? (yes/no): ").strip().lower()
        if add_file == "yes":
            password_use = input("What is this password for? ").strip()
            label_lower = password_use.lower()
            existing_index = None

            for i, item in enumerate(passwords): #enumerate keeps track of the index 'i' and the element in the list 'item'
                if item.lower().startswith(label_lower + " -"): # " -" used to make sure searching 'Google' doesn't trigger 'Google Mail'
                    existing_index = i
                    break

            list_entry = f"{password_use} - {generated}"

            if existing_index is not None:
                replace = input(f"An entry for '{password_use}' already exists. Would you like to replace it? (yes/no): ").strip().lower()
                if replace == "yes":
                    passwords[existing_index] = list_entry #this replaces the item in the list in the same position
                    print(f"Entry for '{password_use}' updated.")
                else:
                    print("Entry not changed.")
            else:
                passwords.append(list_entry)
                print(f"Entry for '{password_use}' added.")

            save_list(passwords)

    elif view == "delete":
        delete = input("Which entry would you like to delete? ").strip().lower()
        found = False
        for item in passwords:  # loops through each entry in the list
            if item.lower().startswith(delete + " -"): # this searches to see if the input is in the line, not the full line
                passwords.remove(item)
                save_list(passwords)
                print(f'"{item}" has been removed.')  # f means evaluate the expression inside {} and put the values into this string
                show_list()
                found = True
                break  # stops the loop
        if not found:
            print("Item wasn't found.")
    elif view == "end":
        print("Goodbye.")
        break
    else:
        print("Please enter a valid input.")