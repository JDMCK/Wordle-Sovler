# Use this while on Wordlearchive.com
# Run in windowed full screen
# Scroll to top of page
# Run program in terminal NOT OBSTRUCTING GAMEBOARD

from PIL import ImageGrab
from pynput.keyboard import Key, Controller
import time
import random as rand

def getRowColors(row):
    # Screen captures board and returns num string in style of input
    GREY = (58, 58, 60, 255)
    YELLOW = (181, 159, 67, 255)
    GREEN = (82, 141, 82, 255)

    STARTINGX = 1110
    STARTINGY = 471
    DISTANCEX = 134
    DISTANCEY = 135

    cap = ImageGrab.grab()
    #cap.show()
    rowColors = ""
    # x starts at 1111
    # y starts at 472
    # 68 pixels between each box
    for c in range(5):
        pixel = cap.getpixel((c*DISTANCEX + STARTINGX, row*DISTANCEY + STARTINGY))
        #print(str(pixel) + " x = " + str(c*DISTANCEX + STARTINGX) + " y = " + str(row*DISTANCEY + STARTINGY))
        if pixel == GREY:
            rowColors += "0"
        elif pixel == YELLOW:
            rowColors += "1"
        elif pixel == GREEN:
            rowColors += "2"
    return rowColors

def getWordToPlay():

    # Processes input into dictionary
    nums = getRowColors(row)
    output = {"grey" : [], "yellow" : [], "green" : [],"yellowPos" : [], "greenPos" : []}
    for i in range(5):
        if nums[i] == '1':
            output["yellow"].append(word[i])
            output["yellowPos"].append(i)
        elif nums[i] == '0' and word[i] not in output["yellow"]:
            output["grey"].append(word[i])
        elif nums[i] == '2':
            output["green"].append(word[i])
            output["greenPos"].append(i)
    for i in output["grey"]:
        if i in output["green"] or i in output["yellow"]:
            output["grey"].remove(i)  
    return output

def filter(specs, answers):

    def multiIn(find, source):
        # Returns true if all finds are in source
        # Returns false if any finds are not in source
        for i in find:
            if i not in source:
               return False
        return True

    def multiOut(find, source):
        # Returns true if all finds are not in source
        # Returns false if any finds are in source
        for i in find:
            if i in source:
                return False
        return True

    def yellowFilter(find, spot, source):
        # Returns false if find is in spot at source
        for i in range(len(find)):
            if find[i] in source[spot[i]]:
                return False
        return True

    def greenFilter(find, spot, source):
        # Returns false if find is not in spot at source
        for i in range(len(find)):
            if find[i] not in source[spot[i]]:
                return False
        return True

    # Filter Grey
    answers = [i for i in answers if multiOut(specs["grey"], i)]

    # Filter Yellow
    answers = [i for i in answers if multiIn(specs["yellow"], i)]
    answers = [i for i in answers if yellowFilter(specs["yellow"], specs["yellowPos"], i)]

    # Filter Green
    answers = [i for i in answers if greenFilter(specs["green"], specs["greenPos"], i)]

    return answers

# Reads answers file
with open('WordleAnswers.txt', 'r') as f:
    answers = f.read().split()

row = 0
word = rand.choice(['slice', 'tried', 'crane'])
print(word)
keyboard = Controller()

# Instructions
print("Please click into the Wordle window and wait.")
time.sleep(2)
# Gameloop
for _ in range(6):

    # Enter Word
    for ch in word:
        keyboard.press(ch)
        keyboard.release(ch)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(2)

    # Calculate Next Word
    attempt = getWordToPlay()
    row += 1
    if len(attempt["green"]) == 5:
        print("Success")
        break
    answers = filter(attempt, answers)
    word = answers[0]
    print(answers[:5])
