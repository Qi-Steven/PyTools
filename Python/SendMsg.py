import pyautogui
import pyperclip
import time
import pandas as pd
excel_path="C:\\Users\\QQ\\Desktop\\Python\\SendMsg.xlsx"
df= pd.read_excel(excel_path)
pyautogui.hotkey('ctrl','alt','w')
oldfriend='0'
for index,row in df.iterrows():
    friend=row['friend']
    msg=row['msg']
    time.sleep(1)
    if(friend==oldfriend):
        print(oldfriend)
    else:
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl','f')
        pyperclip.copy(friend)
        pyautogui.hotkey('ctrl','v')
        oldfriend=friend
        pyautogui.press('enter')
        pyperclip.copy('账户恢复')
        pyautogui.hotkey('ctrl','v')
    time.sleep(1)
    pyautogui.hotkey('ctrl','enter')
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl','v')
    # pyautogui.press('enter')

    
