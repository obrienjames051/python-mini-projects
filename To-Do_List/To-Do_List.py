from pathlib import Path

# Ensure the todo file is resolved relative to this script's directory so the
# program will always use `To-Do_List/todo.txt` regardless of the current
# working directory when the script is run.
BASE_DIR = Path(__file__).parent
FILENAME = BASE_DIR / "todo.txt"  # this uses a new variable so if the file name changes you only have to change it here

def load_list():
    try: #try to do this, if not then move to except
        with open(FILENAME, "r") as file: #opens FILENAME in read mode "r"
            return [line.strip() for line in file.readlines()] #this loops through each line in the file
    except FileNotFoundError: #incase the file doesn't exist yet
        return [] #start with an empty file

def save_list(todo_list): #todo_list is used inside this function as it makes it reusable and not locked to a global variable
    with open(FILENAME, "w") as file: #opens FILENAME in write mode "w"
        for item in todo_list: #loops over every string in the list
            file.write(item + "\n") #writes each item followed by a new line \n

Todo = load_list() #this is the main list variable

def show_list():
    print('Here is your To-Do list: ')
    for item in Todo:
        print("- " + item)

#main loop
while True:
    try:
        instruction = input("What would you like to do? See, add, or delete To-Do's? Or end? ")
        if instruction.upper() == "SEE":
            show_list()
        elif instruction.upper() == "ADD":
            add = input("What would you like to add? ").strip()
            Todo.append(add)
            save_list(Todo)
            show_list()
        elif instruction.upper() == "DELETE":
            delete = input("What would you like to delete? ").strip()
            found = False
            for item in Todo: #loops through each entry in the list
                if item.lower() == delete.lower(): #double = means comparison whereas single means asign
                    Todo.remove(item)
                    save_list(Todo)
                    print(f'"{item}" has been removed.') #f means evaluate the expression inside {} and put the values into this string
                    show_list()
                    found = True
                    break #stops the loop
            if not found:
                print("Item wasn't found.")
        elif instruction.upper() == "END":
            print("Goodbye!")
            break
        else:
            print("Please enter a valid input. ")
    except ValueError:
        print("Please enter a valid input. ")