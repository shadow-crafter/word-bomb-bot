from src.word_finder import WordFinder

def main():
    word_finder = WordFinder("shortest")
    for _ in range(50):
        print(f"word: {word_finder.get_word("hyper")}")


if __name__ == "__main__":
    main()
