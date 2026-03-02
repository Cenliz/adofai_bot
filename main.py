# /ᐠ｡ꞈ｡ᐟ\
# can't open the file depending on the current map played.
# in main.adofai, there is a "song" line with the name of the map
# (maybe use image recognition on the bottom of the map once inside (the pause menue))

import keyboard,time

class Map_part():
    def __init__(self,name:str,angles:list[float],bpm:int,actions:list[str]|None) -> None:
        self.__name = name
        self.__bpm = bpm
        self.__angles = angles
        self.__actions = actions
        return
    
    def get_angles(self)->list[float]:
        return self.__angles
    
    def get_bpm(self)->int:
        return self.__bpm

    def __str__(self) -> str:
        if self.__actions is None:
            return "name: " + str(self.__name) + ", angle number: " + str(len(self.__angles)) + ", bmp: " + str(self.__bpm) + ", action number: 0"
        return "name: " + str(self.__name) + ", angle number: " + str(len(self.__angles)) + ", bmp: " + str(self.__bpm) + ", action number: " + str(len(self.__actions))

def take_board(path:str)->list[Map_part]:
    board = []
    """ this part is for sub levels (tutos) please maintain this part of the program too
    i = 1
    while True:
        try :
            sub = read(path + "sub" + str(i) +".adofai")
        except FileNotFoundError:
            break
        sub_name = scrap_name(sub)
        sub_angles = scrap_angles(sub)
        sub_bpm = scrap_bpm(sub)
        sub_actions = scrap_actions(sub)
        board.append(Map_part(sub_name, sub_angles, sub_bpm, sub_actions))
        i += 1
    """
    main = read(path + "main.adofai")
    main_name = scrap_name(main)
    main_angles = scrap_angles(main)
    main_bpm = scrap_bpm(main)
    main_actions = scrap_actions(main)
    board.append(Map_part(main_name, main_angles, main_bpm, main_actions))
    return board

def read(file:str)->str:
    opened_file = open(file,encoding="UTF-8")
    content = opened_file.read()
    opened_file.close()
    return content

def scrap_name(file:str)->str|int: # err code 1: name not found
    scraped_file = file.splitlines()
    for line in scraped_file:
        if "\t\t\"song\": \"" in line:
            return line[11:-3]
    return 1

def scrap_angles(file:str)->list[float]:
    scraped_file = file.splitlines()
    scraped_file = scraped_file[1][15:-3].split(", ")
    scraped_int = []
    for i in scraped_file:
        scraped_int.append(float(i))
    return scraped_int

def scrap_bpm(file:str)->int: # err code : -1: bpm not found
    scraped_file = file.splitlines()
    for line in scraped_file:
        if "\t\t\"bpm\": " in line:
            return int(line[9:-2])
    print("scrap_bpm: err code -1")
    return -1

def scrap_actions(file:str)->list[str]|None:
    scraped_file = file.splitlines()
    scrap_list = []
    for i in range(len(scraped_file)):
        if scraped_file[i] == "\t\"actions\":":
            scrap_list.append(scraped_file[i])
            i += 1
        if scraped_file[i] == "\t]":
            break
        if len(scrap_list) >= 1:
            scrap_list.append(scraped_file[i])
    
    if len(scrap_list) == 0:
        return None
    return scrap_list[2:]

def calcul_timing(map_part:Map_part,current_tile:int): # "err code" 100: angle not supported
    a = map_part.get_angles()[current_tile - 1] + map_part.get_angles()[current_tile]
    if a == map_part.get_angles()[current_tile - 1]:
        return 1
    print("calcul_timing: err code 100")
    return 100

# kawaii... = 2895342067
path = "C:\\Program Files (x86)\\Steam\\steamapps\\Workshop\\Content\\977950\\" + "3018063128\\" # game path + map
board = take_board(path)

###############################################################################
for i in board:
    print(i)
###############################################################################

keyboard.wait('s') # start
start = time.time()
current_tile = 1 # manual start

while True:
    if keyboard.is_pressed('f'): # fail safe
        break
    timing = calcul_timing(board[-1],current_tile) # temp, main used
    if time.time() - start >= (1/(board[-1].get_bpm()/60))*timing:
        start = time.time()
        keyboard.press_and_release('j')
        current_tile += 1
        