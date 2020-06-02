# Convolutional Neural Network (CNN) Layers for Gesture Recognition

When building my American Sign Language (ASL) gesture recognition engine, I leveraged a deep Convolutional Neural Network (CNN) in TensorFlow and Keras. This note covers the architectural design and purpose of convolutional and pooling layers.

## Why CNNs for ASL Gesture Recognition?
Unlike dense neural networks which flatten spatial image matrices (which destroys spatial relationships between pixels), CNNs use learnable filters (kernels) that slide across the image width and height to capture spatial features (edges, curves, and shapes of fingers/hands).

## Model Architecture in Keras
Here is the convolutional structure I designed to classify 28x28 grayscale hand gestures:

```python
import tensorflow as tf
from tensorflow.keras import layers, models

def build_asl_cnn(input_shape=(28, 28, 1), num_classes=24):
    model = models.Sequential()
    
    # 1. First Convolutional Block
    # 32 filters, 3x3 kernel size. Input shape is (28, 28, 1)
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2))) # Shrinks dimension to (13, 13)
    
    # 2. Second Convolutional Block
    # 64 filters capture more complex patterns (finger joints, palm intersections)
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2))) # Shrinks dimension to (5, 5)
    
    # 3. Third Convolutional Block
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    
    # 4. Dense Classification Head
    model.add(layers.Flatten()) # Converts multi-dimensional feature maps into a 1D vector
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dropout(0.5)) # Regularization to prevent overfitting
    model.add(layers.Dense(num_classes, activation="softmax")) # Softmax for multi-class probability
    
    return model

# Instantiate and summarize
model = build_asl_cnn()
model.summary()
```

## Layer Explanations
- **`Conv2D`**: Slides a 3x3 weight window across the input matrix. The activation function `ReLU` introduces non-linearity (replacing negative pixel values with 0).
- **`MaxPooling2D`**: Slides a 2x2 window and keeps only the maximum value, reducing the spatial size and decreasing computing costs.
- **`Dropout`**: Randomly turns off 50% of the neurons during training, forcing the network to learn redundant representations and reducing overfitting on training frames.
