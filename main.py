"""Lifting Log: terminal menu."""
import sqlite3
from datetime import date

from database import initialize_db
from queries import (
    add_exercise, add_workout, add_set,
    update_set, delete_set, delete_workout,
    get_exercises, get_workouts, get_workout_sets,
    get_max_lift, get_last_session, get_personal_records,
)

MENU = """
=== Lifting Log ===
1. Start a workout (log sets)
2. View workout history
3. Edit a set
4. Delete a set / workout
5. Add an exercise
6. Exercise max
7. What did I lift last time?
8. Personal records for all sets
9. Quit
"""


# Each one of these helpers will loop until the user gives valid input

def ask_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def ask_int(prompt, minimum=0):
    # minimum=1 for reps (must be > 0); the default 0 allows ids/counts of 0 or more
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter an integer that is at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def ask_date(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return date.today().isoformat()
        try:
            # Validate the date format so users have to enter it correctly (YYYY-MM-DD). If they don't, we re-prompt.
            valid_date = date.fromisoformat(user_input)
            return valid_date.isoformat()
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")

def choose_exercise():
    while True:
        exercises = get_exercises()
        print("Available exercises:")
        for exercise in exercises:
            print(f"{exercise['id']}: {exercise['name']} ({exercise['muscle_group']})")
        exercise_id = ask_int("Enter the ID of the exercise you want to choose: ")
        if any(exercise['id'] == exercise_id for exercise in exercises):
            return exercise_id
        else:
            print("Invalid exercise ID. Please choose from the list above.")


# ---------- Menu actions ----------

def start_workout():
    # Collect the workout details first. Validation lives in the helpers above,
    workout_date = ask_date("Workout date (YYYY-MM-DD, Enter for today): ")
    notes = input("Notes (optional): ").strip() or None # This is null in DB so the user doesn't HAVE to enter anything

    # Don't create the workout row yet in case the user quits before logging a set
    workout_id = None
    exercise_id = None
    set_count = 0

    while True:
        # Ask for a new exercise
        if exercise_id is None:
            exercise_id = choose_exercise()
        weight = ask_float("Weight (lbs): ")
        reps = ask_int("Reps: ", minimum=1)  # database requires reps > 0 so the user must enter a valid int.

        # The workout must exist before we can add a set. It creates it now if it doesn't exist
        if workout_id is None:
            workout_id = add_workout(workout_date, notes)
        add_set(workout_id, exercise_id, weight, reps)
        set_count += 1
        print(f"Logged set {set_count}: {weight} lbs x {reps} reps.")

        # The user can add another set or be done
        choice = input("[Enter] same exercise, [n] new exercise, [f] finish: ").strip().lower()
        if choice == "f":
            break
        if choice == "n":
            exercise_id = None 

    print(f"Workout saved for {workout_date} with {set_count} sets.")

# Small helpers shared by the actions below

def exercise_name(exercise_id):
    # choose_exercise() gives an id, and some functions want the name, this helper looks it up
    for exercise in get_exercises():
        if exercise["id"] == exercise_id:
            return exercise["name"]

def confirm(prompt):
    # True only for an explicit y. Anything else counts as no
    return input(f"{prompt} (y/n): ").strip().lower() == "y"

def print_workout(workout):
    # One workout header line followed by its sets, numbered by set id
    notes = f" - {workout['notes']}" if workout["notes"] else ""
    print(f"\nWorkout {workout['id']} on {workout['date']}{notes}")
    for s in get_workout_sets(workout["id"]):
        print(f"  Set {s['id']}: {s['name']} {s['weight']} lbs x {s['reps']}")

def choose_workout():
    # Show the workouts, then re-prompt until a listed id is entered. Returns the workout id, or None if there are no workouts.
    workouts = get_workouts()
    if not workouts:
        print("No workouts logged yet.")
        return None
    # get_workouts() is newest first; print it reversed so the newest workout
    # ends up at the bottom, right above the prompt, where it stays visible
    for w in reversed(workouts):
        print(f"{w['id']}: {w['date']}" + (f" - {w['notes']}" if w["notes"] else ""))
    valid_ids = {w["id"] for w in workouts}
    while True:
        workout_id = ask_int("Workout ID: ")
        if workout_id in valid_ids:
            return workout_id
        print("That workout ID isn't in the list.")

def choose_set(workout_id):
    # Show the sets of one workout and pick one by id. Returns None if it has no sets.
    sets = get_workout_sets(workout_id)
    if not sets:
        print("That workout has no sets.")
        return None
    for s in sets:
        print(f"  Set {s['id']}: {s['name']} {s['weight']} lbs x {s['reps']}")
    valid_ids = {s["id"] for s in sets}
    while True:
        set_id = ask_int("Set ID: ")
        if set_id in valid_ids:
            return set_id
        print("That set ID isn't in the list.")


def view_history():
    workouts = get_workouts()
    if not workouts:
        print("No workouts logged yet.")
        return
    for workout in workouts:  # already ordered newest first
        print_workout(workout)

def edit_set():
    workout_id = choose_workout()
    if workout_id is None:
        return
    set_id = choose_set(workout_id)
    if set_id is None:
        return
    weight = ask_float("New weight (lbs): ")
    reps = ask_int("New reps: ", minimum=1)
    update_set(set_id, weight, reps)
    print("Set updated.")

def delete_menu():
    kind = input("Delete a [s]et or a [w]orkout? ").strip().lower()
    if kind == "s":
        workout_id = choose_workout()
        if workout_id is None:
            return
        set_id = choose_set(workout_id)
        if set_id is None:
            return
        if confirm(f"Delete set {set_id}?"):
            delete_set(set_id)
            print("Set deleted.")
        else:
            print("Cancelled.")
    elif kind == "w":
        workout_id = choose_workout()
        if workout_id is None:
            return
        if confirm(f"Delete workout {workout_id} and all of its sets?"):
            delete_workout(workout_id)
            print("Workout deleted.")
        else:
            print("Cancelled.")
    else:
        print("Please enter s or w.")

def new_exercise():
    name = input("Exercise name: ").strip()
    muscle_group = input("Muscle group: ").strip()
    equipment = input("Equipment: ").strip()
    if not (name and muscle_group and equipment):
        print("All three fields are required.")
        return
    try:
        add_exercise(name, muscle_group, equipment)
        print(f"Added {name}.")
    except sqlite3.IntegrityError:
        # exercises.name is UNIQUE, so a duplicate name is rejected by the database
        print(f"An exercise named '{name}' already exists.")

def show_max():
    name = exercise_name(choose_exercise())
    best = get_max_lift(name)  # a row, or None if the exercise has no sets
    if best is None:
        print(f"No sets logged for {name} yet.")
    else:
        print(f"Max for {name}: {best['weight']} lbs x {best['reps']} reps on {best['date']}.")

def show_last_session():
    name = exercise_name(choose_exercise())
    sets = get_last_session(name)  # a list of rows; empty if never done
    if not sets:
        print(f"No sets logged for {name} yet.")
        return
    print(f"Last {name} session ({sets[0]['date']}):")
    for s in sets:
        print(f"  {s['weight']} lbs x {s['reps']} reps")

def show_reports():
    records = get_personal_records()
    if not records:
        print("No sets logged yet.")
        return
    print("Personal records:")
    for r in records:
        print(f"  {r['name']}: {r['pr']} lbs")


# ---------- Menu loop ----------

ACTIONS = {
    "1": start_workout,
    "2": view_history,
    "3": edit_set,
    "4": delete_menu,
    "5": new_exercise,
    "6": show_max,
    "7": show_last_session,
    "8": show_reports,
}

def main():
    initialize_db()  # create tables / seed exercises if needed
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "9":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Please enter a number from 1 to 9.")
        else:
            action()

if __name__ == "__main__":
    main()
