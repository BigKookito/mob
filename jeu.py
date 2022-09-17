from colorama import Fore, Back, Style, deinit, init, Cursor
from msvcrt import getch
from random import*

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

case_laser = []

nb_mob_mort = 0

cooldown_laser = 10

etat_laser_left = - cooldown_laser
etat_laser_right = - cooldown_laser
etat_laser_top = - cooldown_laser
etat_laser_bottom = - cooldown_laser

try:
    r = open('high_score.txt')
    lecture_txt = r.readlines()
    lecture_separe = lecture_txt[0].split()
    r.close()
except:
    lecture_separe = ['0', '0', '0']

def actualisation():
    global case_laser
    print(Cursor.POS(0, 0))
    print("—————————————————————————————")
    for y in range(nb_cases_y):
        for x in range(nb_cases_x):
            mob_nb = 0
            for i in range(len(mob_x)):
                if x == mob_x[i] and y == mob_y[i]:
                    mob_nb += 1
            if [x, y] in case_laser:
                print(Back.RED, end="")
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
                print(Fore.GREEN + Style.BRIGHT + " * " + Style.RESET_ALL, end="")
            else:
                print(" . " + Style.RESET_ALL, end="")
        print("")
    print(Cursor.POS(35, 4) + Fore.BLUE + 'Le record est de ' + Fore.CYAN + Style.BRIGHT + lecture_separe[2] + Style.RESET_ALL + Fore.BLUE + ' points avec ' + Fore.CYAN + Style.BRIGHT + lecture_separe[1] + Style.RESET_ALL + Fore.BLUE + ' monstres tués (' + Fore.CYAN + Style.BRIGHT + lecture_separe[0] + Style.RESET_ALL + Fore.BLUE + ' tours)' + Style.RESET_ALL)
    print(Cursor.POS(35, 6) + Style.BRIGHT + Fore.BLUE + "Infos :" + Style.RESET_ALL, "Tour :", compteur_tour + 1, "– Monstres tués :", nb_mob_mort, '– Points :', compteur_points)

    print(Cursor.POS(35, 8) + 'Statut lasers :', end="   ")
    print(' ☩ ')
    laser_status(50, 8, etat_laser_left)
    laser_status(56, 8, etat_laser_right)
    laser_status(53, 7, etat_laser_top)
    laser_status(53, 9, etat_laser_bottom)

    print(Cursor.POS(0, nb_cases_y + 2))
    case_laser = []

def laser_status(curseur_x, curseur_y, etat):
    if etat + 10 <= compteur_tour:
        color = Fore.BLUE
    else:
        color = Fore.RED
    print(Cursor.POS(curseur_x, curseur_y) + color + ' ⚫ ' + Fore.RESET)

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

def action_player():
    global player_x, player_y, etat_laser_left, etat_laser_right, etat_laser_top, etat_laser_bottom
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

    # --> direction des lasers
    elif move == b'e':
        direction_laser = getch().lower()
        if direction_laser == b'q' and etat_laser_left + 10 <= compteur_tour:
            rayon_left()
            etat_laser_left = compteur_tour
        elif direction_laser == b'd' and etat_laser_right + 10 <= compteur_tour:
            rayon_right()
            etat_laser_right = compteur_tour
        elif direction_laser == b'z' and etat_laser_top + 10 <= compteur_tour:
            rayon_top()
            etat_laser_top = compteur_tour
        elif direction_laser == b's' and etat_laser_bottom + 10 <= compteur_tour:
            rayon_bottom()
            etat_laser_bottom = compteur_tour
        else:
            print("Direction invalide ou attendre avant de pouvoir utiliser")
    else:
        print("Déplacement invalide, il faut taper z,q,s,d")

def test_collision():
    global compteur_points, piece_x, piece_y
    # on compare les postitions des mobs avec celle du joueur
    for i in range(len(mob_x)):
        if player_y == mob_y[i] and player_x == mob_x[i]:
            if compteur_points > int(lecture_separe[2]):
                print(Cursor.POS(55, 2) + Style.BRIGHT + Fore.RED + " NOUVEAU RECORD" + Style.RESET_ALL + Cursor.POS(0, nb_cases_y + 2))
                with open('high_score.txt', 'w') as r:
                    r.write(str(compteur_tour) + ' ' + str(nb_mob_mort) + ' ' + str(compteur_points))
            exit('╠═══╍╍ Vous avez perdu ╍╍═══╣')
        elif player_x == piece_x and player_y == piece_y:
            compteur_points += 1
            piece_x = randint(0, nb_cases_x - 1)
            piece_y = randint(0, nb_cases_y - 1)

def ajout_mob():
    global mob_x, mob_y
    if compteur_tour % 5 == 0:
        mob_x.append(choices([0, nb_cases_x])[0])
        mob_y.append(choices([0, nb_cases_y])[0])

def rayon_left():
    global mob_x, mob_y, nb_mob_mort
    mob_a_enlever = []
    for i in range(len(mob_x)):
        if mob_x[i] < player_x and mob_y[i] == player_y:
            mob_a_enlever.append(i)
    mob_x = [x for i, x in enumerate(mob_x) if i not in mob_a_enlever]
    mob_y = [y for i, y in enumerate(mob_y) if i not in mob_a_enlever]
    for x in range(0, player_x):
        case_laser.append([x, player_y])
    nb_mob_mort += len(mob_a_enlever)

def rayon_right():
    global mob_x, mob_y, nb_mob_mort
    mob_a_enlever = []
    for i in range(len(mob_x)):
        if mob_x[i] > player_x and mob_y[i] == player_y:
            mob_a_enlever.append(i)
    mob_x = [x for i, x in enumerate(mob_x) if i not in mob_a_enlever]
    mob_y = [y for i, y in enumerate(mob_y) if i not in mob_a_enlever]
    for x in range(player_x + 1, nb_cases_x + 1):
        case_laser.append([x, player_y])
    nb_mob_mort += len(mob_a_enlever)

def rayon_top():
    global mob_x, mob_y, nb_mob_mort
    mob_a_enlever = []
    for i in range(len(mob_x)):
        if mob_x[i] == player_x and mob_y[i] < player_y:
            mob_a_enlever.append(i)
    mob_x = [x for i, x in enumerate(mob_x) if i not in mob_a_enlever]
    mob_y = [y for i, y in enumerate(mob_y) if i not in mob_a_enlever]
    for y in range(0, player_y):
        case_laser.append([player_x, y])
    nb_mob_mort += len(mob_a_enlever)

def rayon_bottom():
    global mob_x, mob_y, nb_mob_mort
    mob_a_enlever = []
    for i in range(len(mob_x)):
        if mob_x[i] == player_x and mob_y[i] > player_y:
            mob_a_enlever.append(i)
    mob_x = [x for i, x in enumerate(mob_x) if i not in mob_a_enlever]
    mob_y = [y for i, y in enumerate(mob_y) if i not in mob_a_enlever]
    for y in range(player_y + 1, nb_cases_y + 1):
        case_laser.append([player_x, y])
    nb_mob_mort += len(mob_a_enlever)

def main():
    global player_x, player_y, compteur_tour
    print('\033[3C' + '╱╳╲ LE JEU COMMENCE ╱╳╲')
    actualisation()
    while True:
        compteur_tour += 1
        action_player()
        test_collision()
        deplacement_mob()
        test_collision()
        ajout_mob()
        actualisation()

if __name__ == '__main__':
    main()
