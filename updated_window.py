import tkinter as tk
import openai
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr

from chat_history import add_question_to_history
from chat_history import add_answer_to_history

# Set your OpenAI API key here
openai.api_key = "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"

# List of previous message history NOT USED YET.
session_chat_history = []

# Generates reponse using previous chat messages, and the user question.
def generate_response(previous_messages, question):
    prompt = ""
    # Adds past messages to prompt.
    for message in previous_messages:
        prompt += f"{message['author']}: {message['text']}\n"

    # Adds new user question to end of prompt.
    prompt += f"You: {question}\nAI:"

    # Generates reponse from GPT-3 API.
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )

    # Gets the chatBot reply from the openAI data structure data retuned from the API call.
    # Obtains text reponse in choices dictionary.
    answer = response.choices[0].text.strip()
    # Returns text reponse.
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

    # Display most recent messages, with updated question and reponse.
    for message in session_chat_history:
        output.insert(tk.END, f"{message['author']}: {message['text']}\n\n")
    output.config(state="disabled")

    # Moves output text to most recent reply on the bottom.
    output.yview_moveto(1.0)


def record_audio():
    fs = 44100
    duration = 5  # seconds
    filename = "recording.wav"
    print("Recording...")
    my_recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, my_recording, fs)

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        print("Transcribing...")
        audio_text = r.record(source)
    try:
        text = r.recognize_google(audio_text)
        print(text)
        entry.insert(tk.END, text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def clear_history(output, previous_messages):
    # Clears previous messages from Text output section on window.
    output.config(state="normal")
    output.delete("1.0", tk.END)  

    # Clears message history list.
    previous_messages.clear()
    output.config(state="disabled")


# Global tk window objects.
window = tk.Tk()

entry = tk.Entry(window, width=50, font=("Arial", 14))
entry.grid(pady=5, row=2, column=0, columnspan=3)
entry.bind("<Return>", lambda event: get_response())

output = tk.Text(window,
                 width=50,
                 height=10,
                 font=("Arial", 14),
                 bg="#44475a",
                 fg="white",
                 wrap="word",
                 state="disabled")
output.grid(pady=5, row=0, column=0, columnspan=3)
# output.pack(pady=10)


def main():
    window.title("SpeakGPT")
    window.geometry("412x350")
    window.resizable(False, False)
    window.configure(bg="#292d3e")

    label = tk.Label(window,
                     text="Ask me anything!",
                     font=("Arial", 16),
                     bg="#292d3e",
                     fg="white")
    label.grid(pady=5, row=1, column=0, columnspan=3)
    entry.grid(pady=5, row=4, column=0, columnspan=3)
    # label.pack(pady=20)
    # entry.pack(pady=10)

    ask_button = tk.Button(window, text="Ask", font=("Arial", 14), command=get_response)
    # ask_button.pack(side="bottom", pady=10)

    clear_button = tk.Button(window, text="Clear", font=("Arial", 14), command=lambda: clear_history(output, session_chat_history))
    # clear_button.pack(side="bottom", pady=10)

    record_button = tk.Button(window, text="Record", font=("Arial", 14), command=record_audio)
    # record_button.pack(side="bottom", pady=10)

    ask_button.grid(row=5, column=2, pady=5)
    clear_button.grid(row=5, column=1, pady=5)
    record_button.grid(row=5, column=0, pady=5)

    window.eval('tk::PlaceWindow . center')
    window.mainloop()


if __name__ == "__main__":
    main()
