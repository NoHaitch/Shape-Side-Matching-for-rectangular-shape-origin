from imageGraph import ImageGraph


def main():
    img1 = "puzzle_piece-1.png"
    img2 = "puzzle_piece-2.png"
    graph = ImageGraph.create_similarity_graph("puzzles/dog/" + img1, "puzzles/dog/" + img2)
    ImageGraph.visualize_graph(graph)


if __name__ == "__main__":
    main()
