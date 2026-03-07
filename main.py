# /ᐠ｡ꞈ｡ᐟ\
# can't open the file depending on the current map played.
# in main.adofai, there is a "song" line with the name of the map
# (maybe use image recognition on the bottom of the map once inside (the pause menue))

import keyboard,time

class Map_part():
    def __init__(self,name:str,angles:list[float],bpm:int,actions:list[tuple]|None) -> None:
        self.__name = name
        self.__bpm = bpm
        self.__angles = angles
        self.__actions = actions
        return
    
    def get_angles(self)->list[float]:
        return self.__angles
    
    def get_bpm(self)->int:
        return self.__bpm
    
    def get_actions(self)->list[tuple]|None:
        return self.__actions

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
            if "\"Twirl\"" in scraped_file[i]:
                type = "Twirl"
                floor_number = int(scraped_file[i][13:scraped_file[i].find(",")])
                scrap_list.append((type, floor_number))
            elif "\"SetSpeed\"" in scraped_file[i]:
                type = "SetSpeed"
                floor_number = int(scraped_file[i][13:scraped_file[i].find(",")])
                bpm = float(scraped_file[i][find_sub_str(scraped_file[i],",",3)+20:find_sub_str(scraped_file[i],",",4)])
                bpm_mult = float(scraped_file[i][find_sub_str(scraped_file[i],",",4)+19:find_sub_str(scraped_file[i],",",5)])
                scrap_list.append((type,floor_number,bpm,bpm_mult)) # (type, floor number, bpm, bpm mult)
    
    if len(scrap_list) == 0:
        return None
    return scrap_list[2:]

def find_sub_str(string:str,sub_string:str,occurence:int=1)->int:
        if not(sub_string in string):
            return 0
        if occurence == 1:
            return string.find(sub_string)
        add = string.find(sub_string)+1
        return find_sub_str(string[add:],sub_string,occurence-1) + add
#MODIF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def calcul_timing(map_part:Map_part,current_tile:int,twirl:bool)->float: # "err code" 100: angle not supported
    current_angle = map_part.get_angles()[current_tile - 1]
    next_angle = map_part.get_angles()[current_tile]
    if current_angle == next_angle:
            return 1
    if twirl:
        if next_angle == current_angle - 45:
            return 0.75
        elif next_angle == current_angle + 45:
            return 1.25
        elif next_angle == current_angle - 90:
            return 0.5
        elif next_angle == current_angle + 90:
            return 1.5
        elif next_angle == current_angle - 135:
            return 0.25
        elif next_angle == current_angle + 135:
            return 1.75
    #else
    if next_angle == current_angle + 45:
        return 0.75
    elif next_angle == current_angle - 45:
        return 1.25
    elif next_angle == current_angle + 90:
        return 0.5
    elif next_angle == current_angle - 90:
        return 1.5
    elif next_angle == current_angle + 135:
        return 0.25
    elif next_angle == current_angle - 135:
        return 1.75
    
    print("calcul_timing: err code 100")
    return 100

# kawaii... = 2895342067
path = "C:\\Program Files (x86)\\Steam\\steamapps\\Workshop\\Content\\977950\\" + "3018063128\\" # game path + map
board = take_board(path)
twirl = False

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
    timing = calcul_timing(board[-1],current_tile,twirl) # temp, main used
    if time.time() - start >= (1/(board[-1].get_bpm()/60))*timing:
        start = time.time()
        keyboard.press_and_release('j')
        for action in board[-1].get_actions():
            if action[1] == current_tile:
                #aply effect
                if action[0] == "Twirl":
                    if twirl == True:
                        twirl = False
                    else:
                        twirl = True
                if action[0] == "SetSpeed":
                    bpm = action[2] * action[3]
                print(action)
    
        current_tile += 1
        