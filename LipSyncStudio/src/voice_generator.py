import os
import torch
from TTS.api import TTS
import whisper
import librosa
import numpy as np

def generate_audio(text, sample=None, language='en', emotion=0.5):
    """
    Generates audio from text using Coqui TTS XTTS-v2 or clones voice from a sample.

    Args:
        text (str): The text to synthesize, or None if transcribing from a sample audio.
        sample (str, optional): Path to a voice sample for cloning. Defaults to None.
        language (str, optional): Language code for TTS (e.g., 'en', 'es'). Defaults to 'en'.
        emotion (float, optional): Emotion intensity (0-1). Defaults to 0.5.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load models
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    whisper_model = whisper.load_model("base").to(device)
    
    # Check for sample file
    if sample is not None:
        if not os.path.exists(sample):
             raise FileNotFoundError(f"Voice sample file not found: {sample}")

    # Transcribe if no text provided
    if text is None:
        if sample is None:
             raise ValueError("Either text or a voice sample must be provided.")
        
        audio = whisper.load_audio(sample)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

        _, probs = whisper_model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions()
        result = whisper.decode(whisper_model, mel, options)

        text = result.text

    # Adjust pitch and speed based on emotion
    pitch = 1.0 + (emotion - 0.5) * 0.4  # Range: 0.8 to 1.2
    speed = 1.0 + (emotion - 0.5) * 0.2  # Range: 0.9 to 1.1

    # Generate audio
    if sample:
        tts.tts_to_file(
            text=text,
            file_path="generated_audio.wav",
            speaker_wav=sample,
            language=language,
            speed=speed,
            pitch=pitch
        )
    else:
        tts.tts_to_file(
            text=text,
            file_path="generated_audio.wav",
            language=language,
            speed=speed,
            pitch=pitch
        )
    print("Generated audio saved to generated_audio.wav")