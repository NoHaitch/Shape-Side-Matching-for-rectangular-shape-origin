from PIL import Image


class ImageProcessing:
    """
    Class to process images and extract their pattern
    """

    @staticmethod
    def extract_pattern_array(image_path: str, side: str) -> list[int]:
        """
        Extract the pattern in the form of an array from an image\n
        The array contains the distance from the edge of the image to the next pixel\n
        if side == "left", the shape is on the right side of the image\n
        if side == "right", the shape is on the left side of the image\n
        if side == "top", the shape is on the bottom side of the image\n
        if side == "bottom", the shape is on the top side of the image
        """

        # Open the image
        image = Image.open(image_path)
        image = image.convert('RGB')

        # Get the dimensions of the puzzle image
        width, height = image.size

        if side in ["left", "right"]:
            distances = [-1 for _ in range(height)]
            max_distance_length = height
        else:
            distances = [-1 for _ in range(width)]
            max_distance_length = width

        # Find the distance of the first pixel from the left side of the image
        if side == "left":
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    if pixel != (0, 0, 0):
                        distances[y] = x
                        break

        # Find the distance of the first pixel from the right side of the image
        elif side == "right":
            for y in range(height):
                for x in range(width - 1, -1, -1):
                    pixel = image.getpixel((x, y))
                    if pixel != (0, 0, 0):
                        distances[y] = width - 1 - x
                        break

            for i, distance in enumerate(distances):
                distances[i] = abs(distance-255)

        # Find the distance of the first pixel from the top side of the image
        elif side == "top":
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x, y))
                    if pixel != (0, 0, 0):
                        distances[x] = y
                        break

        # Find the distance of the first pixel from the bottom side of the image
        elif side == "bottom":
            for x in range(width):
                for y in range(height - 1, -1, -1):
                    pixel = image.getpixel((x, y))
                    if pixel != (0, 0, 0):
                        distances[x] = height - 1 - y
                        break

        return ImageProcessing.flatten_pattern(distances)

    @staticmethod
    def flatten_pattern(distance: list[int] | None) -> list[int] | None:
        """
        Flatten the non-negative distances by subtracting the minimum distance from all distances.
        """
        if distance is None:
            return None

        minimum_distance = min([elmt for elmt in distance if elmt != -1])
        for i in range(len(distance)):
            if distance[i] != -1:
                distance[i] -= minimum_distance
        return distance
