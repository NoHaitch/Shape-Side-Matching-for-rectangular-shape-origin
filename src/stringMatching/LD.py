class LD:
    """
    Class to calculate string similarity using Levenshtein Distance
    """

    @staticmethod
    def levenshtein_distance(str1: str, str2: str) -> int:
        """
        Compute the Levenshtein Distance between two strings
        """
        len_str1 = len(str1)
        len_str2 = len(str2)

        # Create a matrix to store the distances
        dp = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

        # Initialize the first row and column of the matrix
        for i in range(len_str1 + 1):
            dp[i][0] = i
        for j in range(len_str2 + 1):
            dp[0][j] = j

        # Fill the matrix with the Levenshtein Distance values
        for i in range(1, len_str1 + 1):
            for j in range(1, len_str2 + 1):
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = 1
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

        # Return the Levenshtein Distance between the two strings
        return dp[len_str1][len_str2]

    @staticmethod
    def similarity_score(str1: str, str2: str) -> float:
        """
        Compute the similarity score between two strings using Levenshtein Distance
        """
        max_length = max(len(str1), len(str2))
        if max_length == 0:
            return 1.0
        distance = LD.levenshtein_distance(str1, str2)
        return 1.0 - distance / max_length
