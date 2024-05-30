import numpy as np
from skimage.transform import resize
from imageProcessing import ImageProcessing

class ImageSimilarity:
    """
    Image Similarity Module\n
    Provides functions to calculate the similarity between two images based on edge patterns and color distributions.
    """

    @staticmethod
    def pattern_similarity(pattern1: list[int], pattern2: list[int]) -> float:
        """
        Calculate the similarity between two patterns based on their values.
        """
        # Get the minimum length between the two pattern
        min_length = min(len(pattern1), len(pattern2))

        # Calculate the number of matching values
        match_count = 0
        for i in range(min_length):
            if(pattern1[i] == pattern2[i]):
                match_count += 1

        # Calculate the similarity as the ratio of matching values to the total number of values in the shortest pattern
        if min_length == 0:
            return 0.0
        
        similarity = match_count / min_length
        return similarity
    
    @staticmethod
    def color_similarity(colors1: list[float], colors2: list[float]) -> float:
        """
        Calculate the similarity between two sets of edge colors using histogram comparison.
        :param colors1: A list of grayscale colors from the first image.
        :param colors2: A list of grayscale colors from the second image.
        :return: A similarity score between 0 and 1.
        """
        # Calculate histograms
        hist1, _ = np.histogram(colors1, bins=256, range=(0, 255))
        hist2, _ = np.histogram(colors2, bins=256, range=(0, 255))

        # Normalize histograms
        hist1 = hist1 / np.sum(hist1)
        hist2 = hist2 / np.sum(hist2)

        # Compute the histogram intersection similarity
        similarity = np.sum(np.minimum(hist1, hist2))

        return similarity

    @staticmethod
    def combined_similarity(side_pattern1: tuple[list[int], list[float]], side_pattern2: tuple[list[int], list[float]], edge_weight: float = 0.7) -> float:
        """
        Combine edge similarity and color similarity into one uniform similarity.
        """
        edge_pattern1, color_pattern1 = side_pattern1        
        edge_pattern2, color_pattern2 = side_pattern2        

        edge_similarity = ImageSimilarity.pattern_similarity(edge_pattern1, edge_pattern2)
        color_similarity = ImageSimilarity.color_similarity(color_pattern1, color_pattern2)

        # Ensure the weights sum to 1
        color_weight = 1 - edge_weight
        
        combined_similarity = edge_weight * edge_similarity + color_weight * color_similarity
        return combined_similarity

