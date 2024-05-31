import networkx as nx
import matplotlib.pyplot as plt

from imageProcessing import ImageProcessing
from imageSimilarity import ImageSimilarity
from pattern import Pattern


class ImageGraph:
    @staticmethod
    def create_similarity_graph(img1_path, img2_path):
        """
        Create a similarity graph between two images.
        """

        # Extract edge pattern and color pattern
        patterns_img1: tuple[Pattern, Pattern] = ImageProcessing.extract_edges_pattern(img1_path)
        patterns_img2: tuple[Pattern, Pattern] = ImageProcessing.extract_edges_pattern(img2_path)

        edge_pattern1, color_pattern1 = patterns_img1
        edge_pattern2, color_pattern2 = patterns_img2
        
        graph = nx.Graph()

        # create a node for each side of the image
        sides = ["left", "right", "top", "bottom"]
        for side1 in sides:
            for side2 in sides:
                side_edge_pattern1: list[int] = getattr(edge_pattern1, f"{side1}_pattern")
                side_edge_pattern2: list[int] = getattr(edge_pattern2, f"{side2}_pattern")

                side_color_pattern1: list[float] = getattr(color_pattern1, f"{side1}_pattern")
                side_color_pattern2: list[float] = getattr(color_pattern2, f"{side2}_pattern")
                
                if len(set(side_edge_pattern1)) == 1 and len(set(side_edge_pattern2)) == 1:
                    similarity = 0.0
                else:
                    similarity = ImageSimilarity.combined_similarity((side_edge_pattern1, side_color_pattern1),
                                                                     (side_edge_pattern2, side_color_pattern2))

                # Add edge to the graph
                graph.add_edge(f"{side1}_img1", f"{side2}_img2", weight=similarity)

        return graph
    
    @staticmethod
    def combined_similarity(pattern1: tuple[list[int], list[float]],
                            pattern2: tuple[list[int], list[float]],
                            edge_weight: float = 0.7) -> float:
        """
        Combine edge similarity and color similarity into a uniform similarity.
        """
        edge_pattern1, color_pattern1 = pattern1
        edge_pattern2, color_pattern2 = pattern2

        # Get edge pattern similarity
        edge_similarity = ImageSimilarity.pattern_similarity(edge_pattern1, edge_pattern2)
        
        # Get color pattern similarity
        color_similarity = ImageSimilarity.color_similarity(color_pattern1, color_pattern2)

        weight_sum = edge_weight + (1 - edge_weight)
        combined_similarity = (edge_weight * edge_similarity + (1 - edge_weight) * color_similarity) / weight_sum
        return combined_similarity
    
    @staticmethod
    def visualize_graph(graph: nx.Graph):
        """
        Visualize the similarity graph.
        """
        layout = nx.spring_layout(graph)
        nx.draw(graph, layout, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, layout, edge_labels=edge_labels)
        plt.title("Similarity Graph")
        plt.show()
        plt.show()
