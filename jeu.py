from colorama import Fore, Back, Style, Cursor
from msvcrt import getch
from random import *

nb_cases_x = 10
nb_cases_y = 10

player_x = nb_cases_y - 1
player_y = nb_cases_x // 2

mob_x = [0, 0]
mob_y = [0, nb_cases_x - 1]

compteur_tour = 0
compteur_points = 0

piece_x = randint(0, nb_cases_x - 1)
piece_y = randint(0, nb_cases_y - 1)

case_laser = []
lecture_separe = []

nb_mob_mort = 0

cooldown_laser = 10
frequence_ajout_mob = 10

etat_laser_left = - cooldown_laser
etat_laser_right = - cooldown_laser
etat_laser_top = - cooldown_laser
etat_laser_bottom = - cooldown_laser

choix_niveau = ''


def read_highscore():
    global lecture_separe
    try:
        r = open(choix_niveau + '.txt')
        lecture_txt = r.readlines()
        lecture_separe = lecture_txt[0].split()
        r.close()
    except:
        lecture_separe = ['0', '0', '0']


def actualisation():
    global case_laser, choix_niveau
    print(Cursor.POS(0, 3))
    print('\033[5C' + '╱╳╲ MOB HUNTER ╱╳╲')
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
    print(Cursor.POS(35, 7) + Fore.BLUE + Style.BRIGHT + 'Le record est du niveau ' + choix_niveau + ' est de ' + Fore.CYAN + lecture_separe[
        2] + Fore.BLUE + ' points avec ' + Fore.CYAN + lecture_separe[
              1] + Fore.BLUE + ' monstres tués (' + Fore.CYAN + lecture_separe[
              0] + Fore.BLUE + ' tours)' + Style.RESET_ALL)
    print(Cursor.POS(35, 9) + Style.BRIGHT + Fore.BLUE + "Infos :" + Style.RESET_ALL, "Tours :", compteur_tour + 1,
          "– Monstres tués :", nb_mob_mort, '– Points :', compteur_points)
    print(Cursor.POS(35, 11) + Style.BRIGHT + Fore.BLUE + 'Statut lasers :', end="   ")
    print(' ☩ ')
    laser_status(51, 11, etat_laser_left)
    laser_status(55, 11, etat_laser_right)
    laser_status(53, 10, etat_laser_top)
    laser_status(53, 12, etat_laser_bottom)
    print(Cursor.POS(35, 13) + Style.BRIGHT + Fore.BLUE + 'Règle du niveau',
          Fore.CYAN + choix_niveau + Fore.BLUE + ':' + Style.RESET_ALL + ' Fréquence apparition monstres: ' + str(
              frequence_ajout_mob) + ' - Attente avant réutilisation laser ' + str(cooldown_laser))

    print(Cursor.POS(0, nb_cases_y + 4))
    case_laser = []


def laser_status(curseur_x, curseur_y, etat):
    if etat + cooldown_laser <= compteur_tour:
        color = Fore.BLUE
    else:
        color = Fore.RED
    print(Cursor.POS(curseur_x, curseur_y) + color + ' ● ' + Fore.RESET)


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
            print(Fore.RED + Cursor.POS(0, nb_cases_y + 6) + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b'd':
        if player_x != nb_cases_x - 1:
            player_x += 1
        else:
            print(Fore.RED + Cursor.POS(0, nb_cases_y + 6) + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b'z':
        if player_y != 0:
            player_y -= 1
        else:
            print(Fore.RED + Cursor.POS(0, nb_cases_y + 6) + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)
    elif move == b's':
        if player_y != nb_cases_y - 1:
            player_y += 1
        else:
            print(Fore.RED + Cursor.POS(0, nb_cases_y + 6) + "Vous ne pouvez pas traverser le mur" + Style.RESET_ALL)

    # --> direction des lasers
    elif move == b'e':
        direction_laser = getch().lower()
        if direction_laser == b'q' and etat_laser_left + cooldown_laser <= compteur_tour:
            rayon_left()
            etat_laser_left = compteur_tour
        elif direction_laser == b'd' and etat_laser_right + cooldown_laser <= compteur_tour:
            rayon_right()
            etat_laser_right = compteur_tour
        elif direction_laser == b'z' and etat_laser_top + cooldown_laser <= compteur_tour:
            rayon_top()
            etat_laser_top = compteur_tour
        elif direction_laser == b's' and etat_laser_bottom + cooldown_laser <= compteur_tour:
            rayon_bottom()
            etat_laser_bottom = compteur_tour
        else:
            print(Fore.RED + Cursor.POS(0,
                                        nb_cases_y + 6) + "Direction invalide ou attendre avant de pouvoir utiliser" + Style.RESET_ALL)
    else:
        print(Fore.RED + Cursor.POS(0, nb_cases_y + 6) + "Déplacement invalide" + Style.RESET_ALL)


def test_collision():
    global compteur_points, piece_x, piece_y
    # on compare les postitions des mobs avec celle du joueur
    for i in range(len(mob_x)):
        if player_y == mob_y[i] and player_x == mob_x[i]:
            if compteur_points > int(lecture_separe[2]):
                print(Cursor.POS(55, 6) + Style.BRIGHT + Fore.RED + " NOUVEAU RECORD" + Style.RESET_ALL + Cursor.POS(0,
                                                                                                                     nb_cases_y + 2))
                with open(choix_niveau + '.txt', 'w') as r2:
                    r2.write(str(compteur_tour) + ' ' + str(nb_mob_mort) + ' ' + str(compteur_points))
            print(Cursor.POS(0, nb_cases_y + 6))
            exit('╠═══╍╍ Vous avez perdu ╍╍═══╣')
        elif player_x == piece_x and player_y == piece_y:
            compteur_points += 1
            piece_x = randint(0, nb_cases_x - 1)
            piece_y = randint(0, nb_cases_y - 1)


def ajout_mob():
    global mob_x, mob_y
    if compteur_tour % frequence_ajout_mob == 0:
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


def options_jeu():
    global cooldown_laser, frequence_ajout_mob, choix_niveau
    choix_niveau = input('Saisir la difficulté : easy, normal, hard ou rules -> ')
    if choix_niveau == 'easy':
        cooldown_laser = 5
        frequence_ajout_mob = 10
    elif choix_niveau == 'normal':
        cooldown_laser = 10
        frequence_ajout_mob = 10
    elif choix_niveau == 'hard':
        cooldown_laser = 10
        frequence_ajout_mob = 5
    elif choix_niveau == 'rules':
        affichage_des_regles()
    else:
        exit('Aucun choix de niveau fait')

def affichage_des_regles():
    print(Fore.BLUE + Style.BRIGHT + 'Les règles de MOB HUNTER :' + Style.RESET_ALL)
    print('')
    print("Le jeu se joue sur la console python souvent en bas de votre écran, quand le jeu se lance, il faut écrire le niveau de difficulté souhaité ou l'affichage des règles.",
    "Votre personnage est le rond bleu à droite quand le jeu se lance, les chiffres correspondent au nombre de monstres qu'il y a sur la même case, et l'étoile (*) c'est les pièces qu'il faut attrapper",
    "Il faut utiliser les touches z, q, s, d pour se déplacer ce qui correspond respectivement à haut, gauche, bas, droite. Puis il y a la touche e, une fois pressé il faut indiquer une direction pour l'envoi du laser.",
    "Chaque laser, une fois utilisé on doit attendre plusieurs tours avant de l'utiliser à nouveau, cela dépend du niveau de difficulté. C'est pareil pour l'apparition de nouveau monstres.")

    print("Le but du jeu est de faire un maximum de points dans chaque niveau de difficulté, ils sont affichés en haut, le but c'est de les dépasser.")
    print('')
    revenir_au_menu = input(Fore.BLUE + Style.BRIGHT + 'Saisir entrée pour revenir au menu :' + Style.RESET_ALL)
    if revenir_au_menu == '':
        clear_terminal()
        print(Cursor.POS(0, 0))
        options_jeu()

def clear_terminal():
    print('\033[2J')

def main():
    global player_x, player_y, compteur_tour
    options_jeu()
    read_highscore()
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
