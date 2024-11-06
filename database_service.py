import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="200819RR",
            database="workout_repo"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

SCHEMA = "workout_repo"
TABLE = "workouts"
TABLE_TODAY = "workout_today"

def insert_workout(workout_data):
    connection = create_connection() 
    if connection:
        cursor = connection.cursor()
        query = f"INSERT INTO {TABLE} (video_id, chanel, title, duration, is_favorite) VALUES (%s, %s, %s, %s, %s)"
        values = (workout_data['video_id'], workout_data['chanel'], workout_data['title'], workout_data['duration'], False) # False for default non-favorite
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()  
    else:
        print("Error: Could not connect to the database.")

def mark_as_favorite(video_id, favorite=True):
    connection = create_connection() 
    if connection:
        cursor = connection.cursor()
        query = f"UPDATE {TABLE} SET is_favorite = %s WHERE video_id = %s"
        cursor.execute(query, (favorite, video_id))
        connection.commit()
        cursor.close()
        connection.close()  
    else:
        print("Error: Could not connect to the database.")

def get_favorite_workouts():
    connection = create_connection() 
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT video_id, chanel, title, duration FROM {TABLE} WHERE is_favorite = True"
        cursor.execute(query)
        workouts = cursor.fetchall()
        cursor.close()
        connection.close()  
        return workouts
    else:
        print("Error: Could not connect to the database.")
        return []

def delete_workout(workout_id):
    connection = create_connection()  
    if connection:
        cursor = connection.cursor()
        query = f"DELETE FROM {TABLE} WHERE video_id = %s"
        cursor.execute(query, (workout_id,))
        connection.commit()
        cursor.close()
        connection.close()  
    else:
        print("Error: Could not connect to the database.")

# Obtain all workouts from database
def get_all_workouts():
    connection = create_connection() 
    if connection:
        cursor = connection.cursor(dictionary=True) 
        query = f"SELECT video_id, chanel, title, duration FROM {TABLE}"
        cursor.execute(query)
        workouts = cursor.fetchall()
        cursor.close()
        connection.close()  
        return workouts
    else:
        print("Error: Could not connect to the database.")
        return []

# Obtain today workout
def get_workouts_today():
    connection = create_connection() 
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {TABLE_TODAY} WHERE id = 0"
        cursor.execute(query)
        workout_today = cursor.fetchone()
        cursor.close()
        connection.close()  
        return workout_today
    else:
        print("Error: Could not connect to the database.")
        return None

# Update today workout
def update_workout_today(workout_data, insert=False):
    connection = create_connection() 
    if connection:
        cursor = connection.cursor()
        workout_data['id'] = 0
        if insert:
            query = f"INSERT INTO {TABLE_TODAY} (id, video_id, chanel, title, duration) VALUES (%s, %s, %s, %s, %s)"
            values = (workout_data['id'], workout_data['video_id'], workout_data['chanel'], workout_data['title'], workout_data['duration'])
            cursor.execute(query, values)
        else:
            query = f"UPDATE {TABLE_TODAY} SET video_id = %s, chanel = %s, title = %s, duration = %s WHERE id = 0"
            values = (workout_data['video_id'], workout_data['chanel'], workout_data['title'], workout_data['duration'])
            cursor.execute(query, values)

        connection.commit()
        cursor.close()
        connection.close() 
    else:
        print("Error: Could not connect to the database.")
