import json
import os # For file operations
from datetime import date, timedelta # timedelta represents a difference in time

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

    for i, habit_name in enumerate(habit_list, start=1):
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

def view_habit_stats():
    data = load_data()

    if not data['habits']: #stops the function if there are no habits
        print('\nNo habits found. Please create a habit first.')
        return #cancels the whole function and returns to the main menu loop
    
    print('\nHabit Statistics (active only):\n')

    for habit_name, habit_info in data['habits'].items(): # .items() returns both the key and value from the dictionary
        if not habit_info.get('active', True):
            continue #skips the iteration of the for loop for inactive habits

        habit_type = habit_info['type']
        created = habit_info['created']
        unit = habit_info.get('unit', '') #only for quantative habits, empty string otherwise

        days_logged = 0 #defining variables to be used in the loop below
        days_completed = 0
        total_units = 0

        for log_date, daily_log in data['logs'].items(): # runs through each date and looks for the specific habit
            if habit_name not in daily_log:
                continue #skips that iteration of the for loop if the habit wasn't logged that day
            days_logged += 1
            value = daily_log[habit_name] #gets the logged value for that habit on that day

            if habit_type == 'binary': #counts days completed for binary habits
                if value is True:
                    days_completed += 1
                
            elif habit_type == 'quantitative': #counts totals for quantitative habits
                total_units += value
        
        print(f'Habit: {habit_name}')
        print(f'Type: {habit_type}')
        print(f'Created on: {created}')
        print(f'Days logged: {days_logged}')

        if habit_type == 'binary': #days completed for binary habits
            print(f'Days completed: {days_completed}')
            if days_logged > 0:
                completion_rate = (days_completed / days_logged) * 100
                print(f'Completion rate: {completion_rate:.2f}%') #:.2f limits to 2 decimal places
            else:
                print('Completion rate: N/A')
        
        elif habit_type == 'quantitative': #averages for quantative habits
            print(f'Total: {total_units} {unit}')
            if days_logged > 0:
                average = total_units / days_logged
                print(f'Average per day logged: {average:.2f} {unit}')
            else:
                print('Average per day logged: N/A')

        print('-' * 30) #prints a line of dashes to separate the stats for each habit

def get_week_range(date_obj):
    """
    given a date object, return Monday to Sunday for the week that date is in.
    """

    weekday_index = date_obj.weekday() # .weekday() returns an index for each day of the week, Monday = 0, Sunday = 6
    week_start = date_obj - timedelta(days=weekday_index) # subtracts the weekday index from the date gives you the Monday of that week
    week_end = week_start + timedelta(days=6) # adds 6 days to the Monday gives you the Sunday of that week

    return week_start, week_end #returns a tuple

def get_dates_in_range(start_date, end_date):
    """
    Returns a list of date objects from start_date to end_date inclusive.
    """

    dates = [] # this will store the date objects in the range
    current_date = start_date # define loop variable

    while current_date <= end_date: # loop until the current date is after the end date
        dates.append(current_date)
        current_date += timedelta(days=1) # adds one day and keeps it as a date object
    
    return dates #returns a list of date objects

def calculate_stats_for_range(habit_name, habit_info, start_date, end_date, data):
    """
    Calculates statistics for a single habit between start_date and end_date inclusive.
    Returns a dictionary of computed stats.
    """

    habit_type = habit_info['type'] #used to determine how the stats are calculated
    unit = habit_info.get('unit', '') #only for quantative habits, empty string otherwise

    days_logged = 0 #define counters to be used in the loop below
    days_completed = 0
    total_units = 0

    for log_date_str, daily_log in data['logs'].items(): # loops through each log and looks for the specific habit
        log_date = date.fromisoformat(log_date_str) #converts the date string back into a date object

        if log_date_str < start_date or log_date > end_date:
            continue #skips the iteration of the for loop if the log date is outside the specified range

        if habit_name not in daily_log:
            continue #skips the iteration of the for loop if the habit wasn't logged that day

        days_logged += 1
        value = daily_log[habit_name] #gets the logged value for that habit on that day

        if habit_type == 'binary':
            if value is True:
                days_completed += 1

        elif habit_type == 'quantitative':
            total_units += value
    
    if habit_type == 'binary':
        completion_rate = None
        if days_logged > 0:
            completion_rate = (days_completed / days_logged) * 100
        
        return { #returns a dictionary of the calculated stats
            'type': 'binary',
            'days_logged': days_logged,
            'days_completed': days_completed,
            'completion_rate': completion_rate
        }
    
    elif habit_type == 'quantitative':
        average = None
        if days_logged > 0:
            average = total_units / days_logged
        
        return { #returns a dictionary of the calculated stats
            'type': 'quantitative',
            'days_logged': days_logged,
            'total_units': total_units,
            'average': average,
            'unit': unit
        }

def get_completed_weeks(habit_created_date, today):
    """
    Returns a list of (week_start, week_end) tuples for completed weeks,
    Starting after the habit was created and excluding the current week.
    """

    completed_weeks = [] #this will store the completed weeks as tuples of (week_start, week_end)

    creation_week_start, _ = get_week_range(habit_created_date) #gets the start of the week for the habit creation date
    first_week_start = creation_week_start + timedelta(days=7) # avoids the incomplete week of the habit creation

    current_week_start, _ = get_week_range(today) #gets the start of the current week, to exclude it from the completed weeks

    current_week = first_week_start # define loop variable

    while current_week < current_week_start: #loops through all completed weeks
        week_start = current_week #date object for the start of the week
        week_end = week_start + timedelta(days=6) #date object for the end of the week
        completed_weeks.append((week_start, week_end))
        current_week += timedelta(days=7) #moves to the next week by adding 7 days
    
    return completed_weeks #returns a list of tuples of (week_start, week_end)


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

        elif choice == 'view habit stats' or choice == 'view stats' or choice == 'habit stats' or choice == 'stats':
            view_habit_stats()
        
        elif choice == 'view weekly summary' or choice == 'weekly summary' or choice == 'view summary':
            print('summary')

        elif choice == 'exit' or choice == 'end':
            print('Goodbye!')
            break

        else:
            print('\nPlease enter a valid input.')
    
    except ValueError:
        print('Please enter a valid input.')