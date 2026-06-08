import tkinter as tk
from tkinter import messagebox
import random
import re

class AIChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Advanced AI Rule-Based Chatbot")
        self.root.geometry("500x600")
        self.root.configure(bg="#121212") # Dark Mode for visual contrast

        # Intent aur Responses Dictionary (Rules)
        self.rules = {
            r'(hi|hello|hey|hey there|good morning|hello bhai)': [
                "Hello bhai! Main aapka AI assistant hoon. Kaise ho?",
                "Hey! Welcome. Main aapki kya madad kar sakta hoon?",
                "Namaste! AI Chatbot ready hai. Boliye kya help chahiye?"
            ],
            r'(how are you|kaise ho|tum kaise ho)': [
                "Main ekdum mast hoon bhai! Aap batao, aap kaise ho?",
                "I am doing great! Thanks for asking. Aapka din kaisa chal raha hai?",
                "Ekdum badiya! Aapki sewa me hazir hoon."
            ],
            r'(your name|tumhara naam|naam kya hai)': [
                "Mera naam AI Smart Bot hai, aur main aapka personal assistant hoon! 😎",
                "Mujhe CodTech AI Chatbot kehte hain!"
            ],
            r'(internship|codtech|task)': [
                "CodTech IT Solutions ki internship bohot badiya hai! Aap abhi Task 3 par kaam kar rahe hain. 👍",
                "Tasks complete karte jaiye aur GitHub par push karte rahiye. Aap seekh rahe hain!"
            ],
            r'(dhanbad|jharkhand|where do you live)': [
                "Dhanbad toh coal capital hai, bohot hi shaandar jagah hai! 🚂",
                "Jharkhand ke log bohot hardworking hote hain!"
            ],
            r'(bye|goodbye|exit|chalo bye)': [
                "Bye bhai! Apna khayal rakhna. Dobara jald milenge! 👋",
                "Alvida! Agli baar aur baatein karenge. Take care!"
            ],
            r'(thank you|thanks|shukriya)': [
                "You're welcome bhai! Mujhe khushi hui madad karke. 😊",
                "Anytime! Kuch aur poochna hai?"
            ]
        }

        # --- UI Design ---
        # Header Label
        self.header = tk.Label(root, text="🤖 CODTECH AI ASSISTANT", font=("Arial", 14, "bold"), bg="#1f1f1f", fg="#00ffd2", pady=10)
        self.header.pack(fill=tk.X)

        # Chat History Log Window (Scrollable Text)
        self.chat_log = tk.Text(root, bg="#1a1a1a", fg="#ffffff", font=("Arial", 11), wrap=tk.WORD, state=tk.DISABLED, bd=0, padx=10, pady=10)
        self.chat_log.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)
        
        # Welcoming message from Bot
        self.display_message("Bot: Hello bhai! Main CodTech AI Chatbot hoon. Kuch bhi likhiye...\n", "#00ffd2")

        # Input Frame (Neeche box aur button ke liye)
        self.input_frame = tk.Frame(root, bg="#121212")
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=15, padx=15)

        # Entry Box for typing
        self.entry_box = tk.Entry(self.input_frame, bg="#2d2d2d", fg="#ffffff", font=("Arial", 12), insertbackground="white", bd=0, width=32)
        self.entry_box.pack(side=tk.LEFT, ipady=8, padx=(0, 10), fill=tk.X, expand=True)
        self.entry_box.bind("<Return>", lambda event: self.send_message()) # Enter key configuration

        # Send Button
        self.send_btn = tk.Button(self.input_frame, text="Send 🚀", font=("Arial", 11, "bold"), bg="#00ffd2", fg="#1e1e1e", activebackground="#00c8a5", bd=0, padx=15, pady=6, command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

    def send_message(self):
        user_text = self.entry_box.get().strip()
        if not user_text:
            return

        # User ka message screen par dikhao
        self.display_message(f"You: {user_text}\n", "#ffffff")
        self.entry_box.delete(0, tk.END)

        # Bot ka response generate karo
        bot_response = self.generate_response(user_text)
        
        # Bot ka response thode delay ke baad insert hoga natural feel ke liye
        self.root.after(400, lambda: self.display_message(f"Bot: {bot_response}\n\n", "#ffb703"))

    def generate_response(self, text):
        user_input_clean = text.lower()
        
        # Rule check pipeline matching
        for pattern, responses in self.rules.items():
            if re.search(pattern, user_input_clean):
                return random.choice(responses)
                
        # Default response agar koi rule match na ho
        return random.choice([
            "Hmm, thoda dilchasp hai! Par mujhe is baare me zyada pata nahi hai. Kuch aur puchiye? 🤔",
            "Main abhi seekh raha hoon bhai, mujhe ye samajh nahi aaya. Kya aap thoda alag tarike se bol sakte hain?",
            "Accha! Mujhe iske baare me aur batayein, ya fir kuch aur baatein karein?"
        ])

    def display_message(self, msg, color):
        self.chat_log.config(state=tk.NORMAL)
        
        tag_name = str(random.random())
        self.chat_log.insert(tk.END, msg, tag_name)
        self.chat_log.tag_config(tag_name, foreground=color)
        
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END) # Scroll to the bottom automatically

if __name__ == "__main__":
    root = tk.Tk()
    app = AIChatbot(root)
    root.mainloop()