import os
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, set_seed

# Set a directory for output (if needed)
OUTPUT_DIR = "generated_descriptions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the pre-trained GPT-2 model and tokenizer
def load_model():
    model_name = "gpt2"  # Can replace with "distilgpt2" for a smaller model
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.eval()  # Set the model to evaluation mode
    print("Model loaded successfully.")
    return tokenizer, model

# Generate a description from the input text
def generate_description(input_text, max_length=50, temperature=1.0, top_k=50, seed=42):
    if "tokenizer" not in globals() or "model" not in globals():
        global tokenizer, model
        tokenizer, model = load_model()

    set_seed(seed)  # Ensure reproducibility
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    with torch.no_grad():  # No gradient calculations needed
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,  # Controls creativity (higher = more creative)
            top_k=top_k,  # Top-K sampling to control randomness
            num_return_sequences=1  # Number of outputs to generate
        )

    # Decode the generated output
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text
