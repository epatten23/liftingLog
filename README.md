# Overview

During this project, I wanted to learn how to build a relational database, and then use software to manipulate and display that data. I've been coding in Python for a while now, so I wanted to use a language I already knew for the software part, so I could focus on SQL itself.

This application is a lifting log that runs in the terminal and is able to store everything in a SQLite database. The user is able to log a workout after picking their menu item. They can then insert their exercise, weight, and rep foreach set. They can also switch between exercises partway through their workout or finish at any point. Past workouts can be reviewed, personal records are displayed, individual sets can be edited and deleted, and even new exercises can be added to the database. The database file and its tables are created automatically the first time, and the exercise list is seeded with twenty common lifts so a workout can be logged immediately.

My purpose in writing this software was to learn SQL by building something I'll actually need. I lift regularly and the two things I actually want to know at the gym are what my best lift was and what I did last time, so the queries the program runs are questions I ask anyway rather than ones invented to demonstrate a feature.

[Software Demo Video](https://youtu.be/hUnh72nTctY)

# Relational Database

The program uses SQLite, accessed through Python's built-in sqlite3 module. SQLite stores the entire database in a single file and needs no separate server or application.

The database has three tables:

**exercises** holds the catalog of lifts. Columns are id, name, muscle_group, and equipment.. 

**workouts** holds one row per session. Columns are id, date, and an optional notes field.

**sets** is the table that relates the other two. Columns are id, workout_id, exercise_id, weight, and reps. Each row is a single set performed, so one workout has many sets and one exercise appears in many sets. 

# Development Environment

I developed this software in Visual Studio Code and used Git for version control, publishing the project to GitHub. I used the SQLite command line shell to inspect the database directly while building the schema.

The program is written in Python and uses only the standard library: sqlite3 for all database access and datetime for validating and defaulting dates. No third-party packages are required.

# Useful Websites

- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [SQLite Tutorial - Inner Join](https://www.sqlitetutorial.net/sqlite-inner-join/)
- [SQLite - CREATE TABLE](https://www.sqlite.org/lang_createtable.html)

# Future Work

If I were to spend more time on this project, I would improve it by:
- Querying by exercise id instead of looking up the name first
- Adding a way to cancel a workout before the first set is logged, so choosing the menu option by mistake does not commit to logging something
- Adding a date range filter so I can see volume or progress over a chosen period
- Showing progress for a single exercise over time instead of only the single best set

# AI Disclosure

I used Claude as a learning and reference tool during this project. I recieved help to choose a project, learning the sqlite3 patterns before I wrote anything, and reviewing and debugging the finished code.

Claude helped me decide which project would help me in my day to day life while I still learned lots about SQL and joining tables. The three-table structure of exercises, workouts, and sets was suggested to me, I did some outside research on joins, and adopted that structure. AI also helped me decide column names and criteria for each table.

I also needed help with how to approach database code. AI gave me a couple different examples, with unrelated data, showing how the JOIN function works in SQL. It also walked me through a CREAT TABLE and other seeding. AI also helped me with example data, weights, and sets for my example data to start off with. AI explained how to use ? as placeholders in SQL. I was able to understand the examples and write my own tables. I received some help with the queries when it came to joining two tables together so I could grab the right information from the right column.

Separately, I asked how exception handling loops are written in Python compared to JavaScript, which I had used in a previous project. The validation helpers in main.py follow that pattern, rewritten for my own prompts and ranges.

After the program was working, AI helped me code review. It helped me refine my comments and pointed out some areas of improvement if given more time on the project. 

What I learned: I think my biggest takeaway was the SQL information. I truly understood how to create a table in a python program, and also how to update and retrieve that information from a database. I learned about subqueries and queries in general. AI helped me expand my knowledge about databases and implement one in a practical application.