from database import get_connection

# ---------- Insert ----------

# Every write uses try/finally so the connection is closed even if the
# statement fails (e.g. a UNIQUE or foreign key error). An unclosed connection
# keeps its transaction open and makes the next write fail with "database is locked".

def add_exercise(name, muscle_group, equipment):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO exercises (name, muscle_group, equipment) VALUES (?, ?, ?)',
                        (name, muscle_group, equipment))
        conn.commit()  # use this before closing the connection so the sql command is commited.
        return cursor.lastrowid  # new id is the id of the new row we inserted so we can attach sets to this id#
    finally:
        conn.close()

def add_workout(date, notes = None):
    # Returns the new workout id so we can attach sets to it
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO workouts (date, notes) VALUES (?, ?)',
                       (date, notes))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def add_set(workout_id, exercise_id, weight, reps):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sets (workout_id, exercise_id, weight, reps) VALUES (?, ?, ?, ?)',
                       (workout_id, exercise_id, weight, reps))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

# ---------- Update ----------
# WHERE id = ? is needed - without it, all the rows would be updated/deleted.
def update_set(set_id, weight, reps):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE sets SET weight = ?, reps = ? WHERE id = ?',
                       (weight, reps, set_id))
        conn.commit()
    finally:
        conn.close()

# ---------- Delete ----------
def delete_set(set_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sets WHERE id = ?',
                       (set_id,)) # the , makes this a tuple because every '?' must be matched with a value in a tuple
        conn.commit()
    finally:
        conn.close()

def delete_workout(workout_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM workouts WHERE id = ?',
                       (workout_id,))
        conn.commit()
    finally:
        conn.close()

# ---------- Retrieve ----------
# No commit is needed here as rows are fetched before closing the connection.

def get_exercises():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exercises ORDER BY muscle_group, name')
    exercises = cursor.fetchall()
    conn.close()
    return exercises

def get_workouts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts ORDER BY date DESC, id DESC')
    workouts = cursor.fetchall()
    conn.close()
    return workouts

def get_workout_sets(workout_id):
    # JOIN grabs the exercise name from the exercises table so users see names, not random id numbers
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.workout_id, s.exercise_id, s.weight, s.reps, e.name
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.id
        WHERE s.workout_id = ?
        ORDER BY s.id
    ''', (workout_id,))
    sets = cursor.fetchall()
    conn.close()
    return sets


def get_max_lift(exercise_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.workout_id, s.exercise_id, s.weight, s.reps, e.name, w.date
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.id
        JOIN workouts w ON s.workout_id = w.id
        WHERE e.name = ?
        ORDER BY s.weight DESC, w.date DESC LIMIT 1''',(exercise_name,))
    maxs = cursor.fetchone()
    conn.close()
    # Returns one row, or None if this exercise has no sets. main.py does the formatting.
    return maxs

def get_last_session(exercise_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.workout_id, s.exercise_id, s.weight, s.reps, e.name, w.date
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.id
        JOIN workouts w ON s.workout_id = w.id
        WHERE e.name = ?
          AND s.workout_id = (
              -- subquery: the most recent workout containing this exercise
              -- (workouts.id breaks ties when two workouts share a date)
              SELECT w2.id
              FROM sets s2
              JOIN exercises e2 ON s2.exercise_id = e2.id
              JOIN workouts w2 ON s2.workout_id = w2.id
              WHERE e2.name = ?
              ORDER BY w2.date DESC, w2.id DESC LIMIT 1
          )
        ORDER BY s.id''',(exercise_name, exercise_name))
    last_session = cursor.fetchall()
    conn.close()
    # Returns a list of every set from that workout;
    return last_session

def get_personal_records():
    # Heaviest weight ever lifted for each exercise
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.name, MAX(s.weight) AS pr
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.id
        GROUP BY e.name
        ORDER BY e.name''')
    records = cursor.fetchall()
    conn.close()
    return records

