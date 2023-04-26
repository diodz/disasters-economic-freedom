import subprocess
import time
import random
from datetime import datetime, timedelta

# Function to run a command in the console
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

# Function to format datetime for git
def format_git_date(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

# Function to simulate a file change
def simulate_change(file_path):
    with open(file_path, 'a') as f:
        f.write(f"# Change made on {datetime.now()}\n")

# Start date
current_date = datetime(2023, 4, 26)

# End date
end_date = datetime(2024, 4, 21)

while current_date < end_date:
    # Random hour of the day
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    
    # Set the time part to the random values
    current_date = current_date.replace(hour=random_hour, minute=random_minute, second=random_second)
    
    # Simulate a change in the file to ensure there is something to commit
    simulate_change('scripts/data_preparation.py')
    
    # Commit message with the current date
    commit_command = f'GIT_AUTHOR_DATE="{format_git_date(current_date)}" GIT_COMMITTER_DATE="{format_git_date(current_date)}" git commit -m "Updated flask app on {current_date.strftime("%Y-%m-%d")}"'
    print(current_date.strftime("%Y-%m-%d"))
    # Run git commands
    run_command('git add -A')  # Stage all changes, including new files
    run_command(commit_command)
    
    # Check if there are any changes to stash
    status_result = subprocess.run('git status --porcelain', shell=True, capture_output=True, text=True)
    if status_result.stdout:
        run_command('git stash')
        run_command('git pull --rebase')
        run_command('git stash pop')
    else:
        run_command('git pull --rebase')
    
    run_command('git push')
    
    # Wait 1 sec
    time.sleep(1)
    
    # Increment current_date by a random float number between 1 hour and 60 hours
    increment_hours = random.uniform(1, 60)
    current_date += timedelta(hours=increment_hours)
