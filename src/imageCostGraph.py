import os
from imageSimilarity import ImageSimilarity


class ImageCostGraph:
    """
    Create a cost graph using puzzle pieces similarity.
    """

    @staticmethod
    def load_images(folder_path: str) -> list[tuple[str, str]]:
        """
        Get images from a folder.
        :return: List of pairs (filename, image_path).
        """
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                images.append((filename, image_path))
        return images

    @staticmethod
    def create_cost_graph(folder_path: str) -> dict[str, dict[str, float]]:
        """
        Create a cost graph using puzzle pieces similarity.
        :return: Cost graph.
        """
        images = ImageCostGraph.load_images(folder_path)
        graph = {}
        for i, (name1, path1) in enumerate(images):
            graph[name1] = {}
            for j, (name2, path2) in enumerate(images):
                if i != j:
                    alignment_percentage = ImageSimilarity.puzzle_alignment(path1, path2)
                    graph[name1][name2] = alignment_percentage
        return graph

    @staticmethod
    def print_cost_graph(cost_graph: dict[str, dict[str, float]]) -> None:
        """
        Print the cost graph.
        """
        for key, value in cost_graph.items():
            print(f"{key}: {value}")
