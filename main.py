import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import pyjokes
import streamlit as st

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Global flag to check if the engine is speaking
is_speaking = False

# Define the global stop_flag variable
if 'stop_flag' not in st.session_state:
    st.session_state.stop_flag = False

# Define the speak function
def speak(audio):
    global is_speaking
    if not is_speaking:
        try:
            is_speaking = True
            engine.say(audio)
            engine.runAndWait()
        except RuntimeError:
            pass
        finally:
            is_speaking = False

# Define the wish time function
def wish_time():
    x = st.session_state['name']  # Get the user's name from the session state
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 6:
        speak('Good night! Sleep tight.')
    elif 6 <= hour < 12:
        speak('Good morning!')
    elif 12 <= hour < 18:
        speak('Good afternoon!')
    else:
        speak('Good evening!')
    speak(f"{x}, how can I help you?")

# Function to take command from the microphone
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say something")
        recognizer.pause_threshold = 0.8
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio, language='en-in')
        st.write(f"You said: {query}")
    except Exception as e:
        st.write("Could not recognize. Please try again.")
        return "None"
    return query

# Function to perform tasks based on the command
def perform_task():
    query = take_command().lower()
    
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            st.write(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak(f"Multiple meanings found for '{query}'. Please be specific.")
        except wikipedia.exceptions.PageError:
            speak(f"'{query}' does not match any Wikipedia page.")
    
    elif 'play' in query:
        song = query.replace('play', "")
        speak(f"Searching YouTube for {song}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")
    
    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")
    
    elif 'search' in query:
        search_query = query.replace('search', '')
        speak(f"Searching Google for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    
    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")
    
    elif 'open code' in query:
        code_path = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(code_path)
    
    elif 'joke' in query:
        speak(pyjokes.get_joke())
    
    elif "where is" in query:
        location = query.replace("where is", "")
        speak(f"Locating {location}")
        webbrowser.open(f"https://www.google.com/maps/place/{location.replace(' ', '+')}")
    
    elif 'exit' in query:
        speak("Exiting now.")
        st.session_state.stop_flag = True

# Function to start the voice assistant
def start_voice_assistant():
    wish_time()
    while not st.session_state.stop_flag:
        perform_task()

# Main function to run the Streamlit app
def main():
    st.title("Voice Assistant")

    # Input to get user's name
    if 'name' not in st.session_state:
        st.session_state['name'] = st.text_input("Enter Your Name")

    # Button to start the voice assistant
    if st.button("Start Voice Assistant"):
        st.session_state.stop_flag = False
        start_voice_assistant()

    # Button to stop the voice assistant
    if st.button("Stop Voice Assistant"):
        st.session_state.stop_flag = True

if __name__ == "__main__":
    main()
