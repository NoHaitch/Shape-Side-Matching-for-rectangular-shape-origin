class BM:
    """
    Class to perform Boyer-Moore algorithm string matching using the last occurrence table
    """

    @staticmethod
    def preprocess_last_occurrence(pattern: str) -> dict[str, int]:
        """
        Preprocess the pattern to create the last occurrence table
        """
        last_occurrence = {}
        m = len(pattern)
        for i in range(m):
            last_occurrence[pattern[i]] = i
        return last_occurrence

    @staticmethod
    def bm_search(text: str, pattern: str) -> bool:
        """
        Perform Boyer-Moore algorithm to find occurrences of the pattern in the text
        """
        if not pattern or not text:
            return False

        m = len(pattern)
        n = len(text)
        last_occurrence = BM.preprocess_last_occurrence(pattern)

        i = 0
        while i <= n - m:
            j = m - 1            
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                return True
            else:
                char_shift = last_occurrence.get(text[i + j], -1)
                i += max(1, j - char_shift)
        return False
