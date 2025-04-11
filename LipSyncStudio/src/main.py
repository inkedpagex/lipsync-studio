import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from src.dashboard import Dashboard
from src.video_processor import extend_video, extract_frames, reassemble_video
from src.costume_swapper import process_video_costumes
from src.voice_generator import generate_audio
from src.lip_sync import sync_video
from src.advanced_features import add_emotion, render_multi_angle, generate_background
from config import *

class MainApp:
    def __init__(self, master):
        self.master = master
        master.title("LipSync Studio")
        self.dashboard = Dashboard(master, self.run_process)

    def run_process(self, video_path, audio_path, costume_path, tts_text, voice_sample, language, emotion, output_dir, real_time_mode, angle_mode):
        try:
            self.dashboard.update_status("Processing...")

            # Extend video
            extended_video_path = os.path.join(output_dir, "extended_video.mp4")
            extend_video(video_path, extended_video_path)

            # Extract frames
            frame_dir = "frames"
            os.makedirs(frame_dir, exist_ok=True)
            extract_frames(extended_video_path, frame_dir)

            # Costume swapping
            if costume_path:
                costume_frames_dir = "costume_frames"
                os.makedirs(costume_frames_dir, exist_ok=True)
                process_video_costumes(frame_dir, costume_path, costume_frames_dir)
                frame_dir = costume_frames_dir  # Update frame_dir to use costume-swapped frames

            # Voice generation
            generated_audio_path = os.path.join(output_dir, "generated_audio.wav")
            generate_audio(tts_text, voice_sample, language, emotion, generated_audio_path)

            # Lip sync and animation
            synced_video_path = os.path.join(output_dir, "synced_video.mp4")
            sync_video(frame_dir, generated_audio_path, synced_video_path)

            # Reassemble frames into a video
            final_video_path = os.path.join(output_dir, "final_video.mp4")
            reassemble_video(frame_dir, final_video_path, 30)
            
            # Add emotion
            if emotion != 0.5:
                add_emotion(final_video_path, emotion)
                
            #Multi angle
            if angle_mode != "Front":
                render_multi_angle(final_video_path, angle_mode)

            # Background
            generate_background(final_video_path)

            self.dashboard.update_status("Done!")
        except Exception as e:
            self.dashboard.update_status(f"Error: {e}")
            

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()