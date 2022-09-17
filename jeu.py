from colorama import Fore, Back, Style, deinit, init, Cursor
from msvcrt import getch
from random import*

from pygame import quit

nb_cases_x = 10
nb_cases_y = 10

player_x = nb_cases_y - 1
player_y = nb_cases_x // 2


mob_x = [0, 0]
mob_y = [0, nb_cases_x - 1]

#mob_x = [0, 0, nb_cases_x - 1, nb_cases_x - 1]
#mob_y = [0, nb_cases_y - 1, 0, nb_cases_y - 1]

compteur_tour = 0
compteur_points = 0

piece_x = randint(0, nb_cases_x - 1)
piece_y = randint(0, nb_cases_y - 1)

try:
    r = open('high_score.txt')
    lecture_txt = r.readlines()
    lecture_separe = lecture_txt[0].split()
    r.close()
except:
    lecture_separe = ['0', '0', '0']

def actualisation():
    print(Cursor.POS(0, 0))
    print("—————————————————————————————")
    for y in range(nb_cases_y):
        for x in range(nb_cases_x):
            mob_nb = 0
            for i in range(len(mob_x)):
                if x == mob_x[i] and y == mob_y[i]:
                    mob_nb += 1
            if mob_nb >= 1:
                if mob_nb == 1:
                    print(Fore.YELLOW + " " + str(mob_nb) + " " + Style.RESET_ALL, end="")
                elif mob_nb == 2:
                    print(Fore.MAGENTA + " " + str(mob_nb) + " " + Style.RESET_ALL, end="")
                else:
                    print(Fore.RED + " " + str(mob_nb) + " " + Style.RESET_ALL, end="")
            elif x == player_x and y == player_y:
                print(Fore.BLUE + " ● " + Style.RESET_ALL, end="")
            elif compteur_tour >= 2 and x == piece_x and y == piece_y:
                print(Fore.GREEN + " * " + Style.RESET_ALL, end="")
            else:
                print(" . " + Style.RESET_ALL, end="")
        print("")
    print(Cursor.POS(35, 7) + Fore.BLUE + 'Le record est de ' + Fore.CYAN + Style.BRIGHT + lecture_separe[2] + Style.RESET_ALL + Fore.BLUE + ' points avec ' + Fore.CYAN + Style.BRIGHT + lecture_separe[1] + Style.RESET_ALL + Fore.BLUE + ' monstres (' + Fore.CYAN + Style.BRIGHT + lecture_separe[0] + Style.RESET_ALL + Fore.BLUE + ' tours)' + Style.RESET_ALL)
    print(Cursor.POS(35, 9) + Style.BRIGHT + Fore.BLUE + "Infos :" + Style.RESET_ALL, "Tour :", compteur_tour + 1, "– Monstres :", len(mob_x), '– Points :', compteur_points)
    print(Cursor.POS(0, nb_cases_y + 2))

def deplacement_mob():
    global mob_x, mob_y
    for i in range(len(mob_x)):
        if mob_x[i] < player_x and mob_y[i] == player_y:
            # Si le mob est sur la même ligne à gauche du player
            mob_x[i] += 1
        elif mob_x[i] > player_x and mob_y[i] == player_y:
            # Si le mob est sur la même ligne à droite du player
            mob_x[i] -= 1
        elif mob_x[i] == player_x and mob_y[i] < player_y:
            # Si le mob est sur la même ligne à droite du player6
            mob_y[i] += 1
        elif mob_x[i] == player_x and mob_y[i] > player_y:
            # Si le mob est sur la même ligne à droite du player
            mob_y[i] -= 1
    
        elif mob_x[i] < player_x and mob_y[i] < player_y:
            # Si le mob est en haut à gauche du player
            if randint(0, 1) == 1:
                mob_x[i] += 1
            else:
                mob_y[i] += 1
        elif mob_x[i] > player_x and mob_y[i] < player_y:
            # Si le mob est en haut à droite du player
            if randint(0, 1) == 1:
                mob_x[i] -= 1
            else:
                mob_y[i] += 1
        elif mob_x[i] > player_x and mob_y[i] > player_y:
            # Si le mob est en bas à droite du player
            if randint(0, 1) == 1:
                mob_x[i] -= 1
            else:
                mob_y[i] -= 1
        elif mob_x[i] < player_x and mob_y[i] > player_y:
            # Si le mob est en bas à gauche du player
            if randint(0, 1) == 1:
                mob_x[i] += 1
            else:
                mob_y[i] -= 1


def deplacement_player():
    global player_x, player_y
    # print("Saisissez g, d, b, h")
    move = getch().lower()
    if move == b'q':
        if player_x != 0:
            player_x -= 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b'd':
        if player_x != nb_cases_x-1:
            player_x += 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b'z':
        if player_y != 0:
            player_y -= 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b's':
        if player_y != nb_cases_y-1:
            player_y += 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b'e':
        direction_laser = getch().lower()
        if direction_laser == b'q':
            rayon_left()
        else:
            print("Direction invalide, il faut taper z,q,s,d")
    else:
        print("Déplacement invalide, il faut taper z,q,s,d")

def test_collision():
    global compteur_points, piece_x, piece_y
    # on compare les postitions des mobs avec celle du joueur
    for i in range(len(mob_x)):
        if player_y == mob_y[i] and player_x == mob_x[i]:
            if compteur_points > int(lecture_separe[2]):
                with open('high_score.txt', 'w') as r:
                    r.write(str(compteur_tour) + ' ' + str(len(mob_x)) + ' ' + str(compteur_points))
            exit('╠═══╍╍ Vous avez perdu ╍╍═══╣')
        elif player_x == piece_x and player_y == piece_y:
            compteur_points += 1
            piece_x = randint(0, nb_cases_x - 1)
            piece_y = randint(0, nb_cases_y - 1)

def ajout_mob():
    global mob_x, mob_y
    if compteur_tour % 10 == 0:
        mob_x.append(choices([0, nb_cases_x])[0])
        mob_y.append(choices([0, nb_cases_y])[0])

def rayon_left():
    global mob_x, mob_y
    mob_a_enlever = []
    for i in range(len(mob_x)):
        if mob_x[i] < player_x and mob_y[i] == player_y:
            mob_a_enlever.append(i)
    mob_x = [x for i, x in enumerate(mob_x) if i not in mob_a_enlever]
    mob_y = [y for i, y in enumerate(mob_y) if i not in mob_a_enlever]

def main():
    global player_x, player_y, compteur_tour
    print('\033[3C' + '╱╳╲ LE JEU COMMENCE ╱╳╲')
    actualisation()
    while True:
        compteur_tour += 1
        deplacement_player()
        test_collision()
        deplacement_mob()
        test_collision()
        ajout_mob()
        actualisation()

if __name__ == '__main__':
    main()
