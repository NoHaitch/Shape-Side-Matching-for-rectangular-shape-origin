import cv2
import numpy as np


class ImageSimilarity:
    """
    Image Similarity Module\n
    Provides functions to calculate the similarity between two images based on edge patterns and color distributions.
    """

    @staticmethod
    def calculate_edge_similarity(edge1: np.ndarray, edge2: np.ndarray) -> float:
        """
        Calculate the similarity between two edges of puzzle pieces using ORB key points and descriptors.
        
        Parameters:
            edge1 : Edge image of the first puzzle piece.
            edge2 : Edge image of the second puzzle piece.
            
        Returns:
            float: Similarity between the two edges based on key points and descriptors.
        """

        # Initialize ORB detector
        orb = cv2.ORB_create()

        # Find key points and descriptors with ORB
        key_points1, descriptors1 = orb.detectAndCompute(edge1, None)
        key_points2, descriptors2 = orb.detectAndCompute(edge2, None)

        if descriptors1 is None or descriptors2 is None:
            return 0.0

        # Create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors
        matches = bf.match(descriptors1, descriptors2)

        # Calculate the similarity score based on matches
        similarity_index = len(matches) / max(len(key_points1), len(key_points2))
        return similarity_index

    @staticmethod
    def calculate_color_similarity(regions1: list[np.ndarray], regions2: list[np.ndarray]) -> float:
        """
        Calculate the similarity between two sets of regions based on color histograms.
        
        Parameters:
            regions1 (list of numpy.ndarray): List of regions from the first puzzle piece.
            regions2 (list of numpy.ndarray): List of regions from the second puzzle piece.
            
        Returns:
            float: Similarity between the two sets of regions based on color histograms.
        """
        # Initialize histograms
        hist1 = np.zeros((8, 8, 8), dtype=np.float32)
        hist2 = np.zeros((8, 8, 8), dtype=np.float32)

        # Calculate histograms for each set of regions
        for region in regions1:
            if region.size == 0:
                continue
            h = cv2.calcHist([region], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist1 += h

        for region in regions2:
            if region.size == 0:
                continue
            h = cv2.calcHist([region], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist2 += h

        # Normalize the histograms
        hist1 = hist1 / np.sum(hist1)
        hist2 = hist2 / np.sum(hist2)

        # Calculate histogram intersection similarity
        color_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
        color_similarity /= np.min([np.sum(hist1), np.sum(hist2)])  # Normalize to range [0, 1]
        return color_similarity

    @staticmethod
    def extract_edge_regions(image: np.ndarray, edges: np.ndarray, region_size: int = 10) -> list[np.ndarray]:
        """
        Extract regions around the edges of the puzzle piece for color comparison.
        
        Parameters:
            image (numpy.ndarray): Original puzzle piece image.
            edges (numpy.ndarray): Edge image of the puzzle piece.
            region_size (int): Size of the region around each edge pixel to consider for color comparison.
            
        Returns:
            list of numpy.ndarray: Extracted regions around the edges.
        """
        regions = []
        for y, x in zip(*np.where(edges != 0)):
            ymin = max(0, y - region_size)
            ymax = min(image.shape[0], y + region_size)
            xmin = max(0, x - region_size)
            xmax = min(image.shape[1], x + region_size)
            regions.append(image[ymin:ymax, xmin:xmax])
        return regions

    @staticmethod
    def puzzle_alignment(piece1_path: str, piece2_path: str) -> float:
        """
        Calculate the percentage of alignment between the edges of two puzzle pieces\n
        Calculated using the similarity of edge pattern and edge color distributions.
        
        Parameters:
            piece1_path: File path to the first puzzle piece image.
            piece2_path: File path to the second puzzle piece image.

        Returns:
            float: Percentage of alignment between 2 puzzle piece.
        """

        # Load puzzle piece images
        piece1: np.ndarray = cv2.imread(piece1_path)
        piece2: np.ndarray = cv2.imread(piece2_path)

        # ===== Edge Pattern Similarity =====
        # Convert images to grayscale
        gray1: np.ndarray = cv2.cvtColor(piece1, cv2.COLOR_BGR2GRAY)
        gray2: np.ndarray = cv2.cvtColor(piece2, cv2.COLOR_BGR2GRAY)

        # Extract edges using Canny edge detection
        edge1: np.ndarray = cv2.Canny(gray1, 100, 200)
        edge2: np.ndarray = cv2.Canny(gray2, 100, 200)

        # Calculate similarity for edge pattern using key points and descriptors
        edge_similarity: float = ImageSimilarity.calculate_edge_similarity(edge1, edge2)

        # ===== Color Distribution Similarity =====
        # Extract regions near edges for color comparison
        edge_regions1: list[np.ndarray] = ImageSimilarity.extract_edge_regions(piece1, edge1)
        edge_regions2: list[np.ndarray] = ImageSimilarity.extract_edge_regions(piece2, edge2)

        # Calculate color similarity for the regions around edges
        color_similarity: float = ImageSimilarity.calculate_color_similarity(edge_regions1, edge_regions2)

        # ===== Combined Similarity =====
        # Combine edge and color similarities (you can adjust the weights as needed)
        combined_similarity: float = 0.5 * edge_similarity + 0.5 * color_similarity

        # Calculate percentage of alignment based on combined similarity
        percentage_alignment: float = combined_similarity * 100
        percentage_alignment = min(100.0, max(0.0, percentage_alignment))
        return percentage_alignment
