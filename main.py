import tkinter as tk
from tkinter import filedialog, ttk
import pyttsx3
import pytesseract
from PIL import Image
import config

if config.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

class DyslexiaReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dyslexia Assistive Reader")
        self.root.geometry("900x600")
        self.root.configure(bg=config.DEFAULT_BG)
        self.tts_engine = pyttsx3.init()
        self.setup_ui()

    def setup_ui(self):
        self.sidebar = tk.Frame(self.root, width=250, bg="#EAECEE", relief=tk.SUNKEN, bd=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.sidebar, text="Select Font:", bg="#EAECEE").pack(pady=(10,2))
        self.font_var = tk.StringVar(value=config.DEFAULT_FONT)
        self.font_dropdown = ttk.Combobox(self.sidebar, textvariable=self.font_var, values=config.FONTS, state="readonly")
        self.font_dropdown.pack(pady=5)
        self.font_dropdown.bind("<<ComboboxSelected>>", self.update_text_style)

        tk.Label(self.sidebar, text="Font Size:", bg="#EAECEE").pack(pady=(10,2))
        self.size_slider = tk.Scale(self.sidebar, from_=12, to=36, orient=tk.HORIZONTAL, command=self.update_text_style)
        self.size_slider.set(config.DEFAULT_SIZE)
        self.size_slider.pack(pady=5)

        tk.Label(self.sidebar, text="Actions:", bg="#EAECEE").pack(pady=(20,2))
        tk.Button(self.sidebar, text="Upload Image (OCR)", command=self.upload_image).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.sidebar, text="Read Aloud", command=self.read_aloud).pack(fill=tk.X, padx=20, pady=5)

        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg=config.DEFAULT_BG, fg=config.DEFAULT_FG, padx=20, pady=20, insertbackground=config.DEFAULT_FG)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.text_area.insert(tk.END, "Paste your text here or upload an image to begin reading smoothly.")
        self.update_text_style()

    def update_text_style(self, *args):
        chosen_font = self.font_var.get()
        chosen_size = self.size_slider.get()
        self.text_area.configure(font=(chosen_font, chosen_size))

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            try:
                img = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(img)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, extracted_text)
            except Exception as e:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, f"Error processing image OCR: {str(e)}")

    def read_aloud(self):
        text_content = self.text_area.get("1.0", tk.END).strip()
        if text_content:
            self.tts_engine.say(text_content)
            self.tts_engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = DyslexiaReaderApp(root)
    root.mainloop()