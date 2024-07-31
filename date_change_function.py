from datetime import datetime

def get_day_of_week(date_str):
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_str, '%m/%d/%y')

    # Get the day of the week (Monday is 0, Sunday is 6)
    day_of_week = date_object.weekday()

    # Convert to a more readable format (Monday, Tuesday, etc.)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = days[day_of_week]

    return day_name

if __name__ == "__main__":
    raise RuntimeError("This script should not be executed directly. Please import it as a module.")

def get_todays_date():
    # Get the current date and time
    now = datetime.now()

    # Format the date as MM-DD-YY
    formatted_date = now.strftime("%m-%d-%y")

    return formatted_date