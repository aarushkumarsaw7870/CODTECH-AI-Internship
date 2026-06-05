import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
import threading

class SpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Advanced AI Dual-Language Speech Tool")
        self.root.geometry("650x550")
        self.root.configure(bg="#1e1e1e")

        # Title Label
        self.title_label = tk.Label(root, text="AI Hindi & English Speech Converter", font=("Arial", 18, "bold"), fg="#00ffd2", bg="#1e1e1e")
        self.title_label.pack(pady=15)

        # Status Label
        self.status_label = tk.Label(root, text="Status: Ready (Hindi + English Auto Detection)", font=("Arial", 12, "bold"), fg="#ffffff", bg="#1e1e1e")
        self.status_label.pack(pady=5)

        # Buttons Frame
        self.btn_frame = tk.Frame(root, bg="#1e1e1e")
        self.btn_frame.pack(pady=10)

        # Start Mic Button
        self.start_btn = tk.Button(self.btn_frame, text="🎙️ Start Listening", font=("Arial", 11, "bold"), bg="#00ffd2", fg="#1e1e1e", activebackground="#00c8a5", padx=15, pady=6, command=self.start_listening_thread, bd=0)
        self.start_btn.grid(row=0, column=0, padx=10)

        # Save Button
        self.save_btn = tk.Button(self.btn_frame, text="💾 Save to File", font=("Arial", 11, "bold"), bg="#ffb703", fg="#1e1e1e", activebackground="#fb8500", padx=15, pady=6, command=self.save_file, bd=0)
        self.save_btn.grid(row=0, column=1, padx=10)

        # Clear Button
        self.clear_btn = tk.Button(self.btn_frame, text="🗑️ Clear Text", font=("Arial", 11, "bold"), bg="#e63946", fg="#ffffff", activebackground="#d62828", padx=15, pady=6, command=self.clear_text, bd=0)
        self.clear_btn.grid(row=0, column=2, padx=10)

        # Text Area to show output
        self.text_area = tk.Text(root, font=("Arial", 13), wrap=tk.WORD, bg="#2d2d2d", fg="#ffffff", insertbackground="white", bd=0, padx=12, pady=12)
        self.text_area.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)

        self.recognizer = sr.Recognizer()

    def start_listening_thread(self):
        threading.Thread(target=self.listen_speech, daemon=True).start()

    def listen_speech(self):
        self.start_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: 🔊 Listening... Speak in Hindi or English!", fg="#00ffd2")
        
        try:
            with sr.Microphone() as source:
                # Better micro-filtration for clean voice response
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                
                # Listening configuration
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=12)
                self.status_label.config(text="Status: ⏳ Auto-detecting and converting...", fg="#ffb703")
                
                # CRITICAL: Dual-language setup done here (Hindi first, then English India accent)
                text = self.recognizer.recognize_google(audio, language="hi-IN,en-IN")
                
                self.text_area.insert(tk.END, text + " \n")
                self.status_label.config(text="Status: ✅ Successfully Converted!", fg="#00ffd2")
                
        except sr.UnknownValueError:
            self.status_label.config(text="Status: ❌ Voice not clear. Please speak clearly!", fg="#e63946")
        except sr.WaitTimeoutError:
            self.status_label.config(text="Status: ❌ Timeout - No voice detected!", fg="#e63946")
        except Exception as e:
            self.status_label.config(text="Status: ❌ Microphone issue or busy!", fg="#e63946")
        
        self.start_btn.config(state=tk.NORMAL)

    def save_file(self):
        text_content = self.text_area.get("1.0", tk.END).strip()
        if not text_content:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_content)
            self.status_label.config(text="Status: 💾 File saved successfully!", fg="#00ffd2")

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.status_label.config(text="Status: Text cleared", fg="#ffffff")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechApp(root)
    root.mainloop()