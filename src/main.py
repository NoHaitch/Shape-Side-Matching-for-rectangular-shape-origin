from pattern import Pattern
from imageProcessing import ImageProcessing
from imageSimilarity import ImageSimilarity

def main():
    img1 = "puzzle_piece-1.png"
    img2 = "puzzle_piece-2.png"
    img3 = "puzzle_piece-5.png"
    patterns = ImageProcessing.process_images_in_folder("puzzles/dog")

    print("Pattern Similarity: ", ImageSimilarity.pattern_similarity(patterns[img1][0].bottom_pattern, patterns[img2][0].top_pattern))
    print("Color Similarity: ", ImageSimilarity.color_similarity(patterns[img1][1].bottom_pattern, patterns[img2][1].top_pattern))
    print("Combined Similarity: ", ImageSimilarity.combined_similarity([patterns[img1][0].bottom_pattern, patterns[img1][1].bottom_pattern], [patterns[img2][0].top_pattern, patterns[img2][1].top_pattern]))

    print("")

    print("Pattern Similarity: ", ImageSimilarity.pattern_similarity(patterns[img1][0].bottom_pattern, patterns[img3][0].left_pattern))
    print("Color Similarity: ", ImageSimilarity.color_similarity(patterns[img1][1].bottom_pattern, patterns[img3][1].left_pattern))
    print("Combined Similarity: ", ImageSimilarity.combined_similarity([patterns[img1][0].bottom_pattern, patterns[img1][1].bottom_pattern], [patterns[img3][0].left_pattern, patterns[img3][1].left_pattern]))

if __name__ == "__main__":
    main()