"""Database setup: connection, schema, and starter exercise data."""
import sqlite3

def get_connection():
    conn = sqlite3.connect('lifting.db')
    conn.row_factory = sqlite3.Row
    # Foreign keys are off by default so we have to turn them on every time for it to work right.
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

# Three tables: exercises and workouts are independent; sets is the table that links them so the tables stay clean
MY_TABLES = """
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,    
    muscle_group TEXT NOT NULL,
    equipment TEXT NOT NULL        
);
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,           
    notes TEXT                     
);
CREATE TABLE IF NOT EXISTS sets (
    id INTEGER PRIMARY KEY,
    workout_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    weight REAL NOT NULL CHECK(weight >= 0),   
    reps INTEGER NOT NULL CHECK(reps > 0),
    -- Deleting a workout also deletes its sets
    FOREIGN KEY(workout_id) REFERENCES workouts(id) ON DELETE CASCADE,
    -- No cascade: an exercise that has logged sets cannot be deleted
    FOREIGN KEY(exercise_id) REFERENCES exercises(id)
);

CREATE INDEX IF NOT EXISTS idx_sets_exercise ON sets(exercise_id);
CREATE INDEX IF NOT EXISTS idx_sets_workout ON sets(workout_id);
CREATE INDEX IF NOT EXISTS idx_workouts_date ON workouts(date);

"""

# Starter Common lifts as (name, muscle_group, equipment)
EXERCISES = [
    ('Bench Press', 'Chest', 'Barbell'),
    ('Squat', 'Legs', 'Barbell'),
    ('Deadlift', 'Back', 'Barbell'),
    ('Overhead Press', 'Shoulders', 'Barbell'),
    ('Pull-Up', 'Back', 'Bodyweight'),
    ('Dumbbell Row', 'Back', 'Dumbbell'),
    ('Bicep Curl', 'Arms', 'Dumbbell'),
    ('Tricep Extension', 'Arms', 'Dumbbell'),
    ('Lunge', 'Legs', 'Bodyweight'),
    ('Plank', 'Core', 'Bodyweight'),
    ('Seated Leg Curl', 'Legs', 'Machine'),
    ('Leg Press', 'Legs', 'Machine'),
    ('Calf Raise', 'Legs', 'Dumbbell'),
    ('Chest Fly', 'Chest', 'Dumbbell'),
    ('Lat Pulldown', 'Back', 'Machine'),
    ('Shoulder Press', 'Shoulders', 'Dumbbell'),
    ('Hammer Curl', 'Arms', 'Dumbbell'),
    ('Tricep Dip', 'Arms', 'Bodyweight'),
    ('Russian Twist', 'Core', 'Bodyweight'),
    ('Leg Extension', 'Legs', 'Machine')
    ]

def fill_exercises(conn):
    # only insert if the table is empty - otherwise we will get duplicates!
    cursor = conn.execute('SELECT COUNT(*) FROM exercises')
    if cursor.fetchone()[0] == 0:
        # Executes SQL command to insert all our rows from above into the table
        conn.executemany('INSERT INTO exercises (name, muscle_group, equipment) VALUES (?, ?, ?)', EXERCISES)
        conn.commit()

def initialize_db():
    conn = get_connection()
    conn.executescript(MY_TABLES)
    fill_exercises(conn)
    conn.close()

if __name__ == '__main__':
    initialize_db()
