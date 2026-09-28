class User:
    def __init__(self, username: str):
        self.username = username
        self.exercises: list("Exercise") = []
        
    def get_username(self):
        return self.username
    
    def get_exercises(self):
        return self.exercises

    def read_data(self):
        try:
            with open(f"{self.username}.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) == 4: 
                        name, distance, duration, date = parts 
                        task = Exercise(name, distance, duration, date)
                        self.exercises.append(task) 
            return True
        except FileNotFoundError:
            print(f"{self.username} has no available data.")
            return False
        
    def calculate_distance(self, exercise_name: str, month: str or None):
        total_distance = 0
        for task in self.exercises:
            if task.get_name().lower() == exercise_name.lower():
                if task.get_date() == month or month is None:
                    total_distance += task.get_distance()
        return total_distance

    def calculate_max_distance(self, exercise_name: str):
        distances = [0]
        for task in self.exercises:
            if task.get_name().lower() == exercise_name.lower():
                distances.append(task.get_distance())
        return max(distances)
    
    def calculate_duration(self, exercise_name: str, month: str or None): 
        total_duration = 0
        for task in self.exercises:
            if task.get_name().lower() == exercise_name.lower():
                if task.get_date() == month or month is None:
                    total_duration += task.get_duration()
        return total_duration
    
    def calculate_max_duration(self, exercise_name: str): 
        durations = [0]
        for task in self.exercises:
            if task.get_name().lower() == exercise_name.lower():
                durations.append(task.get_duration())
        return max(durations)


class Exercise:
    def __init__(self, name: str, distance: str, duration: str, date: str):
        self.name = name
        self.distance = float(distance)
        self.duration = int(duration)
        self.date = date

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance

    def get_date(self):
        return self.date 

    def get_duration(self):
        return self.duration


def welcome_screen():
    line = "*-*-*-*-*-*-*-*-*-*-*-*-*-*"
    welcome = """
| WELCOME TO USYD FITNESS |
"""
    actions = """
*    LOGS YOUR WORKOUT    *
*   TRACKS YOUR FITNESS   *
*    GET FIT & HEALTHY    *
"""
    box = line + welcome + line + actions + line
    print(box)


def login():
    line = "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    actions = """
| [1] Log an activity     |
| [2] Track your fitness  |
| [3] Plan your health    |
"""

    username = str(input("Login with your username: "))

    while len(username) > 20 or username is None:
        print("Your username is too long.")
        username = str(input("Login with your username: "))
    else:
        spaces = " " * (21 - len(username))
        greeting = f"""
| Hi {username}{spaces}|
"""
        login_screen = f"{line}{greeting}{line}{actions}{line}"
        print(login_screen)
        return username


def is_valid_date(date):
    if '/' not in date:
        print("Please use '/' as a separator")
        return False
    mt_yr = date.split('/')
    if len(mt_yr) != 2:
        print("Please use '/' as a separator")
        return False
    elif len(mt_yr[0]) != 2:
        print("Please enter a valid month.")
        return False
    elif not mt_yr[0].isdigit() or not 1<=int(mt_yr[0])<=12:
        print("Please enter a valid month.")
        return False
    elif len(mt_yr[1]) != 4:
        print("Please enter a valid year.")
        return False
    elif not mt_yr[1].isdigit() or not 2000<=int(mt_yr[1])<=2025:
        print("Please enter a valid year.")
        return False
    else: 
        return True


def log_workout(username: str):
    exercise = input("What exercise would you like to log? ")
    valid_exercise = ["swim", "run", "cycle"]
    if exercise.lower() not in valid_exercise:
        print(f"Sorry, {exercise} is not supported.")
        return

    #asking for month and year of exercise, and making sure correct format used
    date = input(f"What month did you {exercise} (mm/yyyy)? ")
    
    if not is_valid_date(date):
        return

    #asking for distance of exercise, and accessing magnitude and units
    #assuming correct format of input
    distance = input(f"What distance did you {exercise} (km or miles)? ")
    distance_values = distance.split( )
    distance_num = float(distance_values[0])
    #converting distance to km if inputed in miles
    if distance_values[1] == "miles":
        distance_num = distance_num * 1.6

    #asking for duration of exercise in minutes
    #assuming correct format of input
    duration = int(input(f"How long did you {exercise} (minutes)? "))

    #accessing the parameter of the log_workout function
    filename = f"{username}.txt"
    #opening a file, using a with statement, in append mode to add the exercise information to the file
    with open(filename, "a") as file:
        file.write(f"{exercise.lower()},{distance_num:.1f},{duration},{date}\n")


def track_activity(username: str):
    user = User(username) 
    if not user.read_data():
        return
    
    exercise = input("What exercise would you like to track? ")
    valid_exercise = ["swim", "run", "cycle"]
    if exercise.lower() not in valid_exercise:
        print(f"Sorry, {exercise} is not supported.")
        return
    
    date = input("What month would you like to track (mm/yyyy)? ")
    #validating a date exercise
    if date != "all": #adding in all as valid date
        if not is_valid_date(date):
            return
    else:
        date = None
    
    total_distance = user.calculate_distance(exercise, date)
    total_duration = user.calculate_duration(exercise, date)

    ex_count = 0
    for ex in user.get_exercises():
        if ex.get_name().lower() == exercise:
            if ex.get_date() == date or date is None:
                ex_count += 1
    try:
        avg_distance = total_distance / ex_count
        avg_duration = total_duration / ex_count
        avg_speed = total_distance / (total_duration / 60)
    except ZeroDivisionError:
        avg_distance = 0
        avg_duration = 0
        avg_speed = 0

    print(f"Total distance: {total_distance:.1f}km")
    print(f"Average distance: {avg_distance:.1f}km")
    print(f"Total duration: {total_duration} mins")
    print(f"Average duration: {round(avg_duration)} mins")
    print(f"Average speed (km/h): {avg_speed:.2f}km/h")


def plan_health(username: str):
    user = User(username)
    if not user.read_data():
        return

    goal = input("What goal would you like to achieve? ")
    possible_goals = ["marathon run", "marathon swim", "century", "ironman", "5 minute mile"]
    if goal.lower() not in possible_goals:
        print("Sorry, that goal is not supported.")
        return
    try:
        weeks = int(input("How many weeks do you have to achieve it? "))
    except ValueError:
        return
    if weeks <=0:
        return
    
    print(f"To achieve the {goal} challenge you need to:")

    goal_aim = {
        "marathon run": {"run": 42}, 
        "marathon swim": {"swim": 10}, 
        "century": {"cycle": 100}, 
        "ironman": {"swim": 4, "cycle": 180, "run": 42}}

    if goal.lower() in goal_aim.keys():
        needed_exercises = goal_aim[goal.lower()].items()
        for an_exercise, aim_dist in needed_exercises:
            current_max_dist = user.calculate_max_distance(an_exercise)

            if aim_dist <= current_max_dist:
                increase = 0
            else:
                increase = (aim_dist - current_max_dist) / weeks
                
            print(f"    Increase your max {an_exercise} by {increase:.1f}km per week.")
            
    elif goal.lower() == "5 minute mile":
        max_speed = 0
        for exercise in user.get_exercises():
            if exercise.get_name().lower() == "run":
                speed = exercise.get_distance() / exercise.get_duration() * 60
                if speed > max_speed:
                    max_speed = speed
        needed_speed = 12 * 1.6 
        if needed_speed <= max_speed:
            increase = 0
        else:
            increase = (needed_speed - max_speed) / weeks
        print(f"    Increase your max speed by {increase:.2f}km/h per week.")

#initialising main function
def main():
    welcome_screen() #runs function to display welcome screen

    #Ask the user to login with a username
    username = None
    while username is None:
        username = login() 

    #asking user what information they want to log/track etc.
    option = input("Choose an option: ") # should be either 1, 2 or 3
    
    #running corresponding function to what option the user chose
    if option == "1":
        log_workout(username)
    elif option == "2":
        track_activity(username)
    elif option == "3":
        plan_health(username)
    else:
        return #function is returned if an invalid option was inputted


if __name__ == '__main__':
    main()