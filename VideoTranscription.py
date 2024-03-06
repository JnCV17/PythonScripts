#Video transcription to text using moviepy, speech_Recognition (free API and Online service), and tkinter for file choosing methods.
#Language is setted to spanish, for video calls transcription and laziness transcribing those calls.
#Might improve later

from moviepy.editor import VideoFileClip
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
import os

def choose_file():
    root = tk.Tk()

    # Hide the main window
    root.withdraw()  

    # Open file dialog and get selected file path
    file_path = filedialog.askopenfilename()  
    return file_path

def extract_audio_and_transcribe_in_batches(video_path, batch_duration):

    recognizer = sr.Recognizer()

    clip = VideoFileClip(video_path)
    total_duration = clip.duration
    print("Duración total de Video:", total_duration)
    
    start_time = 0
    end_time = batch_duration
    
    batch_number = 1

    output_file = os.path.dirname(video_path) + "/" + os.path.splitext(os.path.basename(video_path))[0] + ".txt"

    text = ""
    
    while start_time < total_duration:
        # Ensure end_time doesn't exceed total duration
        end_time = min(end_time, total_duration)
        
        # Extract audio for the current batch
        audio = clip.subclip(start_time, end_time).audio
        
        # Save audio to file
        audio_filename = f"batch_{batch_number}_audio.wav"
        audio.write_audiofile(audio_filename)
        
        print(f"Audio extraido - batch {batch_number}: {audio_filename}")

        with sr.AudioFile(audio_filename) as source:
            audio_duration = source.DURATION
            print("Duración de audio total:", audio_duration)

            audio1 = recognizer.record(source)
            
            try:
                # Recognize speech using Google Web Speech API
                text1 = recognizer.recognize_google(audio1, language="es-ES")
                
                #Store text transcribed for end file
                text += f"\n{text1}\n\n"

                #Print to check what is being transcribed
                #print(f"\n{text1}\n\n")
            except sr.UnknownValueError:
                print("\n\nGoogle Web Speech API no pudo reconocer el audio not understand audio")
            except sr.RequestError as e:
                print("\n\No se pudo obtener resultados del API de Google Web Speech; {0}".format(e))
        
        os.remove(audio_filename)

        # Move to the next batch
        #Due to the video being trimmed the start time is setted 10 secs back in case a word was cut
        start_time += batch_duration-20
        end_time = start_time + batch_duration
        batch_number += 1
    
    text_file = open(output_file, "w")
    text_file.write(text)
    text_file.close()
    clip.close()

if __name__ == "__main__":
    file_path = choose_file()
    if file_path:
        #Testing the API it worked fine with 100 secs, 200 secs had a weird behavior. Check later
        extract_audio_and_transcribe_in_batches(file_path, batch_duration=100)
    else:
        print("No selecciono archivos.")