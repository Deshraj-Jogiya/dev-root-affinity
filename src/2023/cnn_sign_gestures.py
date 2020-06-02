import tensorflow as tf
from tensorflow.keras import layers, models

def build_sign_language_cnn(input_shape=(64, 64, 1), num_classes=10):
    """
    Builds a Convolutional Neural Network (CNN) architecture designed for
    classifying American Sign Language (ASL) static digit gestures (0-9).
    Created for the ASU Master's Computer Vision course project.
    """
    model = models.Sequential()

    # Layer 1: Conv + ReLU + MaxPool
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))

    # Layer 2: Conv + ReLU + MaxPool
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    # Layer 3: Conv + ReLU + MaxPool
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    # Flatten & Dense Classifier
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5)) # Regularization to prevent overfitting
    model.add(layers.Dense(num_classes, activation='softmax')) # Output Layer

    # Compile the model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

if __name__ == "__main__":
    # Create the model instance
    asl_model = build_sign_language_cnn()
    
    # Print architecture summary
    print("=== ASU Sign Language CNN Architecture ===")
    asl_model.summary()
