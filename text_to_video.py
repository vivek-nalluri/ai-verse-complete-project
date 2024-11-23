import os
import uuid
import cv2
import numpy as np
from diffusers import StableDiffusionPipeline
import torch

# Directory to save generated videos and frames
OUTPUT_DIR = "generated_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Stable Diffusion model for CPU
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.to("cpu")
    print("Using CPU for model inference.")
    return pipe

def generate_frames(prompt, num_frames, guidance_scale, height, width):
    if "pipe" not in globals():
        global pipe
        pipe = load_model()

    frames = []
    for i in range(num_frames):
        result = pipe(
            f"{prompt}, frame {i+1} of {num_frames}",
            num_inference_steps=25,
            guidance_scale=guidance_scale,
            height=height,
            width=width
        ).images[0]

        frames.append(np.array(result))

    return frames

def create_video(frames, fps):
    video_filename = f"{OUTPUT_DIR}/{uuid.uuid4().hex}.mp4"
    height, width, _ = frames[0].shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

    for frame in frames:
        video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    video_writer.release()
    return video_filename

def generate_video(prompt, num_frames, fps, guidance_scale, height, width):
    frames = generate_frames(prompt, num_frames, guidance_scale, height, width)
    video_path = create_video(frames, fps)
    return video_path
