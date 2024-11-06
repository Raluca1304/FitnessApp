import random
import streamlit as st
from yt_extractor import get_info
import database_service as dbs


@st.cache_data
def get_workouts():
    return dbs.get_all_workouts()

def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text

st.title("Workout APP")

menu_options = ("Today's workout", "All workouts", "Add workout", "Favorite workouts")
selection = st.sidebar.selectbox("Menu", menu_options)

if selection == "All workouts":
    st.markdown("## All workouts")

    workouts = get_workouts()

    # Obțin lista unică de canale și durate
    channels = list(set(wo['chanel'] for wo in workouts))
    durations = ["< 5 min", "5-10 min", "10-20 min", "> 20 min"]

    # Filtrare după durată
    selected_duration = st.selectbox("Filter by duration", ["All durations"] + durations)

    # Aplică filtrul de durată
    if selected_duration != "All durations":
        if selected_duration == "< 5 min":
            workouts = [wo for wo in workouts if wo['duration'] < 300]
        elif selected_duration == "5-10 min":
            workouts = [wo for wo in workouts if 300 <= wo['duration'] <= 600]
        elif selected_duration == "10-20 min":
            workouts = [wo for wo in workouts if 600 < wo['duration'] <= 1200]
        elif selected_duration == "> 20 min":
            workouts = [wo for wo in workouts if wo['duration'] > 1200]

    # Afișare antrenamente
    if workouts:
        for idx, wo in enumerate(workouts):
            url = "https://youtu.be/" + wo["video_id"]
            st.text(wo['title'])
            st.text(f"{wo['chanel']} - {get_duration_text(wo['duration'])}")
            st.video(url)

            # Verifică dacă antrenamentul este deja favorit
            is_favorite = wo.get('is_favorite', False)
            favorite_button_text = "Remove from Favorite" if is_favorite else "Mark as Favorite"

            # Buton pentru marcarea ca favorit
            if st.button(favorite_button_text, key=f"fav_{wo['video_id']}_{idx}"):
                dbs.mark_as_favorite(wo["video_id"], not is_favorite)
                st.success(f"Updated favorite status for {wo['title']}!")
                st.cache_data.clear()

            # Buton pentru ștergere
            if st.button('Delete workout', key=f"del_{wo['video_id']}_{idx}"):
                dbs.delete_workout(wo["video_id"])
                st.cache_data.clear()

    else:
        st.text("No workouts found with the selected filters!")


elif selection == "Add workout":
    st.markdown(f"## Add workout")
    
    url = st.text_input('Please enter the video URL')
    if url:
        workout_data = get_info(url)
        if workout_data is None:
            st.text("Could not find video")
        else:
            st.text(workout_data['title'])
            st.text(workout_data['chanel']) 
            st.video(url)
            if st.button("Add workout"):
                dbs.insert_workout(workout_data)
                st.text("Added workout!")
                st.cache_data.clear()
                
else:
    st.markdown(f"## Today's workout")
    
    workout_today = dbs.get_workouts_today()
    
    if workout_today:
        wo = workout_today
        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo['title'])
        st.text(f"{wo['chanel']} - {get_duration_text(wo['duration'])}")
        st.video(url)
        
        if st.button("Choose another workout"):
            workouts = get_workouts()
            if workouts:
                new_wo = random.choice(workouts)
                while new_wo['video_id'] == wo['video_id']:
                    new_wo = random.choice(workouts)
                dbs.update_workout_today(new_wo)
    else:
        workouts = get_workouts()
        if workouts:
            wo = random.choice(workouts)
            dbs.update_workout_today(wo, insert=True)
            url = "https://youtu.be/" + wo["video_id"]
            st.text(wo['title'])
            st.text(f"{wo['chanel']} - {get_duration_text(wo['duration'])}")
            st.video(url)
        else:
            st.text("No workouts in Database!")
