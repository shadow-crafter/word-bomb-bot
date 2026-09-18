import cv2
import numpy as np
from pathlib import Path
import pyautogui
import pydirectinput
from pynput import mouse
import pytesseract
import random
from src.area import AreaSelector
from src.word_finder import WordFinder
import time


PANIC_LIST = list("eariotnslcudpmhgbfywkvxzjq")

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
    input("Press enter when you are ready to select area for letters.")

    selector = AreaSelector()
    region = selector.get_selection()
    if not region:
        print("Could not get region from selection")
        return None

    return region


def get_letters_in_region(screenshot) -> str:
    img_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(img_resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.floodFill(thresh, None, (0, 0), 255)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)) # Clean up
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    #cv2.imshow("debug", thresh)
    #cv2.waitKey()

    config = r'--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text: str = pytesseract.image_to_string(thresh, config=config).strip().lower().replace(" ", "")
    print(f"Letters found: {text}")
    return text


def type_word(word: str):
    pydirectinput.PAUSE = 0.01
    
    time.sleep(0.1 + random.random() * 0.35)
    for c in word:
            pydirectinput.press(c)
            time.sleep(0.025 + random.random() * 0.05)
    time.sleep(0.1 + random.random() * 0.2)
    pydirectinput.press("enter")


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
    panic_letters: list[str] = []
    panic_letters.extend(PANIC_LIST)

    print("Starting bot, focus window...")
    time.sleep(1) # Time so you can click in window
    while True:
        if pyautogui.pixel(arrow_location[0], arrow_location[1]) == arrow_color:
            Path("logs/").mkdir(parents=True, exist_ok=True)
            screenshot = pyautogui.screenshot("logs/region_screenshot.png", region=letter_region)

            letters = get_letters_in_region(screenshot)
            if len(letters) > 1:
                panic_letters.extend(PANIC_LIST) # reset
                word = word_finder.get_word(letters)
                print(f"Word found: {word}")
                type_word(word)
            else: # PANIC MODE!! Shouldn't detect <= one letter
                if len(panic_letters) == 0: #unlikely, but just in case
                    panic_letters.extend(PANIC_LIST)
                letters += panic_letters[0]
                panic_letters.pop(0)
                word = word_finder.get_word(letters, panic=True)
                print(f"Panicking!!! Word found: {word}")
                type_word(word)
            time.sleep(0.35) #delay before checking again


def main():
    bot_loop()


if __name__ == "__main__":
    main()
