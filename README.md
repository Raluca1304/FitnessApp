# Workout APP

**Workout APP** is a Streamlit application for managing and viewing workout videos. The app uses a database to save workout details, including favorite videos and today's selected workout.

---

## Features

1. **Main Menu**  
   In the sidebar, users can choose from the following options:
   - **Today's workout**: displays the workout selected for the current day, with an option to choose another.
   - **All workouts**: lists all workouts saved in the database, with filtering options by duration and favorite status management.
   - **Add workout**: allows users to add a new workout by entering a YouTube video URL.
   - **Favorite workouts**: (future functionality) could display a list of marked favorite workouts.

2. **Workout Management**  
   Users can view details for each workout, including the title, YouTube channel, duration, and can watch the video within the app.

3. **Button Functionality**
   - **Mark as Favorite / Remove from Favorite**: marks or unmarks a workout as a favorite.
   - **Delete workout**: deletes the selected workout from the database.

4. **Adding Workouts**  
   In the *Add workout* section, users can add a new workout using a YouTube URL. After retrieving the video information, users can click **Add workout** to save it to the database.

---

## Database Details

The app uses functions from `database_service.py` to perform operations on a MySQL database:
- **The `workouts` table** stores all workouts, with details like title, channel, video duration, and favorite status.
- **The `workout_today` table** keeps track of the workout selected for the current day.

---


## Requirements

- **Streamlit**: for the user interface.
- **yt_dlp**: for extracting video information from YouTube.
- **MySQL**: for storing workout data.

