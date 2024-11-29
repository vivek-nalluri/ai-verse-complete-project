# Original imports and code
import gradio as gr
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
            gr.Slider(1, 4, step=1, value=1, label="Number of Images"),  # Number of images
            gr.Slider(1, 20, step=1, value=7.5, label="Guidance Scale"),  # Prompt adherence
            gr.Slider(256, 1024, step=64, value=512, label="Image Height (px)"),  # Image height
            gr.Slider(256, 1024, step=64, value=512, label="Image Width (px)")  # Image width
        ],
        outputs=[
            gr.Gallery(label="Generated Images"),  # Show images in a gallery
            gr.File(label="Download All Images")  # Provide a download option
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
            gr.Slider(1, 30, step=1, value=10, label="Number of Frames"),  # Total frames
            gr.Slider(1, 60, step=1, value=15, label="Frames per Second (FPS)"),  # FPS
            gr.Slider(1, 20, step=1, value=7.5, label="Guidance Scale"),  # Prompt adherence
            gr.Slider(256, 1024, step=64, value=512, label="Frame Height (px)"),  # Frame height
            gr.Slider(256, 1024, step=64, value=512, label="Frame Width (px)")  # Frame width
        ],
        outputs=[gr.File(label="Download Video")],  # Provide a download option
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

        # Add Logout Button with styling
        with gr.Row():
            gr.Markdown("### Logout Section")
            gr.HTML('<button style="padding:10px 20px; background-color:red; color:white; border:none; border-radius:5px;" onclick="window.location.href=\'http://127.0.0.1:5000/logout\'">Logout</button>')

    return app

if __name__ == "__main__":
    # Launch Gradio app
    gradio_app = main()
    gradio_app.launch(server_name="127.0.0.1", server_port=7860)

# Logout functionality integration
from flask import Flask, session, redirect
import mysql.connector
import threading

# Flask app for logout
logout_app = Flask(__name__)
logout_app.secret_key = "your_secret_key"  # Replace with a secure key

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Your MySQL host
        user="root",            # Your MySQL username
        password="Vivek94947@", # Your MySQL password
        database="user_database" # Your MySQL database
    )

# Logout route
@logout_app.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session['user_id']

        # Clear session from the database
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM user_sessions WHERE user_id = %s", (user_id,))
        db.commit()
        cursor.close()
        db.close()

        # Clear session in Flask
        session.pop('user_id', None)

    # Redirect to Gradio app after logout
    return redirect('http://127.0.0.1:7860')

# Function to start Flask in a separate thread
def start_flask():
    logout_app.run(host="127.0.0.1", port=5000)

# Run Flask app in a separate thread
flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()
