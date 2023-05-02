import tkinter as tk

import openai
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr

# Set your OpenAI API key here
openai.api_key = "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"

# List of previous message history
session_chat_history = []

# Generates response using previous chat messages, and the user question.
def generate_response(previous_messages, question):
    prompt = ""
    # Adds past messages to prompt.
    for message in previous_messages:
        prompt += f"{message['author']}: {message['text']}\n"

    # Adds new user question to end of prompt.
    prompt += f"You: {question}\nAI:"

    # Generates response from GPT-3 API.
    response = openai.Completion.create(
        # Set GPT-3 engine.
        engine="davinci",
        # Set prompt.
        prompt=prompt,
        # Set temperature (randomness, creativity) of generated text, higher is more random and less predictable.
        temperature=0.4,
        # Set max number of tokens (words) the model generates.
        max_tokens=1024,
        # Set P diversity of generated text.
        top_p=1,
        # Set penalty for generating same word multiple times.
        frequency_penalty=0.6,
        # Set penalty for generating words not present in prompt.
        presence_penalty=0.2,
        # Stops generating when it encounters character in stop.
        stop=["\n"]
    )

    # Gets the reply from the openAI data structure data returned from the API call.
    # Obtains text response in choices dictionary.
    answer = response.choices[0].text.strip()
    # Returns text response.
    return answer


def get_response():
    # Gets text from entry.
    question = entry.get()

    # Structures dictionary for question and appends to message history list.
    message = {"author": "You", "text": question}
    session_chat_history.append(message)

    # Structures dictionary for response and appends to message history list.
    response = generate_response(session_chat_history, question)
    message = {"author": "AI", "text": response}
    session_chat_history.append(message)

    # Clear previous messages.
    output.config(state="normal")
    output.delete("1.0", tk.END)

    # Display most recent messages, with updated question and response.
    for message in session_chat_history:
        output.insert(tk.END, f"{message['author']}: {message['text']}\n\n")
    output.config(state="disabled")

    # Moves output text to most recent reply on the bottom.
    output.yview_moveto(1.0)

    # Clear the contents of the entry
    entry.delete(0, tk.END)

# Not used due to latency in record_audio
def countdown():
    def count_down(seconds):
        if seconds > 0:
            timer.config(text=seconds)
            window.after(1000, count_down, seconds - 1)
        else:
            timer.config(text="")

    timer = tk.Label(window, font=("Arial", 14), fg="red")
    timer.grid(row=6, column=0, columnspan=3)

    # Start the timer
    count_down(5)

def record_audio():
    # Clear the contents of the entry
    entry.delete(0, tk.END)

    #countdown()

    # Record audio and transcribe it
    fs = 44100
    duration = 5  # seconds
    filename = "recording.wav"
    print("Recording...")
    record_label.config(text="Recording...")
    my_recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, my_recording, fs)

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        print("Transcribing...")
        record_label.config(text="Transcribing...")
        audio_text = r.record(source)
    try:
        text = r.recognize_google(audio_text)
        print(text)
        entry.insert(tk.END, text)
        record_label.config(text="Recording has a 5 second limit.", fg="white")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        record_label.config(text="Google Speech Recognition could not understand audio.", fg="red")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        record_label.config(text="Could not request results from Google Speech Recognition service; {0}".format(e), fg="red")



def clear_history(output, previous_messages):
    # Clears previous messages from Text output section on window.
    output.config(state="normal")
    output.delete("1.0", tk.END)

    # Clears message history list.
    previous_messages.clear()
    output.config(state="disabled")


# Global tk  objects.
window = tk.Tk()

entry = tk.Entry(window, width=50, font=("Arial", 14))
entry.bind("<Return>", lambda event: get_response())

output = tk.Text(window, width=50, height=10, font=("Arial", 14), bg="#44475a", fg="white", wrap="word", state="disabled")

clear_button = tk.Button(window, text="Clear", font=("Arial", 14), command=lambda: clear_history(output, session_chat_history))
ask_button = tk.Button(window, text="Ask", font=("Arial", 14), command=get_response)
record_button = tk.Button(window, text="Record", font=("Arial", 14), command=record_audio)

record_label = tk.Label(window, text="Recording has a 5 second limit.",font=("Arial", 10, "italic"),bg="#292d3e",fg="white")

def main():
    window.title("SpeakGPT")
    window.resizable(False, False)
    window.configure(bg="#292d3e")

    entry.grid(pady=5, row=2, column=0, columnspan=3)
    output.grid(pady=5, row=0, column=0, columnspan=3)

    label = tk.Label(window, text="Ask me anything!", font=("Arial", 16), bg="#292d3e", fg="white")
    label.grid(pady=5, row=1, column=0, columnspan=3)

    # Sets buttons on grid pos.
    clear_button.grid(row=5, column=0, pady=5)
    ask_button.grid(row=5, column=1, pady=5)
    record_button.grid(row=5, column=2, pady=5)

    record_label.grid(pady=5, row=6, column=0, columnspan=3)

    # Sets window on center of screen on start.
    window.eval('tk::PlaceWindow . center')
    window.mainloop()


if __name__ == "__main__":
    main()
