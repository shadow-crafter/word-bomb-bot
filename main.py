
class WordFinder:
    def __init__(self, mode: str):
        self.ignore_list: list[str] = []
        self.mode = mode

    def get_word(self, letters: str) -> str:
        selected_word = ""
        with open("word-list.txt", "r") as f:
            for line in f:
                l = line.strip().lower()
                if letters in l and not l in self.ignore_list:
                    if self.mode == "normal":
                        selected_word = l
                        break
                    elif self.mode == "longest":
                        selected_word = l if len(l) > len(selected_word) else selected_word
                    elif self.mode == "shortest":
                        selected_word = l if len(l) < len(selected_word) else selected_word

        self.ignore_list.append(selected_word)
        return selected_word

def main():
    word_finder = WordFinder("longest")
    for _ in range(50):
        print(f"word: {word_finder.get_word("hyper")}")


if __name__ == "__main__":
    main()
