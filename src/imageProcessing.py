from pattern import Pattern
from PIL import Image
import os


class ImageProcessing:  

    @staticmethod
    def extract_edges_pattern(image_path: str) -> tuple[Pattern, Pattern]:
        """
        Extract the pattern from each 4 sides of an image.
        :return Edge Pattern, Color Pattern
        """
        image = Image.open(image_path)
        image = image.convert('RGB')  # Ensure image is in RGB format

        # Get the dimensions of the puzzle image
        width, height = image.size

        left_distance = [-1 for _ in range(height)]
        right_distance = [-1 for _ in range(height)]
        top_distance = [-1 for _ in range(width)]
        bottom_distance = [-1 for _ in range(width)]

        left_color = [0 for _ in range(height)]        
        right_color = [0 for _ in range(height)]        
        bottom_color = [0 for _ in range(width)]        
        top_color = [0 for _ in range(width)]

        # Helper function to calculate average color
        def normalize_color(color_value, min_value, max_value, new_min=0, new_max=255):
            """
            Normalize a color value to a new range.
            """
            return ((color_value - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min

        def average_color(pixels):
            """
            Calculate the average color of a set of pixels using min-max normalization.
            """
            # Calculate minimum and maximum values for each color channel
            min_r = min(p[0] for p in pixels)
            max_r = max(p[0] for p in pixels)
            min_g = min(p[1] for p in pixels)
            max_g = max(p[1] for p in pixels)
            min_b = min(p[2] for p in pixels)
            max_b = max(p[2] for p in pixels)

            # Normalize each color channel individually
            normalized_r = 0 if min_r == max_r else normalize_color(sum(p[0] for p in pixels) / len(pixels), min_r, max_r)
            normalized_g = 0 if min_g == max_g else normalize_color(sum(p[1] for p in pixels) / len(pixels), min_g, max_g)
            normalized_b = 0 if min_b == max_b else normalize_color(sum(p[2] for p in pixels) / len(pixels), min_b, max_b)

            # Combine normalized values to get grayscale value
            return 0.21 * normalized_r + 0.72 * normalized_g + 0.07 * normalized_b

        # Get left side distance and color
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                if pixel != (0, 0, 0):
                    left_distance[y] = x
                    left_pixels = [image.getpixel((min(x + i, width - 1), y)) for i in range(15)]
                    left_color[y] = average_color(left_pixels)
                    break

        # Get right side distance and color
        for y in range(height):
            for x in range(width - 1, -1, -1):
                pixel = image.getpixel((x, y))
                if pixel != (0, 0, 0):
                    right_distance[y] = x
                    right_pixels = [image.getpixel((max(x - i, 0), y)) for i in range(15)]
                    right_color[y] = average_color(right_pixels)
                    break

        # Get bottom side distance and color
        for x in range(width):
            for y in range(height - 1, -1, -1):
                pixel = image.getpixel((x, y))
                if pixel != (0, 0, 0):
                    bottom_distance[x] = y
                    bottom_pixels = [image.getpixel((x, max(y - i, 0))) for i in range(15)]
                    bottom_color[x] = average_color(bottom_pixels)
                    break

        # Get top side distance and color
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                if pixel != (0, 0, 0):
                    top_distance[x] = y
                    top_pixels = [image.getpixel((x, min(y + i, height - 1))) for i in range(15)]
                    top_color[x] = average_color(top_pixels)
                    break
        
        # Remove pattern where distance is above the limit
        fluctuation_limit = 150
        
        # Remove end of pattern
        def remove_fluctuations(distance, color):
            for i in range(len(distance) - 1):
                if abs(distance[i] - distance[i + 1]) > fluctuation_limit:
                    return distance[:i], color[:i]
            return distance, color

        left_distance, left_color = remove_fluctuations(left_distance, left_color)
        right_distance, right_color = remove_fluctuations(right_distance, right_color)
        bottom_distance, bottom_color = remove_fluctuations(bottom_distance, bottom_color)
        top_distance, top_color = remove_fluctuations(top_distance, top_color)

        # Flatten distances
        left_pattern = ImageProcessing.flatten_pattern(left_distance)
        right_pattern = ImageProcessing.flatten_pattern(right_distance)
        top_pattern = ImageProcessing.flatten_pattern(top_distance)
        bottom_pattern = ImageProcessing.flatten_pattern(bottom_distance)

        return Pattern(left_pattern, right_pattern, top_pattern, bottom_pattern), Pattern(left_color, right_color, top_color, bottom_color)

    @staticmethod
    def flatten_pattern(distance: list[int]) -> list[int]:
        """
        Flatten the non-negative distances by subtracting the minimum distance from all distances.
        """
        minimum_distance = min([elmt for elmt in distance if elmt != -1])
        for i in range(len(distance)):
            if distance[i] != -1:
                distance[i] -= minimum_distance
        return distance

    @staticmethod
    def process_images_in_folder(folder_path: str) -> dict[str, tuple[Pattern, Pattern]]:
        """
        Process all images in the given folder and extract their edge patterns.
        """
        patterns = {}
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Check for image files
                image_path = os.path.join(folder_path, filename)
                patterns[filename] = ImageProcessing.extract_edges_pattern(image_path)
                print(f"Processed {filename}")

        return patterns
