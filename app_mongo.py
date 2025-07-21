
# Original imports and code
import gradio as gr
import os
from text_to_image import generate_image
from text_to_video import generate_video
from text_to_description import generate_description

# Text-to-Image interface
def text_to_image_interface():
    return gr.Interface(
        fn=generate_image,
        inputs=[
            gr.Textbox(
                label="Describe the image",
                placeholder="E.g., a futuristic cityscape with flying cars"
            ),
            gr.Slider(1, 4, step=1, value=1, label="Number of Images"),
            gr.Slider(1, 20, step=1, value=7.5, label="Guidance Scale"),
            gr.Slider(256, 1024, step=64, value=512, label="Image Height (px)"),
            gr.Slider(256, 1024, step=64, value=512, label="Image Width (px)")
        ],
        outputs=[
            gr.Gallery(label="Generated Images"),
            gr.File(label="Download All Images")
        ],
        title="Text-to-Image Generator",
        description="Enter a description to generate an image with various customization options."
    )

# Text-to-Video interface
def text_to_video_interface():
    return gr.Interface(
        fn=generate_video,
        inputs=[
            gr.Textbox(
                label="Describe the video",
                placeholder="E.g., a futuristic cityscape with flying cars"
            ),
            gr.Slider(1, 30, step=1, value=10, label="Number of Frames"),
            gr.Slider(1, 60, step=1, value=15, label="Frames per Second (FPS)"),
            gr.Slider(1, 20, step=1, value=7.5, label="Guidance Scale"),
            gr.Slider(256, 1024, step=64, value=512, label="Frame Height (px)"),
            gr.Slider(256, 1024, step=64, value=512, label="Frame Width (px)")
        ],
        outputs=[gr.File(label="Download Video")],
        title="Text-to-Video Generator",
        description="Enter a description to generate a video with various customization options."
    )

# Text-to-Description interface
def text_to_description_interface():
    return gr.Interface(
        fn=generate_description,
        inputs=[
            gr.Textbox(
                label="Input Text",
                placeholder="E.g., Artificial Intelligence is"
            ),
            gr.Slider(20, 200, step=10, value=100, label="Max Description Length"),
            gr.Slider(0.5, 2.0, step=0.1, value=1.0, label="Temperature (Creativity)"),
            gr.Slider(1, 100, step=5, value=50, label="Top-K Sampling"),
            gr.Number(value=42, label="Random Seed")
        ],
        outputs=[
            gr.Textbox(label="Generated Description")
        ],
        title="Text-to-Description Generator",
        description="Generate detailed descriptions for any input text using a pre-trained Mistral-7B model."
    )

# Main function
def main():
    with gr.Blocks() as app:
        gr.Markdown("# AI-Verse: A Multimodal Generative AI Platform")
        with gr.Tab("Text-to-Image"):
            text_to_image_interface()
        with gr.Tab("Text-to-Video"):
            text_to_video_interface()
        with gr.Tab("Text-to-Description"):
            text_to_description_interface()

        with gr.Row():
            gr.Markdown("### Logout Section")
            gr.HTML('<button style="padding:10px 20px; background-color:red; color:white; border:none; border-radius:5px;" onclick="window.location.href=\'https://ai-verse-complete-project.onrender.com/logout\'">Logout</button>')

    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    gradio_app = main()
    gradio_app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

# Logout Flask app using MongoDB
from flask import Flask, session, redirect
import threading
from pymongo import MongoClient

logout_app = Flask(__name__)
logout_app.secret_key = "your_secret_key"

def get_db_connection():
    client = MongoClient("mongodb+srv://vivek94947:Vivek9494@cluster0.p9bhhfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return client["user"]

@logout_app.route('/logout')
def logout():
    if 'username' in session:
        db = get_db_connection()
        session_collection = db["sessions"]
        session_collection.delete_many({"username": session["username"]})
        session.pop('username', None)

    return redirect('/')

def start_flask():
    logout_app.run(host="0.0.0.0", port=5000)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()
