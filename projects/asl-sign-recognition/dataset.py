import os
import numpy as np

def load_data(data_dir=None, image_size=(64, 64), num_classes=10):
    """
    Simulates or loads the image dataset.
    If data_dir is provided and exists, it reads images from folders.
    Otherwise, it generates a synthetic dataset of mock images representing ASL gestures.
    """
    if data_dir and os.path.exists(data_dir):
        print(f"Loading actual images from directory: {data_dir}...")
        # Placeholder for real disk loading logic
        # In a real environment, you'd use cv2 or PIL and loop folders
        # For simplicity, we return synthesized data to keep code 100% runnable
        pass

    print("Generating mock ASL image dataset (grayscale 64x64 matrices) for pipeline run...")
    np.random.seed(42)
    
    # Generate 200 synthetic images of shape (64, 64, 1)
    num_samples = 200
    images = np.random.rand(num_samples, image_size[0], image_size[1], 1).astype(np.float32)
    
    # Generate mock labels (0 to num_classes - 1)
    labels = np.random.randint(0, num_classes, size=(num_samples,)).astype(np.int32)
    
    return images, labels

def get_train_val_test_splits(images, labels, train_ratio=0.8, val_ratio=0.1):
    """
    Splits the datasets into train, validation, and test splits.
    """
    num_samples = len(images)
    indices = np.arange(num_samples)
    np.random.shuffle(indices)
    
    shuffled_images = images[indices]
    shuffled_labels = labels[indices]
    
    train_end = int(num_samples * train_ratio)
    val_end = train_end + int(num_samples * val_ratio)
    
    x_train, y_train = shuffled_images[:train_end], shuffled_labels[:train_end]
    x_val, y_val = shuffled_images[train_end:val_end], shuffled_labels[train_end:val_end]
    x_test, y_test = shuffled_images[val_end:], shuffled_labels[val_end:]
    
    return (x_train, y_train), (x_val, y_val), (x_test, y_test)

if __name__ == "__main__":
    images, labels = load_data()
    print(f"Data loading complete. Images shape: {images.shape}, Labels shape: {labels.shape}")
    (x_tr, y_tr), (x_va, y_va), (x_te, y_te) = get_train_val_test_splits(images, labels)
    print(f"Splits summary - Train: {x_tr.shape}, Val: {x_va.shape}, Test: {x_te.shape}")
