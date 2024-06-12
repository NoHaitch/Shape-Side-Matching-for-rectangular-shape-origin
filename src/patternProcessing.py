from imageProcessing import ImageProcessing

class PatternProcessing:
    """
    Process image and array pattern to get Ascii String
    """
    
    @staticmethod
    def get_image_ascii_pattern(image_path: str, side: str) -> str:
        """
        Get the ascii pattern from image\n
        if side == "left", the shape is on the right side of the image\n
        if side == "right", the shape is on the left side of the image\n
        if side == "top", the shape is on the bottom side of the image\n
        if side == "bottom", the shape is on the top side of the image
        """

        pattern_array = ImageProcessing.extract_pattern_array(image_path, side)
        for i in range(len(pattern_array)//2):
            if pattern_array[i] < 256:
                pattern_array = pattern_array[i::]
                break

        for i in range(len(pattern_array)):
            if pattern_array[i] > 255:
                pattern_array = pattern_array[0:i]
                break

        if PatternProcessing.can_be_converted_to_ascii(pattern_array):
            return PatternProcessing.convert_array_to_ascii(pattern_array)
        else:
            return None

    @staticmethod
    def convert_array_to_ascii(pattern_array: list[int]) -> str:
        """
        Convert the pattern array to an ASCII string
        """
        return ''.join([chr(i) for i in pattern_array])
    
    @staticmethod
    def can_be_converted_to_ascii(pattern_array: list[int]) -> bool:
        """
        Check if there is a pattern where the distance is above the 8-bit ascii limit
        """
        return min(pattern_array) < 256
    

    @staticmethod
    def get_sub_pattern(ascii_pattern: str) -> list[str]:
        """
        Get 16 subpatterns from the ASCII pattern
        """
        # Calculate the length of each subpattern
        subpattern_length = len(ascii_pattern) // 16

        # Initialize a list to store the subpatterns
        subpatterns = []

        # Iterate over the ASCII pattern in steps of subpattern length
        for i in range(0, len(ascii_pattern), subpattern_length):
            # Extract the current subpattern
            subpattern = ascii_pattern[i:i + subpattern_length]

            # Append the middle 5 characters of the subpattern to the list
            middle_start_index = (subpattern_length - 5) // 2
            middle_end_index = middle_start_index + 5
            middle_subpattern = subpattern[middle_start_index:middle_end_index]
            subpatterns.append(middle_subpattern)

        return subpatterns
    
    @staticmethod
    def get_image_sub_pattern(image_path: str, side: str) -> list[str]:
        """
        Get 16 subpatterns from the image
        """
        return PatternProcessing.get_sub_pattern(PatternProcessing.get_image_ascii_pattern(image_path, side))