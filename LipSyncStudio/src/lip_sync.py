import subprocess
import os
from config import LATENTSYNC_PATH, MUSE_TALK_PATH

def sync_video(video_path, audio_path, output_path, real_time_mode=False):
    """
    Synchronizes video with audio using LatentSync and adds full-face animation with MuseTalk.

    Args:
        video_path (str): Path to the input video.
        audio_path (str): Path to the input audio.
        output_path (str): Path to save the synchronized video.
        real_time_mode (bool): Whether to use real-time mode (LiveSpeechPortraits).
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if real_time_mode:
        # Placeholder for real-time lip sync and animation
        try:
            subprocess.run(["python", "live_sync.py", "--video", video_path, "--audio", audio_path, "--output", output_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error in live_sync.py: {e}")
        print(f"Real-time mode (LiveSpeechPortraits) applied. Output saved to: {output_path}")
        return
    
    # Lip Sync with LatentSync
    try:
        subprocess.run([
            "python", os.path.join(LATENTSYNC_PATH, "inference.py"),
            "--video", video_path,
            "--audio", audio_path,
            "--outfile", output_path.replace(".mp4", "_temp_lipsync.mp4")
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error in LatentSync: {e}")
    
    print(f"LatentSync applied. Temporary lip-synced video saved to {output_path.replace('.mp4', '_temp_lipsync.mp4')}")

    # Full-face animation with MuseTalk (using the temporary lip-synced video)
    try:
        subprocess.run([
            "python", os.path.join(MUSE_TALK_PATH,"demo.py"),
            "--source_image", video_path,
            "--driven_audio", audio_path,
            "--result_dir", os.path.dirname(output_path),
            "--outfile", output_path
            
        ], check=True)

        os.remove(output_path.replace(".mp4", "_temp_lipsync.mp4"))
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error in MuseTalk: {e}")

    print(f"MuseTalk applied. Final synchronized video saved to: {output_path}")