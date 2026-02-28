# /ᐠ｡ꞈ｡ᐟ\
# can't open the file depending on the current map played.
# in main.adofai, there is a "song" line with the name of the map
# (maybe use image recognition on the bottom of the map once inside (the pause menue))

class Map_part():
    def __init__(self,name:str,angles:list[int],bpm:int,actions:list[str]|None) -> None:
        self.__name = name
        self.__bpm = bpm
        self.__angles = angles
        self.__actions = actions
        return
    def __str__(self) -> str:
        if self.__actions is None:
            return "name: " + str(self.__name) + ", angle number: " + str(len(self.__angles)) + ", bmp: " + str(self.__bpm) + ", action number: 0"
        return "name: " + str(self.__name) + ", angle number: " + str(len(self.__angles)) + ", bmp: " + str(self.__bpm) + ", action number: " + str(len(self.__actions))

def read(file:str)->str:
    opened_file = open(file,'r')
    content = opened_file.read()
    opened_file.close()
    return content

def scrap_angles(file:str)->list[int]:
    scraped_file = file.splitlines()
    scraped_file = scraped_file[1][15:-3].split(", ")
    scraped_int = []
    for i in scraped_file:
        scraped_int.append(int(i))
    return scraped_int

def scrap_bpm(file:str)->int: # err code : -1: bpm not found
    scraped_file = file.splitlines()
    for line in scraped_file:
        if "\t\t\"bpm\": " in line:
            return int(line[9:-2])
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


path = "C:\\Program Files (x86)\\Steam\\steamapps\\Workshop\\Content\\977950\\" + "2895342067\\" # path + game
main = read(path + "main.adofai")
main_angles = scrap_angles(main)
main_bpm = scrap_bpm(main)
main_actions = scrap_actions(main)
board = [Map_part("main", main_angles, main_bpm, main_actions)]

""" this part is for sub levels (tutos) please maintain this part of the program too
i = 1
while True:
    try :
        sub = read(path + "sub" + str(i) +".adofai")
    except FileNotFoundError:
        break
    sub_angles = scrap_angles(sub)
    sub_bpm = scrap_bpm(sub)
    sub_actions = scrap_actions(sub)
    board.append(Map_part("sub" + str(i), sub_angles, sub_bpm, sub_actions))
    i += 1
###############################################################################
"""
for i in board:
    print(i)