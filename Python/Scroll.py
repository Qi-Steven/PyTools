import pyautogui
import keyboard
def clicker():
    while not keyboard.is_pressed('esc'):
        pyautogui.scroll(300*-1)
        
def main():
    while True:
        keyboard.wait('home')
        clicker()
if __name__=='__main__':
    main()