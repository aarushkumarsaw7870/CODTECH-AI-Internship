import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import threading
import traceback

# Variable name simplified to avoid any spelling mismatch
LABELS = {
    817: "SPORTS CAR / RACING CAR",
    511: "CONVERTIBLE (CAR)",
    479: "CAR WHEEL / RIM",
    281: "TABBY CAT / PET",
    282: "TIGER CAT",
    504: "COFFEE MUG / CUP",
    968: "CUP / SAUCER"
}

class AdvancedImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Professional AI Image Analyzer (MobileNetV2)")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")

        # --- UI Layout Top Header ---
        self.header = tk.Label(root, text="🧠 DEEP LEARNING IMAGE CLASSIFIER", font=("Arial", 16, "bold"), bg="#1f1f1f", fg="#00ffd2", pady=12)
        self.header.pack(fill=tk.X)

        # Main Workspace Splitter
        self.main_frame = tk.Frame(root, bg="#121212")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Left Panel (Image Display)
        self.left_panel = tk.LabelFrame(self.main_frame, text=" Image Preview ", font=("Arial", 10, "bold"), bg="#121212", fg="#00ffd2", bd=1)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.image_label = tk.Label(self.left_panel, bg="#1e1e1e", text="No Image Selected\nClick 'Upload' to scan", font=("Arial", 11), fg="#888888")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right Panel (Analysis Breakdown)
        self.right_panel = tk.LabelFrame(self.main_frame, text=" AI Classification Breakdown ", font=("Arial", 10, "bold"), bg="#121212", fg="#00ffd2", bd=1, width=340)
        self.right_panel.pack_propagate(False)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        self.status_label = tk.Label(self.right_panel, text="Status: Initializing AI...", font=("Arial", 11, "bold"), fg="#ffb703", bg="#121212", anchor="w")
        self.status_label.pack(fill=tk.X, padx=15, pady=15)

        self.results_box = tk.Text(self.right_panel, bg="#1e1e1e", fg="#ffffff", font=("Courier New", 11), wrap=tk.WORD, bd=0, padx=10, pady=10, state=tk.DISABLED)
        self.results_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Bottom Control Bar
        self.controls = tk.Frame(root, bg="#1f1f1f", pady=10)
        self.controls.pack(fill=tk.X, side=tk.BOTTOM)

        self.upload_btn = tk.Button(self.controls, text="📁 Upload New Image", font=("Arial", 11, "bold"), bg="#00ffd2", fg="#1e1e1e", activebackground="#00c8a5", padx=20, pady=6, bd=0, command=self.process_image_thread)
        self.upload_btn.pack(side=tk.LEFT, padx=30)

        self.clear_btn = tk.Button(self.controls, text="🗑️ Reset Layout", font=("Arial", 11, "bold"), bg="#e63946", fg="#ffffff", activebackground="#d62828", padx=20, pady=6, bd=0, command=self.reset_all)
        self.clear_btn.pack(side=tk.RIGHT, padx=30)

        self.model_loaded = False
        threading.Thread(target=self.initialize_ai, daemon=True).start()

    def initialize_ai(self):
        try:
            self.model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
            self.model.eval()
            self.model_loaded = True
            self.status_label.config(text="Status: AI Model Active & Ready", fg="#00ffd2")
        except Exception:
            try:
                self.model = models.mobilenet_v2(pretrained=True)
                self.model.eval()
                self.model_loaded = True
                self.status_label.config(text="Status: AI Model Active (Fallback)", fg="#00ffd2")
            except Exception:
                self.status_label.config(text="Status: Critical Init Error", fg="#e63946")
                traceback.print_exc()

        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def process_image_thread(self):
        if not self.model_loaded:
            return
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            threading.Thread(target=self.analyze_core, args=(file_path,), daemon=True).start()

    def analyze_core(self, path):
        self.upload_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Analyzing features...", fg="#ffb703")
        
        try:
            img = Image.open(path).convert('RGB')
            
            img_disp = img.copy()
            img_disp.thumbnail((380, 380))
            self.tk_img = ImageTk.PhotoImage(img_disp)
            self.image_label.config(image=self.tk_img, text="")

            img_t = self.transform(img)
            batch_t = torch.unsqueeze(img_t, 0)

            with torch.no_grad():
                output = self.model(batch_t)
            
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            top3_prob, top3_raw_idx = torch.topk(probabilities, 3)

            report_card = "RANK    PREDICTED OBJECT      CONFIDENCE\n"
            report_card += "========================================\n"
            
            for rank, (prob, idx) in enumerate(zip(top3_prob, top3_raw_idx), 1):
                idx_val = idx.item()
                # Reading directly from the unique LABELS dictionary
                label = LABELS.get(idx_val, f"OBJECT CLASS {idx_val}")
                score = prob.item() * 100
                report_card += f"#{rank:<4}  {label:<20}  {score:.2f}%\n\n"

            self.results_box.config(state=tk.NORMAL)
            self.results_box.delete("1.0", tk.END)
            self.results_box.insert(tk.END, report_card)
            self.results_box.config(state=tk.DISABLED)

            self.status_label.config(text="Status: Analysis Complete ✅", fg="#00ffd2")

        except Exception as e:
            self.status_label.config(text="Status: Runtime Error", fg="#e63946")
            traceback.print_exc()

        self.upload_btn.config(state=tk.NORMAL)

    def reset_all(self):
        self.image_label.config(image='', text="No Image Selected\nClick 'Upload' to scan")
        self.results_box.config(state=tk.NORMAL)
        self.results_box.delete("1.0", tk.END)
        self.results_box.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Layout Reset. Ready.", fg="#ffffff")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedImageApp(root)
    root.mainloop()