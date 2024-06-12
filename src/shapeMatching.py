from stringMatching.KMP import KMP
from stringMatching.BM import BM
from stringMatching.LD import LD
from patternProcessing import PatternProcessing


class ShapeMatching:
    """
    Class for shape matching
    """

    @staticmethod
    def shape_match_kmp(img_path: str, side: str, dataset_pattern: dict[str, dict[str, str]]) -> str:
        """
        Find the shapes from the dataset with the most weight using KMP
        """
        sub_patterns = PatternProcessing.get_image_sub_pattern(img_path, side)
        max_count = 0
        best_matches = []

        for image_name, pattern_data in dataset_pattern.items():

            for pattern_side, pattern in pattern_data.items():
                total_count = 0

                for sub_pattern in sub_patterns:
                    if KMP.kmp_search(pattern, sub_pattern):
                        total_count += 1

                if total_count > max_count:
                    max_count = total_count
                    best_matches.clear()
                    best_matches.append(image_name+"/"+pattern_side)
                
                elif total_count == max_count:
                    best_matches.append(image_name+"/"+pattern_side)

        if max_count > 6:
            if len(best_matches) == 1:
                return best_matches[0]

        return ShapeMatching.shape_match_ld(img_path, side, dataset_pattern)
    
    @staticmethod
    def shape_match_bm(img_path: str, side: str, dataset_pattern: dict[str, dict[str, str]]) -> str:
        """
        Find the shapes from the dataset with the most weight using BM
        """
        sub_patterns = PatternProcessing.get_image_sub_pattern(img_path, side)
        max_count = 0
        best_matches = []

        for image_name, pattern_data in dataset_pattern.items():

            for pattern_side, pattern in pattern_data.items():
                total_count = 0

                for sub_pattern in sub_patterns:
                    if BM.bm_search(pattern, sub_pattern):
                        total_count += 1

                if total_count > max_count:
                    max_count = total_count
                    best_matches.clear()
                    best_matches.append(image_name+"/"+pattern_side)
                
                elif total_count == max_count:
                    best_matches.append(image_name+"/"+pattern_side)

        if max_count > 6:
            if len(best_matches) == 1:
                return best_matches[0]

        return ShapeMatching.shape_match_ld(img_path, side, dataset_pattern)
    
    @staticmethod
    def shape_match_ld(img_path: str, side: str, dataset_pattern: dict[str, dict[str, str]]) -> str:
        """
        Find the shapes from the dataset with the highest similarity score using Levenshtein Distance
        """
        pattern = PatternProcessing.get_image_ascii_pattern(img_path, side)
        max_similarity = 0
        best_matches = []

        for image_name, pattern_data in dataset_pattern.items():
            for pattern_side, dataset_pattern in pattern_data.items():
                similarity_score = LD.similarity_score(dataset_pattern, pattern)
                if similarity_score > max_similarity:
                    max_similarity = similarity_score
                    best_matches.clear()
                    best_matches.append(image_name + "/" + pattern_side)
                elif similarity_score == max_similarity:
                    best_matches.append(image_name + "/" + pattern_side)

        return best_matches[0]
