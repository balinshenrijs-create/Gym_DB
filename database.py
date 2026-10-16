import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "gym.db")

def run_query(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_data(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def init_db():
    run_query('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    muscle_group VARCHAR(100)
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_name VARCHAR(255),
                    workout_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS workout_sets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_id INTEGER NOT NULL,
                    exercise_id INTEGER NOT NULL,
                    set_number INTEGER NOT NULL,
                    weight_kg INTEGER,
                    reps INTEGER,
                    rest_seconds INTEGER,
                    FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE,
                    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS personal_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    exercise_id INTEGER NOT NULL,
                    weight_kg INTEGER,
                    reps INTEGER,
                    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS meal_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    meal_name VARCHAR(255),
                    calories INTEGER,
                    protein_g INTEGER,
                    carbs_g INTEGER,
                    fats_g INTEGER,
                    logged_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    height_cm INTEGER,
                    target_weight_kg INTEGER,
                    fitness_goals TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')
    
    run_query('''CREATE TABLE IF NOT EXISTS body_measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    weight_kg INTEGER,
                    body_fat_pct INTEGER,
                    chest_cm INTEGER,
                    waist_cm INTEGER,
                    hips_cm INTEGER,
                    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')