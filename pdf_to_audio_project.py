import pyttsx3
import PyPDF2
import threading
from googletrans import Translator
import tkinter as tk
from tkinter import filedialog

# Initialize the text-to-speech engine
pdf_speaker = pyttsx3.init()

# Set the speaking rate (adjust this value as needed)
pdf_speaker.setProperty('rate', 150)  # You can experiment with different values

# Function to set the voice to a female US English voice
def set_female_us_voice():
    voices = pdf_speaker.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower() and "female" in voice.name.lower() and "us" in voice.name.lower():
            pdf_speaker.setProperty('voice', voice.id)
            break

# Function to read the PDF, optionally translate, and speak
def read_pdf_translate_and_speak(pdf_path, page_num, translate_to=None):
    pdf_book = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_book)
    num_pages = len(pdf_reader.pages)  # Calculate the number of pages

    if 1 <= page_num <= num_pages:
        chosen_page = pdf_reader.pages[page_num - 1]
        pdf_text = chosen_page.extract_text()

        if translate_to == 'hi':
            # Save the Hindi text to an audio file using gTTS
            tts = gTTS(text=pdf_text, lang='hi')
            audio_path = 'output.mp3'
            tts.save(audio_path)

            # Play the audio file using the default media player
            import os
            os.system(f'start {audio_path}')
        else:
            # Set the voice to a female US English voice
            set_female_us_voice()

            # Start speaking the text using pyttsx3
            pdf_speaker.say(pdf_text)
            pdf_speaker.runAndWait()
    else:
        print("Invalid page number. Please choose a page within the specified range.")

    pdf_book.close()

# Function to listen for keyboard input and stop speech
def listen_for_keyboard_input():
    input("Press Enter to stop speaking...")

# Create a GUI window for file selection
root = tk.Tk()
root.withdraw()  # Hide the main window

# Allow the user to choose a PDF file
file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

# Allow the user to choose a page to read
while True:
    try:
        page_num = int(input("Enter the page number to read (1 - ?): "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid page number.")

# Allow the user to choose whether to translate the text
translate_option = input("Translate text to Hindi? (yes/no): ").strip().lower()
if translate_option == 'yes':
    translate_to = 'hi'
else:
    translate_to = None

# Create a thread to read, optionally translate, and speak the PDF
pdf_thread = threading.Thread(target=read_pdf_translate_and_speak, args=(file_path, page_num, translate_to))
pdf_thread.start()

# Create a thread to listen for keyboard input and stop speech
keyboard_thread = threading.Thread(target=listen_for_keyboard_input)
keyboard_thread.start()

# Wait for the speech thread to finish
pdf_thread.join()

# Wait for the keyboard input thread to finish
keyboard_thread.join()
