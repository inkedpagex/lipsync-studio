import cv2
import librosa
import numpy as np
import os
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
import math

def extend_video(input_video, output_video, audio_path):
    """Extends a video to match the duration of an audio file with fade transitions."""
    try:
        video_clip = VideoFileClip(input_video)
        audio_clip = AudioFileClip(audio_path)

        video_duration = video_clip.duration
        audio_duration = audio_clip.duration
        
        if audio_duration <= video_duration:
            video_clip.audio = audio_clip
            video_clip.write_videofile(output_video, fps=video_clip.fps, audio_codec='aac')
            video_clip.close()
            audio_clip.close()
            return

        num_loops = math.ceil(audio_duration / video_duration)

        clips = [video_clip]
        for _ in range(num_loops -1):
          clips.append(video_clip)

        final_clip = concatenate_videoclips(clips)
        final_clip = final_clip.subclip(0, audio_duration)

        fade_duration = 1  # Duration of fade in seconds
        
        video_with_audio_clip = final_clip.set_audio(audio_clip)

        video_with_audio_clip.write_videofile(output_video, fps=video_with_audio_clip.fps, audio_codec='aac')

        video_clip.close()
        audio_clip.close()
        video_with_audio_clip.close()
    except Exception as e:
      raise e

def extract_frames(video_path, frame_dir):
    """Splits a video into individual JPG frames."""
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_path = os.path.join(frame_dir, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    cap.release()
    return fps

def reassemble_video(frame_dir, output_video, fps):
    """Rebuilds a video from a directory of frames using FFmpeg."""
    if not os.path.exists(frame_dir):
        raise FileNotFoundError(f"Frame directory not found: {frame_dir}")

    frame_pattern = os.path.join(frame_dir, "frame_%04d.jpg")
    
    command = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", frame_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    
    subprocess.run(command, check=True)

def detect_pauses_and_freeze_frames(audio_path, frame_dir, output_frame_dir, silence_threshold=0.02, min_pause_duration=0.2, fps=30):
    """Detects pauses in audio and duplicates frames during silence."""
    
    if not os.path.exists(output_frame_dir):
        os.makedirs(output_frame_dir)

    y, sr = librosa.load(audio_path)
    
    intervals = librosa.effects.split(y, top_db=librosa.amplitude_to_db(silence_threshold))

    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".jpg")])
    
    frame_index = 0
    output_frame_index = 0
    
    for i, (start, end) in enumerate(intervals):
        
        start_time = librosa.samples_to_time(start, sr=sr)
        end_time = librosa.samples_to_time(end, sr=sr)
        duration = end_time - start_time

        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        
        for j in range(max(frame_index,start_frame), min(len(frame_files),end_frame)):

          frame_path = os.path.join(frame_dir, frame_files[j])
          output_frame_path = os.path.join(output_frame_dir, f"frame_{output_frame_index:04d}.jpg")
          os.system(f"cp {frame_path} {output_frame_path}")

          output_frame_index+=1
        frame_index = end_frame
    
    last_interval_end = librosa.samples_to_time(intervals[-1][1], sr=sr)

    if (last_interval_end) < librosa.get_duration(y=y,sr=sr):
      for j in range(frame_index, len(frame_files)):
        frame_path = os.path.join(frame_dir, frame_files[j])
        output_frame_path = os.path.join(output_frame_dir, f"frame_{output_frame_index:04d}.jpg")
        os.system(f"cp {frame_path} {output_frame_path}")
        output_frame_index+=1