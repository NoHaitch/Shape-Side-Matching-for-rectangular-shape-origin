import os
from patternProcessing import PatternProcessing

class Dataset:
    """
    Process images for a whole folder
    """

    @staticmethod
    def get_folder_ascii_pattern(folder_path: str) -> dict[str, dict[str, str]]:
        """
        Extract ASCII patterns for all images in a folder.
        The patterns are extracted for each side of the image and stored in a nested dictionary.
        """
        patterns = {}

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):

            # Only accept PNG images
            if filename.endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                
                # Extract the ASCII pattern from the image for each side
                sides = ["left", "right", "top", "bottom"]
                side_patterns = {}
                for side in sides:
                    ascii_pattern = PatternProcessing.get_image_ascii_pattern(image_path, side)
                    
                    # Don't store empty or invalid patterns
                    if ascii_pattern is None:
                        continue

                    # Store the ASCII pattern with the side name
                    side_patterns[side] = ascii_pattern
                
                # Store patterns only if at least one valid pattern is found
                if side_patterns:
                    patterns[filename] = side_patterns

        return patterns