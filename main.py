import pygame
import pygame_gui
import os
from random import *

# Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Solfège : Lecture de note")
pygame.display.set_icon(pygame.image.load("image/treble-clef.png"))
screen.fill((255, 255, 255))
manager = pygame_gui.UIManager((600, 600), 'theme.json')
rect_partition = pygame.Rect(20, 0, 550, 290)  # x,y,longueur,hauteur
rect_score = pygame.Rect(121, 540, 358, 60)
myfont = pygame.font.SysFont('Arial', 30)

# Variables du jeu
timer = 0
nbr_note = 0
total_note = -1
clock = pygame.time.Clock()
points = 0
clicked = False
random_note = None


class Note:
    def __init__(self, nom, numero, position):
        self.nom = nom
        self.numero = numero
        self.position = position

    def get_image(self):
        """
        Donne une image de note normal si celle-ci est situé sur ou en dessous de la ligne du milieu de la partition.
        Else: une image inversée
        """
        if self.position < 4:  # note inversé
            return "image/note_reversed.png"
        elif self.position >= 4:  # note normal
            return "image/note_normal.png"

    def centre(self):
        """
        Donne le centre de la note pour lui donne une position exacte.
        """
        if self.position < 4:  # note inversé
            return 12, 9  # x,y avec O en NW
        elif self.position >= 4:  # note normal
            return 12, 54  # x,y avec O en NW

    def afficher_note(self, nb_notes):
        # Affichage de la note
        posx = (nb_notes * decalage_note + pos_ini_x) - Note.centre(self)[0]
        posy = (self.position * decalage_ligne + pos_ini_y) - Note.centre(self)[1]
        load_note = pygame.image.load(Note.get_image(self))
        load_note.convert_alpha()
        screen.blit(load_note, (posx, posy))

        # Affichage lignes supplémentaires
        if self.position <= -1:
            for line in range(0, 1 - round(self.position)):
                start = (posx - 20 + Note.centre(self)[0],
                         pos_ini_y - line * decalage_ligne)
                end = (posx + 20 + Note.centre(self)[0],
                       pos_ini_y - line * decalage_ligne)
                pygame.draw.line(screen, (0, 0, 0), start, end)
        elif self.position > 4.51:
            for line in range(1, round(self.position) - 3):
                start = (posx - 20 + Note.centre(self)[0],
                         pos_ini_y + 4 * decalage_ligne + line * decalage_ligne)
                end = (posx + 20 + Note.centre(self)[0],
                       pos_ini_y + 4 * decalage_ligne + line * decalage_ligne)
                pygame.draw.line(screen, (0, 0, 0), start, end)
        pygame.display.update(rect_partition)  # update le rectangle autour de la partition


# Liste notes
Mi2 = Note("Mi", 1, -3)
Re2 = Note("Ré", 1, -2.50001)
Do2 = Note("Do", 1, -2)
Si1 = Note("Si", 1, -1.50001)
La1 = Note("La", 1, -1)
Sol1 = Note("Sol", 1, -0.50001)
Fa1 = Note("Fa", 1, 0)
Mi1 = Note("Mi", 1, 0.50001)
Re1 = Note("Ré", 1, 1)
Do1 = Note("Do", 1, 1.50001)
Si0 = Note("Si", 1, 2)
La0 = Note("La", 1, 2.50001)
Sol0 = Note("Sol", 1, 3)
Fa0 = Note("Fa", 1, 3.50001)
Mi0 = Note("Mi", 1, 4)
Re0 = Note("Ré", 1, 4.50001)
Do0 = Note("Do", 1, 5)
Si_F = Note("Si", 1, 5.50001)
La_F = Note("La", 1, 6)
Sol_F = Note("Sol", 1, 6.50001)
Fa_F = Note("Fa", 1, 7)

note_liste = [Mi2, Re2, Do2, Si1, La1, Sol1, Fa1, Mi1, Re1, Do1, Si0, La0, Sol0, Fa0, Mi0, Re0, Do0, Si_F, La_F, Sol_F,
              Fa_F]

taille_ligne = 550
decalage_ligne = 20
decalage_note = 40
pos_ini_x = 20
pos_ini_y = 100

# Affichage des boutons :
do_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 295), (100, 50)),
                                         text='Do',
                                         manager=manager)
re_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 295), (100, 50)),
                                         text='Ré',
                                         manager=manager)
mi_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 295), (100, 50)),
                                         text='Mi',
                                         manager=manager)
fa_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 355), (100, 50)),
                                         text='Fa',
                                         manager=manager)
sol_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 355), (100, 50)),
                                          text='Sol',
                                          manager=manager)
la_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 355), (100, 50)),
                                         text='La',
                                         manager=manager)
si_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240, 415), (100, 50)),
                                         text='Si',
                                         manager=manager)
stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 540), (100, 50)),
                                           text='STOP',
                                           manager=manager)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((480, 540), (100, 50)),
                                            text='START',
                                            manager=manager)
slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((130, 500), (320, 20)),
                                                start_value=1,
                                                value_range=(1, 10),
                                                manager=manager)


# hover_slider = pygame_gui.elements.UITooltip(html_text='Ceci est un texte de test',
#                                              hover_distance=(0,20),
#                                              manager=manager,
#                                              parent_element=start_button)


def afficher_partition():
    """
    Affiche la partition, donc affiche 5 lignes avec 20px d'espace.
    Aucune valeure à rentrer
    """
    # Affichage partition
    for line in range(0, 5):
        start = (pos_ini_x, pos_ini_y +
                 decalage_ligne * line)
        end = (pos_ini_x + taille_ligne,
               pos_ini_y + decalage_ligne * line)
        pygame.draw.line(screen, (0, 0, 0), start, end)
    pygame.display.update(rect_partition)


def reset_partition():
    """
    Réinitialise la partition, supprime les notes de l'affichage.
    """
    screen.fill((255, 255, 255), rect_partition)
    afficher_partition()


def afficher_score(score, total):
    """
    Affiche le score du joueur.
    """
    score = str(score)
    total = str(total)
    score_render = "Score : %s/%s" % (score, total)
    affichage_score = myfont.render(score_render, True, (0, 0, 0), (255, 255, 255))
    decalage = len(score) + len(total) * 5  # décale l'affichage du score selon la taille du score
    screen.fill((255, 255, 255), rect_score)
    screen.blit(affichage_score, (230 - decalage, 540))
    pygame.display.update(rect_score)


def test_bonne_note(note):
    """
    Test si la note est juste par rapport à la note aléatoire,
    en argument la note à tester
    :param note:
    :return:
    """
    global clicked
    global points
    global total_note
    global random_note
    if note == random_note.nom:  # on compare la réponse au nom de la note
        points += 1
        total_note += 1
    else:
        total_note += 1
    clicked = True


def main():
    global clicked  # Clicked sert à vérifier si une réponse a été donné, si c'est le cas on affiche une autre note
    global points
    global timer
    global nbr_note
    global random_note
    global clock
    global total_note
    launched = True
    game_start = False

    afficher_partition()

    while launched:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == do_button:
                        if game_start:
                            test_bonne_note("Do")
                    if event.ui_element == re_button:
                        if game_start:
                            test_bonne_note("Ré")
                    if event.ui_element == mi_button:
                        if game_start:
                            test_bonne_note("Mi")
                    if event.ui_element == fa_button:
                        if game_start:
                            test_bonne_note("Fa")
                    if event.ui_element == sol_button:
                        if game_start:
                            test_bonne_note("Sol")
                    if event.ui_element == la_button:
                        if game_start:
                            test_bonne_note("La")
                    if event.ui_element == si_button:
                        if game_start:
                            test_bonne_note("Si")
                    if event.ui_element == stop_button:
                        if game_start:
                            game_start = False
                            reset_partition()
                            timer = 0
                            nbr_note = 0
                            total_note = 0
                            points = 0

                    if event.ui_element == start_button:
                        if not game_start:
                            game_start = True
        if game_start:
            timer -= dt
            if (timer <= 0 and nbr_note < 13) or (clicked and nbr_note < 13):
                # Si le temps est écoulé ou si on a cliqué
                nbr_note += 1
                if timer <= 0:
                    total_note += 1
                afficher_score(points, total_note)
                random_note = choice(note_liste)
                Note.afficher_note(random_note, nbr_note)
                timer = 10000/round(slider.get_current_value())
                clicked = False
            elif (timer <= 0 and nbr_note >= 13) or (clicked and nbr_note >= 13):
                # Si on a atteint la fin de la portée on reset tout l'affichage
                reset_partition()
                nbr_note = 0
                clicked = False

        manager.update(dt / 1000.0)
        manager.draw_ui(screen)
        pygame.display.flip()


main()
