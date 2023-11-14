# ASL Sign Gesture Recognition using Convolutional Neural Networks

This project implements a Convolutional Neural Network (CNN) in TensorFlow/Keras to classify static American Sign Language (ASL) gestures (specifically digits 0-9 and letters A-Z). It was developed as a course project during my Master of Science in Information Technology (MS IT) program at Arizona State University (ASU).

## Project Structure
- `model.py` — CNN architecture definition with dropout regularization.
- `dataset.py` — Data pipeline to load, pre-process, normalize, and split image directories.
- `train.py` — Script to compile, fit, and save training weights.
- `predict.py` — Inference engine to perform predictions on sample images.

## CNN Model Architecture
The network consists of:
1. **Feature Extraction Blocks**: Three sets of `Conv2D` layers with rectified linear activation (ReLU), paired with `MaxPooling2D` and `BatchNormalization` to accelerate convergence.
2. **Regularization**: `Dropout` layers to mitigate overfitting.
3. **Classification Dense Network**: A fully connected `Dense` layer feeding into a `Softmax` output classifier matching the number of gesture categories.

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run model summary check:
   ```bash
   python model.py
   ```
3. Train the model:
   ```bash
   python train.py
   ```
4. Predict a test image:
   ```bash
   python predict.py --image path/to/sample.jpg
   ```
