from colorama import Fore, Back, Style
from msvcrt import getch
from random import*

nb_cases_x = 6
nb_cases_y = 6

player_x = 6
player_y = 3


mob_x = [0, 0, 6, 6]
mob_y = [0, 6, 0, 6]


def actualisation():
    print("--------------------------")
    for x in range(7):
        for y in range(7):
            mob_nb = 0
            for i in range(len(mob_x)):
                if x == mob_x[i] and y == mob_y[i]:
                    mob_nb += 1
            if mob_nb >= 1:
                if mob_nb == 1:
                    print(Fore.YELLOW + " " + str(mob_nb) + Style.RESET_ALL, end=" ")
                elif mob_nb == 2:
                    print(Fore.MAGENTA + " " + str(mob_nb) + Style.RESET_ALL, end=" ")
                else:
                    print(Fore.RED + " " + str(mob_nb) + Style.RESET_ALL, end=" ")
            elif x == player_x and y == player_y:
                print(Fore.BLUE + " O" + Style.RESET_ALL, end=" ")
            else:
                print(" .", end=" ")
        print("")


def deplacement_mob():
    global mob_x, mob_
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
    # print(move)
    if move == b'q':
        if player_y != 0:
            player_y -= 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur, réessayez" + Style.RESET_ALL)
    elif move == b'd':
        if player_y != nb_cases_y:
            player_y += 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur, réessayez" + Style.RESET_ALL)
    elif move == b'z':
        if player_x != 0:
            player_x -= 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur, réessayez" + Style.RESET_ALL)
    elif move == b's':
        if player_x != nb_cases_x:
            player_x += 1
        else:
            print(Fore.RED + "Vous ne pouvez pas traverser le mur, réessayez" + Style.RESET_ALL)
    else:
        print("saisie invalide")

def test_collision():
    # on compare les postitions des mobs avec celle du joueur
    for i in range(len(mob_x)):
        if player_y == mob_y[i] and player_x == mob_x[i]:
            exit('Vous avez perdu')

def main():
    global player_x, player_y
    print("LE JEU COMMENCE")
    actualisation()
    while True:
        deplacement_player()
        test_collision()
        deplacement_mob()
        test_collision()
        actualisation()

        # print(player_x, player_y)


if __name__ == '__main__':
    main()
