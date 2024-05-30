import matplotlib.pyplot as plt


class Pattern:
    def __init__(self, left_pattern: list[int] | list[float], right_pattern: list[int] | list[float],
                 top_pattern: list[int] | list[float], bottom_pattern: list[int] | list[float]):
        self.left_pattern: list[int] | list[float] = left_pattern
        self.right_pattern: list[int] | list[float] = right_pattern
        self.top_pattern: list[int] | list[float] = top_pattern
        self.bottom_pattern: list[int] | list[float] = bottom_pattern
    
    @staticmethod
    def visualize_patterns(pattern1: list[int] | list[float], pattern2: list[int] | list[float]):
        """
        Visualizes two patterns represented by lists of integers in one window using Matplotlib.
        """
        max_distance = max(max(pattern1), max(pattern2))
        plt.figure(figsize=(10, 6))

        # Plot pattern 1
        plt.subplot(2, 1, 1)
        plt.plot(pattern1, color='blue', label='Pattern 1')
        plt.ylim(-max_distance, max_distance)
        plt.xlabel('Index')
        plt.ylabel('Distance')
        plt.title('Pattern Comparison')
        plt.grid(True)
        plt.legend()

        # Plot pattern 2
        plt.subplot(2, 1, 2)
        plt.plot(pattern2, color='red', label='Pattern 2')
        plt.ylim(-max_distance, max_distance)
        plt.xlabel('Index')
        plt.ylabel('Distance')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()
