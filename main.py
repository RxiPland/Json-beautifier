# json beautifier
# python 3.9.12
# udělal RxiPland

from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog
import sys

from os import environ

environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"

class file_dialog(QDialog):

    def vyberLokace_raw(self):
        # otevře průzkumník souborů a nechá uživatele vybrat normální soubor, který se pak bude šifrovat
        try:

            dlg = QFileDialog.getOpenFileName(self, 'Vyberte soubor, který chcete zpracovat','','Všechny soubory (*.*);;Textový soubor (*.txt)')
            return str(dlg[0])

        except:
            return "exited"

    def vyberLokace_save(self):
        # otevře průzkumník souborů a nechá uživatele uložit nový soubor

        try:
            dlg = QFileDialog.getSaveFileName(self, 'Uložte hotový soubor', '','JSON soubor (*.json);;Textový soubor (*.txt);;Všechny soubory (*.*)')
            return str(dlg[0])

        except:
            return "exited"

        
def main():

    print("\n[1] Vyberte soubor, který chcete upravit...")

    cesta_raw = "!"

    while cesta_raw in ["!", "exited"]:
        cesta_raw = dialog.vyberLokace_raw()

    if not cesta_raw:
        sys.exit()

    with open(cesta_raw, "r") as file:
        obsah_raw = file.read()

    nazevSouboru = cesta_raw.split("/")

    print(f"[2] Soubor {nazevSouboru[-1]} byl načten")

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

    print("[3] JSON byl úspěšně upraven")

    print("[4] Uložte soubor...")

    cesta_save = "!"

    while cesta_save in ["!", "exited"]:
        cesta_save = dialog.vyberLokace_save()
        
    if not cesta_save:
        sys.exit()

    with open(cesta_save, "w") as file:
        file.write(final)

    nazevSouboru = cesta_save.split("/")

    print(f"[5] Soubor {nazevSouboru[-1]} byl úspěšně uložen")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = file_dialog()

    main()
    print("[6] Ukončuji program")

    sys.exit()