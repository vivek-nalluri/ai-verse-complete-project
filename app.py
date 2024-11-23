import gradio as gr
from text_to_image import generate_image
from text_to_video import generate_video

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

def main():
    with gr.Blocks() as app:
        gr.Markdown("# Unified Text-to-Image and Text-to-Video Generator")
        with gr.Tab("Text-to-Image"):
            text_to_image_interface()
        with gr.Tab("Text-to-Video"):
            text_to_video_interface()

    app.launch()

if __name__ == "__main__":
    main()
