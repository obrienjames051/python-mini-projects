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
    print('2. Quantitive (numeric value)')
    habit_type_choice = input('Enter choice (1 or 2): ').strip()

    if habit_type_choice == '1': #creates a dictionary for the definition of the habit
        habit_type = 'binary'
        habit_data = {
            'type': habit_type,
            'created': today_str,
            'active': True
        }

    elif habit_type_choice == '2': #creates a dictionary for the definition of the habit
        habit_type = 'quantitive'
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
        print('Invalid choice. Habit not created.')
        return
    
    data['habits'][habit_name] = habit_data #adds the new habit to the habits section of the data dictionary
    save_data(data)
    print(f'Habit "{habit_name}" created successfully!') #f-string lets you put variables inside strings

def log_today_habits():
    data = load_data()


print(f'\nHello! Today is {today_str}. Welcome to your Habit Tracker!')

while True:
    try:
        print('\nWhat would you like to do?\n'
      '\nCreate habits'
      '\nLog today\'s habits'
      '\nView habit stats'
      '\nView weekly summary'
      '\nExit')
        choice = input('\nEnter your choice: ').lower()

        if choice == 'create habits' or choice == 'create habit':
            create_habit()

        elif choice == 'log today\'s habits' or choice == 'log habits' or choice == 'log habit':
            print('logged')

        elif choice == 'view habit stats' or choice == 'view stats' or choice == 'habit stats':
            print('stats')
        
        elif choice == 'view weekly summary' or choice == 'weekly summary' or choice == 'view summary':
            print('summary')

        elif choice == 'exit' or choice == 'end':
            print('Goodbye!')
            break

        else:
            print('Please enter a valid input.')
    
    except ValueError:
        print('Please enter a valid input.')