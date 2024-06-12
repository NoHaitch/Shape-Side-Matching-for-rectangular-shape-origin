class KMP:
    """
    Class to perform Knuth-Morris-Pratt algorithm string matching using the border function
    """

    @staticmethod
    def computeBorderFunction(pattern: str) -> list[int]:
        """
        Preprocess the pattern to compute the border array
        """
        m = len(pattern)
        border = [0] * m
        j = 0

        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = border[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            border[i] = j
        return border

    @staticmethod
    def KMPSearch(text: str, pattern: str) -> bool:
        """
        Perform Knuth-Morris-Pratt algorithm to find occurrences of the pattern in the text
        """
        if not pattern or not text:
            return False

        m = len(pattern)
        n = len(text)
        border = KMP.computeBorderFunction(pattern)

        i = 0 
        j = 0 

        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
                if j == m:
                    return True
            else:
                if j != 0:
                    j = border[j - 1]
                else:
                    i += 1

        return False
