import tkinter as tk
from tkinter import ttk, filedialog
import os

class Dashboard:
    def __init__(self, master, run_process_callback):
        self.master = master
        master.title("LipSync Studio Dashboard")
        self.run_process_callback = run_process_callback

        # Input Section
        self.input_frame = ttk.LabelFrame(master, text="Inputs")
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.costume_path = tk.StringVar()

        self.create_file_input(self.input_frame, "Video (base.mp4)", self.video_path)
        self.create_file_input(self.input_frame, "Audio (new.wav)", self.audio_path)
        self.create_file_input(self.input_frame, "Costume (costume.jpg)", self.costume_path)

        # TTS/Cloning Section
        self.tts_frame = ttk.LabelFrame(master, text="TTS/Cloning")
        self.tts_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.tts_text = tk.StringVar()
        ttk.Label(self.tts_frame, text="TTS Text:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.tts_frame, textvariable=self.tts_text, width=30).grid(row=0, column=1)

        self.sample_path = tk.StringVar()
        self.create_file_input(self.tts_frame, "Voice Sample (sample.wav)", self.sample_path)

        self.language = tk.StringVar(value="en")
        ttk.Label(self.tts_frame, text="Language:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(self.tts_frame, textvariable=self.language, values=["en", "es", "fr"]).grid(row=2, column=1)

        self.emotion = tk.DoubleVar(value=0.5)
        ttk.Label(self.tts_frame, text="Emotion:").grid(row=3, column=0, sticky="w")
        ttk.Scale(self.tts_frame, variable=self.emotion, from_=0, to=1, orient="horizontal").grid(row=3, column=1)

        # Output Settings
        self.output_frame = ttk.LabelFrame(master, text="Output Settings")
        self.output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.output_dir = tk.StringVar(value="output/")
        ttk.Label(self.output_frame, text="Output Directory:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.output_frame, textvariable=self.output_dir, width=30).grid(row=0, column=1)

        # Advanced Options
        self.advanced_frame = ttk.LabelFrame(master, text="Advanced Options")
        self.advanced_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.real_time_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.advanced_frame, text="Real-Time Mode", variable=self.real_time_mode).grid(row=0, column=0, sticky="w")

        self.angle_mode = tk.StringVar(value="Front")
        ttk.Label(self.advanced_frame, text="Angle Mode:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(self.advanced_frame, textvariable=self.angle_mode, values=["Front", "Side", "3/4"]).grid(row=1, column=1)

        self.auto_background_button = ttk.Button(self.advanced_frame, text="Auto-Background", command=self.auto_background)
        self.auto_background_button.grid(row=2, column=0, pady=5)

        # Status
        self.status_label = ttk.Label(master, text="Ready")
        self.status_label.grid(row=4, column=0, pady=10)

        # Run Button
        self.run_button = ttk.Button(master, text="Run", command=self.run_process)
        self.run_button.grid(row=5, column=0, pady=20)
    
    def create_file_input(self, parent, label_text, var):
        ttk.Label(parent, text=label_text).grid(sticky="w")
        entry = ttk.Entry(parent, textvariable=var, width=30)
        entry.grid(sticky="w")
        button = ttk.Button(parent, text="Browse", command=lambda: self.browse_file(var))
        button.grid(sticky="w")

    def browse_file(self, var):
        file_path = filedialog.askopenfilename()
        var.set(file_path)

    def auto_background(self):
        self.update_status("Generating Background...")
        print("Auto-Background generation initiated.")
        self.update_status("Ready")

    def run_process(self):
        self.update_status("Processing...")
        self.run_process_callback(
            self.video_path.get(),
            self.audio_path.get(),
            self.costume_path.get(),
            self.tts_text.get(),
            self.sample_path.get(),
            self.language.get(),
            self.emotion.get(),
            self.output_dir.get(),
            self.real_time_mode.get(),
            self.angle_mode.get(),
        )
        self.update_status("Done!")
    
    def update_status(self, status):
        self.status_label.config(text=status)
        self.master.update_idletasks()