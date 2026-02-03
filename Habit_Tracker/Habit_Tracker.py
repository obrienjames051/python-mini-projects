import json
import os # For file operations
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory of the current script
data_file = os.path.join(BASE_DIR, "habits_data.json") # Full path to the data file

today = date.today() #this is a date object, not a string
today_str = today.isoformat() #converts the date object into a string in the format YYYY-MM-DD

def load_data():
    if not os.path.exists(data_file): #creates the file if it doesn't exist
        data = {
            "habits": {},
            "logs": {}
        }
        save_data(data)
        return data

    with open(data_file, "r") as file: #'with ... as file' is a context manager, it closes the file automatically, temporarily calls the file 'file'
        return json.load(file) #reads the json data and converts it into a python dictionary

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=2) #converts the python dictionary into json, indent=2 makes the json file easier to read

def create_habit():
    data = load_data()

    print('\nCreate a new habit')
    habit_name = input('Enter habit name: ').strip().lower()

    if not habit_name:
        print('Habit name cannot be empty.')
        return #renturns to the main menu loop
    
    if habit_name in data['habits']: #checks the habits section of the data dictionary
        print('That habit already exists.')
        return
    
    print('\nSelect habit type:')
    print('1. Binary (yes/no)')
    print('2. Quantitative (numeric value)')
    habit_type_choice = input('Enter choice (1 or 2): ').strip()

    if habit_type_choice == '1': #creates a dictionary for the definition of the habit
        habit_type = 'binary'
        habit_data = {
            'type': habit_type,
            'created': today_str,
            'active': True
        }

    elif habit_type_choice == '2': #creates a dictionary for the definition of the habit
        habit_type = 'quantitative'
        unit = input('Enter unit (e.g. minutes, reps, etc.): ').strip().lower()

        if not unit: #stops empty unit entries
            print('Unit cannot be empty.')
            return

        habit_data = {
            'type': habit_type,
            'unit': unit,
            'created': today_str,
            'active': True
        }
    
    else:
        print('\nInvalid choice. Habit not created.')
        return
    
    data['habits'][habit_name] = habit_data #adds the new habit to the habits section of the data dictionary
    save_data(data)
    print(f'\nHabit "{habit_name}" created successfully!') #f-string lets you put variables inside strings

def log_today_habits():
    data = load_data()

    if not data['habits']:
        print('\nNo habits found. Please create a habit first.')
        return #cancels the whole function and returns to the main menu loop
    
    if today_str not in data['logs']: #checks if there is already a log for today
        data['logs'][today_str] = {} #creates an empty log for today if not

    for habit_name, habit_info in data['habits'].items(): #habit_name becomes the key, habit_info becomes the value (dictionary in this case)
        # .items() returns both the key and value from the dictionary

        if not habit_info.get('active', True): #checks the dictionary habit_info for the key 'active'
            continue #skips inactive habits

        habit_type = habit_info['type'] #binary or quantitive
        unit = habit_info.get('unit', '') #gets the unit if it exists, otherwise returns '' - an empty string

        if habit_name in data ['logs'][today_str]:
            while True:
                choice = input (f'"{habit_name}" already logged. Overwrite? (y = overwrite, s = skip): ').strip().lower()

                if choice == 's':
                    break # exits the while loop (later the program skips to the net habit if choice is 's')
                elif choice == 'y':
                    pass #continues to the logging section below. Used when you must have some code in the block and jsut tells the program to move on
                else:
                    print("Invalid input. Enter 'y' or 's'. ")
                    continue #skips the rest of the while loop and runs it again

                break # exits the while loop and continues the rest of the function
        
        else:
            choice = 'y' #if the habit hasn't been logged, this will avoid an error in the next line

        if choice == 's':
            continue #skips to the next habit in the loop

        if habit_type == 'binary':
            while True:
                completed = input(f'Did you complete "{habit_name}" today? (y/n): ').strip().lower()

                if completed == 'y':
                    data['logs'][today_str][habit_name] = True #marks the habit as done
                    break #exits the inner while loop
                
                elif completed == 'n':
                    data['logs'][today_str][habit_name] = False #marks the habit as not done
                    break #exits the inner while loop

                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

        elif habit_type == 'quantitative':
            while True:
                value = input(f'How many {unit} did you log for "{habit_name}" today? ').strip() # "" marks around {habit_name} is simply a design choice

                try: # try is used to catch errors that may occur in the block
                    value = float(value)
                    if value < 0:
                        print('Value cannot be negative. Please enter a valid number.')
                        continue #repeats the inner while loop
                    data['logs'][today_str][habit_name] = value
                    break #exits the inner while loop

                except ValueError: #loops back to the start of the inner while loop if the value cannot be converted to a float
                    print('Invalid input. Please enter a numeric value.')
        
    save_data(data)
    print("\nToday's habits logged successfully!")

def edit_habit_status():
    data = load_data()

    if not data['habits']:
        print('\nNo habits found. Please create a habit first.')
        return #cancels the whole function and returns to the main menu loop
    
    print('\nSelect a habit to edit:')

    habit_list = list(data['habits'].keys())

    for i, habit_name in enumerate(habit_list, start=1): #.keys() gets the keys from the dictionary. enumerate() adds a counter to the loop, start=1 makes it start from 1
        status = 'active' if data['habits'][habit_name]['active'] else 'inactive' #ternary operator, a one-line if-else statement
        print(f'{i}. {habit_name} ({status})')
    
    while True:
        choice = input("\nEnter number or 'q' to cancel: ").strip().lower()

        if choice == 'q':
            return
        
        try:
            choice = int(choice)
            if choice < 1 or choice > len(habit_list):
                print("Please enter a valid number or 'q' to cancel.")
                continue #repeats the while loop
            else:
                break #exits the while loop

        except ValueError:
            print("Please enter a valid number or 'q' to cancel.")
            continue #repeats the while loop
        
    habit_name = habit_list[choice - 1] #gets the habit name based on the user's choice
    current_status = data['habits'][habit_name]['active'] #gets the current status
    new_status = not current_status #toggles the status
    data['habits'][habit_name]['active'] = new_status #updates the status in the data dictionary
    save_data(data)

    print(f"\n{habit_name} is now {'active' if new_status else 'inactive'}.")

print(f'\nHello! Today is {today_str}. Welcome to your Habit Tracker!')

#main menu loop
while True:
    try:
        print('\nWhat would you like to do?\n'
      '\nCreate habits'
      '\nLog today\'s habits'
      '\nEdit habits'
      '\nView habit stats'
      '\nView weekly summary'
      '\nExit')
        choice = input('\nEnter your choice: ').lower()

        if choice == 'edit habits' or choice == 'edit habit' or choice == 'edit':
            edit_habit_status()

        if choice == 'create habits' or choice == 'create habit' or choice == 'create':
            create_habit()

        elif choice == 'log today\'s habits' or choice == 'log habits' or choice == 'log habit' or choice == 'log':
            log_today_habits()

        elif choice == 'view habit stats' or choice == 'view stats' or choice == 'habit stats':
            print('stats')
        
        elif choice == 'view weekly summary' or choice == 'weekly summary' or choice == 'view summary':
            print('summary')

        elif choice == 'exit' or choice == 'end':
            print('Goodbye!')
            break

        else:
            print('\nPlease enter a valid input.')
    
    except ValueError:
        print('Please enter a valid input.')