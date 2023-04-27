import tkinter as tk
import openai
import soundfile as sf
import sounddevice as sd
import speech_recognition as sr

# Set your OpenAI API key here
openai.api_key = "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"

# List of previous message history NOT USED YET.
previous_messages = []

def generate_response(question):
    prompt = f"Q: {question}\nA:"
    response = openai.Completion.create(engine="davinci",
                                        prompt=prompt,
                                        temperature=0.7,
                                        max_tokens=1024,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0,
                                        stop=["\n"])
    answer = response.choices[0].text.strip()
    return answer

def get_response():
    question = entry.get()
    response = generate_response(question)

    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, response)
    output.config(state="disabled")
    entry.delete(0, tk.END)

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

window = tk.Tk()
entry = tk.Entry(window, width=50, font=("Arial", 14))
output = tk.Text(window,
                 width=50,
                 height=10,
                 font=("Arial", 14),
                 bg="#44475a",
                 fg="white",
                 state="disabled")
output.pack(pady=10)

def main():
    window.title("ChatGPT")
    window.geometry("600x400")
    window.configure(bg="#292d3e")

    label = tk.Label(window,
                     text="Ask me anything!",
                     font=("Arial", 16),
                     bg="#292d3e",
                     fg="white")
    label.pack(pady=20)

    entry.pack(pady=10)

    button = tk.Button(window, text="Ask", font=("Arial", 14), command=get_response)
    button.pack(pady=10)

    record_button = tk.Button(window, text="Record", font=("Arial", 14), command=record_audio)
    record_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
