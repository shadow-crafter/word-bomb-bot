import random

class WordFinder:
    def __init__(self, mode: str):
        self.ignore_list: list[str] = []
        self.mode = mode

    def get_word(self, letters: str) -> str:
        selected_word = ""
        candidates = []
        with open("word-list.txt", "r") as f:
            for line in f:
                l = line.strip().lower()
                if letters in l and not l in self.ignore_list:
                    if self.mode == "normal":
                        selected_word = l
                        break
                    elif self.mode == "longest" or self.mode == "shortest":
                            candidates.append(l)

        if self.mode == "longest" and candidates:
            max_length = max(len(word) for word in candidates)
            longest_words = [w for w in candidates if len(w) == max_length]
            selected_word = random.choice(longest_words)
        elif self.mode == "shortest" and candidates:
            min_length = min(len(word) for word in candidates)
            shortest_words = [w for w in candidates if len(w) == min_length]
            selected_word = random.choice(shortest_words)
        
        self.ignore_list.append(selected_word)
        return selected_word
