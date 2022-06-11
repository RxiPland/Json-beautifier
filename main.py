# json beautifier

from os import system, getcwd
from os.path import exists

soubor_raw = input("Zadejte soubor: ")

if not exists(soubor_raw):

    soubor_raw = getcwd() + "\\" + soubor_raw

f_raw = open(soubor_raw, "r")
obsah_raw = f_raw.read()
f_raw.close()

final = ""              # pomocná proměnná do které for zapisuje postupně znak po znaku
i = 0                   # počet /t (tab) odsazení -> bude se postupně vnořovat
uvozovky_lock = False   # false == mimo uvozovky;  true == v uvozovkách

for x, character in enumerate(obsah_raw):

    if character in ["\'", "\""]:
        if uvozovky_lock == False:
            uvozovky_lock = True
        else:
            uvozovky_lock = False

        final += character
    
    elif character == ":" and uvozovky_lock == False:
        if obsah_raw[x] == " ":
            pass
        else:
            character += ' '

        final += character

    elif character == "{" and uvozovky_lock == False:
        final += "{\n" + "\t"*(i+1)
        i += 1

    elif character == "}" and uvozovky_lock == False:
        i -= 1
        final += "\n" + "\t"*i + "}"

    elif character == "," and uvozovky_lock == False:
        final += "," + "\n" + "\t"*i

    elif character == "[" and uvozovky_lock == False:
        if obsah_raw[x+1] == "]":
            final += character
        else:
            i += 1
            final += "[" + "\n" + "\t"*i

    elif character == "]" and uvozovky_lock == False:
        if obsah_raw[x-1] == "[":
            final += character
        else:
            i -= 1
            final += "\n" + "\t"*i + "]"

    else:
        final += character

f_done = open("done.json", "w")
f_done.write(final)
f_done.close()