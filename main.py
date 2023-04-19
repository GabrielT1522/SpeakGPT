import tkinter as tk
import openai
import sounddevice as sd
import speech_recognition as sr

# Set your OpenAI API key here
openai.api_key = "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"

#   List of previous message history NOT USED YET.
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


def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as stream:
        print("Recording...")
        audio = r.listen(stream)
    # recognize speech using Sphinx
    try:
        print("Transcribing...")
        text = r.recognize_sphinx(audio)
        print(text)
        entry.insert(tk.END, text)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

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

    button = tk.Button(window,
                       text="Ask",
                       command=get_response,
                       font=("Arial", 14),
                       bg="#44475a",
                       fg="black",
                       activebackground="#6272a4",
                       activeforeground="red")
    button.pack(pady=10)

    record_button = tk.Button(window,
                              text="Record Audio",
                              command=record_audio,
                              font=("Arial", 14),
                              bg="#44475a",
                              fg="black",
                              activebackground="#6272a4",
                              activeforeground="red")
    record_button.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    main()
