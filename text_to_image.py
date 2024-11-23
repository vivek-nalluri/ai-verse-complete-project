import os
import uuid
from diffusers import StableDiffusionPipeline
import torch
import zipfile

# Directory to save generated images
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Stable Diffusion model for CPU
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.to("cpu")
    print("Using CPU for model inference.")
    return pipe

def generate_image(prompt, num_images, guidance_scale, height, width):
    if "pipe" not in globals():
        global pipe
        pipe = load_model()

    results = pipe(
        prompt,
        num_inference_steps=25,
        guidance_scale=guidance_scale,
        height=height,
        width=width,
        num_images_per_prompt=num_images
    ).images

    file_paths = []
    for img in results:
        file_name = f"{OUTPUT_DIR}/{uuid.uuid4().hex}.png"
        img.save(file_name)
        file_paths.append(file_name)

    zip_file_path = f"{OUTPUT_DIR}/{uuid.uuid4().hex}_images.zip"
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for file_path in file_paths:
            zipf.write(file_path, os.path.basename(file_path))

    return file_paths, zip_file_path
