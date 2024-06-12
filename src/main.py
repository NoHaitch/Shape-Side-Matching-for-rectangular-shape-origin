from dataset import Dataset
from shapeMatching import ShapeMatching
from patternProcessing import PatternProcessing
from imageProcessing import ImageProcessing

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def visualize_match(best_match_image_path: str, original_image_path: str):
    # Load images
    best_match_image = Image.open(best_match_image_path)
    original_image = Image.open(original_image_path)

    # Display images
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Plot best match image
    axes[0].imshow(best_match_image)
    axes[0].set_title('Best Match Image')

    # Plot original image
    axes[1].imshow(original_image)
    axes[1].set_title('Original Image')

    # Hide axes
    for ax in axes:
        ax.axis('off')

    plt.show()

def main():

    

    img = "test\\right-side-3.png"
    data_folder = "dataset"

    dataset_pattern = Dataset.get_folder_ascii_pattern(data_folder)

    result = ShapeMatching.ShapeMatchBM(img, "right", dataset_pattern)

    # Example usage:
    best_matched_image_path = "dataset\\" + result.split('/')[0]
    original_image_path = img
    visualize_match(best_matched_image_path, original_image_path)

if __name__ == "__main__":
    main()
