from pathlib import Path
from PIL import ImageOps, ImageEnhance
import pyautogui
from pynput import mouse
import pytesseract
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
    input("Press enter when you are ready to select area for letters.")

    selector = AreaSelector()
    region = selector.get_selection()
    if not region:
        print("Could not get region from selection")
        return None

    return region


def get_letters_in_region(img) -> str:
    text = pytesseract.image_to_string(img, config=r'--psm 7').strip()
    print(f"Letters found: {text}")
    return text


def type_word(word: str):
    for c in word:
        pyautogui.press(c)
        time.sleep(random.random() / 100)
    time.sleep(0.05 + random.random() / 100)
    pyautogui.press("enter")


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
            Path("logs/").mkdir(parents=True, exist_ok=True)
            screenshot = pyautogui.screenshot("logs/region_screenshot.png", region=letter_region)
            img_gray = ImageOps.grayscale(screenshot)
            img = ImageEnhance.Contrast(img_gray).enhance(2.0)
            letters = get_letters_in_region(img)

            word = word_finder.get_word(letters)
            print(f"Word found: {word}")
            type_word(word)
            time.sleep(0.35) #delay before checking again


def main():
    bot_loop()


if __name__ == "__main__":
    main()
