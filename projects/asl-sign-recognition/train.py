import os
import argparse
import matplotlib.pyplot as plt
from model import get_asl_model
from dataset import load_data, get_train_val_test_splits

def parse_args():
    parser = argparse.ArgumentParser(description="Train ASL sign gesture recognition model.")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training.")
    parser.add_argument("--output-model", type=str, default="asl_model.h5", help="Output path for the trained model.")
    return parser.parse_args()

def main():
    args = parse_args()
    print("=== Initiating ASL CNN Training Pipeline ===")
    
    # 1. Load data
    images, labels = load_data()
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = get_train_val_test_splits(images, labels)
    
    # 2. Instantiate and compile model
    model = get_asl_model(input_shape=(64, 64, 1), num_classes=10)
    
    # 3. Fit model
    print(f"\nStarting training for {args.epochs} epochs with batch size {args.batch_size}...")
    history = model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=1
    )
    
    # 4. Evaluate on test split
    print("\nEvaluating model on test split...")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_acc:.4f} | Test Loss: {test_loss:.4f}")
    
    # 5. Save the trained weights
    model.save(args.output_model)
    print(f"Trained model saved successfully to: {args.output_model}")
    
    # 6. Plot & Save training history curves (Loss and Accuracy)
    plt.figure(figsize=(12, 4))
    
    # Plot Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy')
    plt.title('Training & Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    # Plot Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Training & Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    history_plot_path = "training_curves.png"
    plt.tight_layout()
    plt.savefig(history_plot_path)
    print(f"Training curves plot saved to: {history_plot_path}")

if __name__ == "__main__":
    main()
