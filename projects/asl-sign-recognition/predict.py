import argparse
import numpy as np
import tensorflow as tf

def parse_args():
    parser = argparse.ArgumentParser(description="Predict ASL gesture sign from an image.")
    parser.add_argument("--image", type=str, default=None, help="Path to input image file.")
    parser.add_argument("--model", type=str, default="asl_model.h5", help="Path to saved model h5 file.")
    return parser.parse_args()

def preprocess_image(image_path, target_size=(64, 64)):
    """
    Reads an image from disk, converts to grayscale, and resizes it.
    If no image_path is provided, generates a random mock test image.
    """
    if image_path:
        print(f"Reading and preprocessing input image: {image_path}...")
        # In a real setup:
        # img = tf.keras.utils.load_img(image_path, color_mode="grayscale", target_size=target_size)
        # img_array = tf.keras.utils.img_to_array(img) / 255.0
        # return np.expand_dims(img_array, axis=0)
        pass
        
    print("No image path provided. Generating a mock input image matrix...")
    mock_img = np.random.rand(1, target_size[0], target_size[1], 1).astype(np.float32)
    return mock_img

def main():
    args = parse_args()
    print("=== ASL CNN Inference Engine ===")
    
    # 1. Load the model
    try:
        model = tf.keras.models.load_model(args.model)
        print(f"Loaded trained model from {args.model} successfully.")
    except Exception as exc:
        print(f"Error loading model: {exc}")
        print("Please run train.py first to train and generate the model file.")
        return
        
    # 2. Preprocess input
    img_tensor = preprocess_image(args.image)
    
    # 3. Predict
    predictions = model.predict(img_tensor, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    
    print("\n=== Prediction Result ===")
    print(f"Predicted Class ID: {predicted_class}")
    print(f"Confidence Score: {confidence * 100:.2f}%")
    print(f"Probability Distribution: {predictions[0]}")

if __name__ == "__main__":
    main()
