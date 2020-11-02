import pyautogui as g
from time import sleep


class OpenYT:

    w, h = g.size()

    def __init__(self):
        self.move_to(2, self.h-1)
        self.click_btn()
        self.write_text(' YouTube Music')
        self.press_enter()
        sleep(2)
        self.move_to(self.w*0.3, self.h*0.3)
        sleep(3)
        self.click_btn()

    def move_to(self, width, height):
        g.moveTo(width, height)

    def click_btn(self):
        g.click()

    def write_text(self, text):
        g.write(text, interval=0.25)

    def press_enter(self):
        g.press('enter')


open_now = OpenYT()
