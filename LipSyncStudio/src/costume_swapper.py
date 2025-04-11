import cv2
import mediapipe as mp
import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image
import numpy as np
import os

class CostumeSwapper:
    def __init__(self, model_path="stabilityai/stable-diffusion-2-inpainting"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        ).to(self.device)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1)

    def generate_torso_mask(self, image):
        """Generates a torso mask using MediaPipe Pose."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.mp_pose.process(image_rgb)

        if not results.pose_landmarks:
            return None

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Define relevant landmarks for torso
        torso_landmarks = [
            mp.solutions.pose.PoseLandmark.LEFT_SHOULDER,
            mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER,
            mp.solutions.pose.PoseLandmark.LEFT_HIP,
            mp.solutions.pose.PoseLandmark.RIGHT_HIP,
        ]
        
        points = []
        for landmark_enum in torso_landmarks:
            landmark = results.pose_landmarks.landmark[landmark_enum]
            h, w = image.shape[:2]
            points.append((int(landmark.x * w), int(landmark.y * h)))

        # Draw polygon on the mask
        points = np.array(points, dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)
        
        return mask

    def swap_costume(self, frame_path, costume_path, output_path):
        """Swaps the costume in the given frame using Stable Diffusion Inpainting."""
        try:
            frame = cv2.imread(frame_path)
            costume = cv2.imread(costume_path)

            if frame is None or costume is None:
                raise FileNotFoundError("Frame or costume image not found")
                
            mask = self.generate_torso_mask(frame)
            
            if mask is None:
                print(f"Warning: No torso detected in {frame_path}. Skipping.")
                cv2.imwrite(output_path, frame)
                return

            mask_image = Image.fromarray(mask)

            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            prompt = "a person wearing a " + os.path.basename(costume_path).split('.')[0].replace('_',' ') + ", highly detailed"

            inpainted_image = self.pipe(
                prompt=prompt,
                image=frame_pil,
                mask_image=mask_image,
            ).images[0]

            inpainted_cv2 = cv2.cvtColor(np.array(inpainted_image), cv2.COLOR_RGB2BGR)

            center = (frame.shape[1] // 2, frame.shape[0] // 2)
            seamless_clone = cv2.seamlessClone(
                inpainted_cv2, frame, mask, center, cv2.MIXED_CLONE
            )
            cv2.imwrite(output_path, seamless_clone)

        except Exception as e:
            print(f"Error processing {frame_path}: {e}")

    def process_video_costumes(self, frame_dir, costume_path):
        """Batch-processes frames to swap costumes."""
        if not os.path.exists(frame_dir):
            raise FileNotFoundError(f"Frame directory not found: {frame_dir}")

        output_dir = os.path.join(os.path.dirname(frame_dir), "costume_frames")
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in os.listdir(frame_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                frame_path = os.path.join(frame_dir, filename)
                output_path = os.path.join(output_dir, filename)
                self.swap_costume(frame_path, costume_path, output_path)

# Example usage (assuming you have frame_dir and costume_path defined):
# costume_swapper = CostumeSwapper()
# costume_swapper.process_video_costumes("path/to/frames", "path/to/costume.jpg")