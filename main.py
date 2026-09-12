import cv2
from cv2.typing import MatLike
import numpy as np
from numpy.typing import NDArray
from pathlib import Path
import pyautogui
from src.area import AreaSelector
from src.word_finder import WordFinder

def get_image() -> MatLike | None:
    Path("logs/").mkdir(parents=True, exist_ok=True)

    input("Press enter when you are ready to select area for words.")

    selector = AreaSelector()
    region = selector.get_selection()
    if not region:
        print("Could not get region from selection")
        return None

    screenshot = pyautogui.screenshot("logs/region_screenshot.png", region=region)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    return img

def main():
    word_finder = WordFinder("shortest")
    for _ in range(50):
        print(f"word: {word_finder.get_word("hyper")}")

    get_image()


if __name__ == "__main__":
    main()
