import cv2
from cv2.typing import MatLike
import numpy as np
from numpy.typing import NDArray
from pathlib import Path
import pyautogui
from pynput import mouse
import random
from src.area import AreaSelector
from src.word_finder import WordFinder
import time


def get_arrow_location() -> list:
    input("When ready, press enter, then click the yellow arrow WHILE IT IS POINTING at your player.")

    pos: list = []
    def on_click(x, y, _, pressed):
        if pressed:
            pos.extend([x, y])
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join() #join so it blocks until click

    return pos


def get_letter_region() -> tuple | None:
    Path("logs/").mkdir(parents=True, exist_ok=True)

    input("Press enter when you are ready to select area for letters.")

    selector = AreaSelector()
    region = selector.get_selection()
    if not region:
        print("Could not get region from selection")
        return None

    return region


def get_letters_in_region(img: MatLike) -> str:
    return "hy"


def type_word(word: str):
    for c in word:
        pyautogui.press(c)
        time.sleep(random.random() / 100)


def bot_loop():
    mode = input("Enter mode (normal, shortest, longest): ").lower()
    if mode == "":
        mode = "normal"
    elif mode != "normal" and mode != "shortest" and mode != "longest":
        print("Invalid mode!")
        return
    
    word_finder = WordFinder(mode)
    arrow_location = get_arrow_location()
    arrow_color = pyautogui.pixel(arrow_location[0], arrow_location[1])
    letter_region = get_letter_region()

    while True:
        if pyautogui.pixel(arrow_location[0], arrow_location[1]) == arrow_color:
            screenshot = pyautogui.screenshot("logs/region_screenshot.png", region=letter_region)
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            letters = get_letters_in_region(img)

            word = word_finder.get_word(letters)
            print(f"Word found: {word}")
            type_word(word)
            time.sleep(0.35) #delay before checking again


def main():
    bot_loop()


if __name__ == "__main__":
    main()
