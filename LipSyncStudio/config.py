import os

# --- Model Paths ---
MODELS_DIR = "models"
LATENTSYNC_PATH = os.path.join(MODELS_DIR, "LatentSync")  # Assuming you'll clone the repo here
MUSE_TALK_PATH = os.path.join(MODELS_DIR, "MuseTalk")  # Assuming you'll clone the repo here
NERF_STUDIO_PATH = os.path.join(MODELS_DIR, "nerfstudio") #Assuming you clone it here

# --- Model Checkpoints ---
XTTS_V2_CHECKPOINT = os.path.join(MODELS_DIR, "xtts_v2")  # Path to your downloaded XTTS-v2 checkpoint
STABLE_DIFFUSION_INPAINTING_CHECKPOINT = "stabilityai/stable-diffusion-2-inpainting" # Hugging Face model ID or local path

# --- Data Paths ---
ASSETS_DIR = "assets"
OUTPUT_DIR = "output"
FRAMES_DIR = "frames"
COSTUME_FRAMES_DIR = "costume_frames"

# --- Sample Assets (placeholders) ---
SAMPLE_VIDEO = os.path.join(ASSETS_DIR, "sample.mp4")
SAMPLE_AUDIO = os.path.join(ASSETS_DIR, "sample.wav")
SAMPLE_COSTUME = os.path.join(ASSETS_DIR, "suit.jpg")

# --- Intermediate Files ---
GENERATED_AUDIO = "generated_audio.wav"

# --- Check if directories exist, if not create them
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(COSTUME_FRAMES_DIR, exist_ok=True)