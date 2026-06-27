import tkinter as tk
from tkinter import filedialog, ttk
import pyttsx3
import pytesseract
from PIL import Image
import config
import threading

if config.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

class DyslexiaReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dyslexia Assistive Reader Pro")
        self.root.geometry("1000x650")
        self.root.configure(bg=config.DEFAULT_BG)
        
        self.is_speaking = False
        
        self.setup_ui()

    def setup_ui(self):
        # Left Control Panel Sidebar
        self.sidebar = tk.Frame(self.root, width=260, bg="#EAECEE", relief=tk.SUNKEN, bd=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Typography Settings
        tk.Label(self.sidebar, text="Typography Settings", font=("Arial", 11, "bold"), bg="#EAECEE").pack(pady=(15,5))
        
        tk.Label(self.sidebar, text="Select Font:", bg="#EAECEE").pack(pady=(5,2))
        self.font_var = tk.StringVar(value=config.DEFAULT_FONT)
        self.font_dropdown = ttk.Combobox(self.sidebar, textvariable=self.font_var, values=config.FONTS, state="readonly")
        self.font_dropdown.pack(pady=5)
        self.font_dropdown.bind("<<ComboboxSelected>>", self.update_text_style)

        tk.Label(self.sidebar, text="Font Size:", bg="#EAECEE").pack(pady=(5,2))
        self.size_slider = tk.Scale(self.sidebar, from_=14, to=38, orient=tk.HORIZONTAL, command=self.update_text_style, bg="#EAECEE", bd=0)
        self.size_slider.set(config.DEFAULT_SIZE)
        self.size_slider.pack(pady=5, fill=tk.X, padx=20)

        # Document Ingestion
        tk.Label(self.sidebar, text="Document Ingestion", font=("Arial", 11, "bold"), bg="#EAECEE").pack(pady=(20,5))
        tk.Button(self.sidebar, text="Upload Image (OCR)", command=self.upload_image, bg="#34495E", fg="white", relief=tk.FLAT).pack(fill=tk.X, padx=20, pady=5)
        
        # Audio Engine Controls
        tk.Label(self.sidebar, text="Assistive Audio Engine", font=("Arial", 11, "bold"), bg="#EAECEE").pack(pady=(20,5))
        self.play_button = tk.Button(self.sidebar, text="▶ Read & Track", command=self.start_read_thread, bg="#27AE60", fg="white", relief=tk.FLAT)
        self.play_button.pack(fill=tk.X, padx=20, pady=5)

        # Right Text Workspace Panel
        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg=config.DEFAULT_BG, fg=config.DEFAULT_FG, padx=30, pady=30, insertbackground=config.DEFAULT_FG, bd=0)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Highlighting tag configuration
        self.text_area.tag_config("highlight", background=config.HIGHLIGHT_BG, foreground="#000000")
        
        self.text_area.insert(tk.END, "Paste text here or load a document image file. Click 'Read & Track' to watch the visual focus engine follow each spoken word.")
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
                self.text_area.insert(tk.END, extracted_text.strip())
            except Exception as e:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, f"Error processing image OCR: {str(e)}")

    def start_read_thread(self):
        if not self.is_speaking:
            # Safely capture the text data on the main thread before launching the background process
            raw_text = self.text_area.get("1.0", tk.END).strip()
            
            if raw_text:
                self.is_speaking = True
                self.play_button.config(state=tk.DISABLED)
                
                audio_thread = threading.Thread(target=self.speech_tracking_loop, args=(raw_text,), daemon=True)
                audio_thread.start()

    def speech_tracking_loop(self, text_to_speak):
        engine = pyttsx3.init()
        
        def on_word(name, location, length):
            start_idx = f"1.0 + {location} chars"
            end_idx = f"1.0 + {location + length} chars"
            self.root.after(0, lambda: self.apply_ui_highlight(start_idx, end_idx))

        def on_end(name, completed):
            self.root.after(0, self.reset_audio_interface_state)

        engine.connect('started-word', on_word)
        engine.connect('finished-utterance', on_end)
        
        engine.say(text_to_speak)
        engine.runAndWait()

    def apply_ui_highlight(self, start_idx, end_idx):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        self.text_area.tag_add("highlight", start_idx, end_idx)
        self.text_area.see(start_idx)

    def reset_audio_interface_state(self):
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        self.is_speaking = False
        self.play_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DyslexiaReaderApp(root)
    root.mainloop()