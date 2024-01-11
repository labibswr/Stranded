# Title: STRANDED PYGAME
# Start Date: December 17, 2022
# End Date: January 18, 2023
# Description: The following program is a pygame project that is a game
#               about a character lost in space. The objective of the game
#               is for the user to complete a series of levels to get the
#               character to the portal until it reaches the end. Upon
#               completing the fifth level, the game is completed. If the
#               player fails to complete a level, they are redirected to
#               an additional "resurrection" game that is a cursor based
#               maze game. If the user can complete the resurrection, they
#               will be placed back at the level they were playing at.
#               Failure of the resurrection game will result in "game over"
#               and the user will have to replay back at level 1.

# Importing pygame and classes
from Block import *
from Player import *
from Enemy import *

import pygame
from pygame.locals import *

# Intialising pygame
pygame.init ()
pygame.mixer.init ()


# Resurrection game function
def resurrection (map_i):
    # Set resurrection maze game window
    r_screen = pygame.display.set_mode ( (600, 600))
    bg = pygame.image.load ("graphics/dark_bg.jpg")
    bg = pygame.transform.scale (bg, (600, 600))

    # Maze path rectangle coordinates
    maze_path = [[ ( (150, 400), (50, 200)), ( (150, 350), (250, 51)),
                  ( (360, 350), (40, 200)), ( (399, 520), (110, 30)),
                  ( (500, 150), (30, 400)), ( (250, 150), (252, 25)),
                  ( (250, 0), (20, 151))],
                 [( (0, 250), (201, 50)), ( (199, 250), (52, 180)),
                  ( (249, 400), (202, 30)), ( (420, 350), (31, 51)),
                  ( (450, 350), (100, 30)), ( (530, 150), (20, 201)),
                  ( (300, 150), (231, 20)), ( (300, 0), (15, 151))]]

    in_maze = True

    # Rectangles for the maze map is drawn.
    r_screen.blit (bg, (0, 0))
    for d in maze_path[map_i]:
        pygame.draw.rect (r_screen, "white", d)

    # The cursor position is set to the start of the maze.
    # Maze end portal is drawn as a circle.
    if (map_i == 0):
        pygame.mouse.set_pos ( (175, 580))
        portal_pos = (260, 50)
        radius = 7.5
        pygame.draw.circle (r_screen, "red", portal_pos, radius)

    else:
        pygame.mouse.set_pos ( (30, 270))
        portal_pos = (307.5, 20)
        radius = 4.5
        pygame.draw.circle (r_screen, "red", portal_pos, radius)

    while in_maze:

        for event in pygame.event.get ():
            if (event.type == pygame.QUIT):
                pygame.quit ()

        mouse_pos = pygame.mouse.get_pos ()

 #Function returns 1 if mouse position meets the portal circle  position.
        if ( ( (mouse_pos[0] - portal_pos[0]) ** 2 + (mouse_pos[1] -
                                                    portal_pos[1]) ** 2)
                <= radius ** 2):
            return 1

    # Game keeps going while the mouse is inside the maze path rectangles.
        if (any (i[0][0] < mouse_pos[0] < i[1][0] + i[0][0] and
                i[0][1] < mouse_pos[1] < i[1][1] + i[0][1]
                for i in maze_path[map_i])):
            pass
 # If mouse is not in the rectangle, function returns 0 and the player
        # fails.
        else:
            return 0

        pygame.display.update ()


# Function that takes the following parameters and uses them to make the
# map in a display. It uses the record that is setup below within the
# main functions.
def load_map (grid, track, obj, imgs):
    for i in range (len (grid[track])):
        for j in range (len (grid[track][i])):

            if (grid[track][i][j] == "#"):

                b = Block (j * 20, i * 20, "block", imgs[1])
                obj[0].append (b)

            elif (grid[track][i][j] == "@"):

                b = Block (j * 20, i * 20, "portal", imgs[0])
                obj[0].append (b)

            elif (grid[track][i][j] == "^"):

                p = Player (j * 20, i * 20, imgs[3])
                obj[1].append (p)

            elif (grid[track][i][j] == "x"):

                e = Enemy (j * 20, i * 20, "melee", imgs[4])
                obj[2].append(e)

            elif (grid[track][i][j] == "1"):

                e = Enemy (j * 20, i * 20, "turret", imgs[5])
                obj[2].append (e)

            elif (grid[track][i][j] == "="):

                b = Block (j * 20, i * 20, "spikes", imgs[2])

                obj[0].append (b)


def game_over_screen ():
    # creates screen
    game_over_screen = pygame.display.set_mode ( (600, 600))

    # unloads game music
    pygame.mixer.music.unload ()

    # loads new music, adjust volumne and loops
    pygame.mixer.music.load ("sound/scary-forest-90162.mp3")
    pygame.mixer.music.set_volume (0.2)
    pygame.mixer.music.play (-1)

    screen_loop = True # loop for screen is true

    while (screen_loop):
        game_over_img = pygame.image.load ('graphics/game_over_screen.jpg')

        game_over_scale = pygame.transform.scale (game_over_img, (750,
                                                                  600))

        game_over_screen.blit (game_over_scale, (-70, 0))

        # replay button and quit button for the game over menu
        replay_button_rect = pygame.Rect (90, 430, 120, 50)  # replay
        quit_button_rect = pygame.Rect (380, 430, 120, 50)  # quit

        # checks if the mouse is hovering over where the button is
        mouse_x, mouse_y = pygame.mouse.get_pos ()
        replay_hovering = replay_button_rect.collidepoint (mouse_x,
                                                           mouse_y)
        quit_hovering = quit_button_rect.collidepoint (mouse_x, mouse_y)

        white = (255, 255, 255) # colour code saved for use

        # changes colours of buttons if user is hovering on either of them
        if (replay_hovering):
            replay_button_color = (0, 0, 255)
        else:
            replay_button_color = (5, 5, 5)

        if (quit_hovering):
            quit_button_color = (0, 0, 255)
        else:
            quit_button_color = (5, 5, 5)

        # Box for the replay and quit buttons
        pygame.draw.rect (game_over_screen, replay_button_color,
                         replay_button_rect)

        pygame.draw.rect (game_over_screen, quit_button_color,
                         quit_button_rect)

        # Font and size used for both buttons
        font = pygame.font.Font (None, 32)

        # Replay and Quit text created with font and colour,
        # and positioned
        replay_text_surface = font.render ("Replay", True, white)

        replay_text_rect = replay_text_surface.get_rect (
            center=replay_button_rect.center)

        quit_text_surface = font.render ("Quit", True, white)

        quit_text_rect = quit_text_surface.get_rect (
            center=quit_button_rect.center)

        game_over_screen.blit (replay_text_surface,
                              replay_text_rect)  # replay button
        game_over_screen.blit (quit_text_surface, quit_text_rect) # quit

        pygame.display.flip () # updates display

        # gathers the events of the user
        for event in pygame.event.get ():
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==
                    1):
                if (quit_hovering): # if quit button is clicked
                    return "Quit"

                elif (replay_hovering): # if replay button is clicked
                    pygame.mixer.music.unload ()
                    pygame.mixer.music.load ('sound/background_sound.mp3')
                    pygame.mixer.music.set_volume (0.2)
                    pygame.mixer.music.play (-1)
                    return "Replay"

            elif (event.type == pygame.QUIT): # if user closes windoew
                return "Quit"


def game_completed_screen ():
    # music unloaded
    pygame.mixer.music.unload ()
    # new music loaded, adjusted volumne and looped
    pygame.mixer.music.load ('sound/end_screen_sound.mp3')
    pygame.mixer.music.set_volume (0.1)
    pygame.mixer.music.play (-1)
    # Create display for gameover screen
    game_completed_screen = pygame.display.set_mode ( (600, 600))

    # start loop to keep the window open until the user closes it
    screen_loop = True

    # contents of the gameover screen
    while (screen_loop):
        # loads the image, scales the image, and puts the image on the
        # display
        game_completed_img = pygame.image.load (
            "graphics/game_completed_screen.jpg")

        game_completed_scale = pygame.transform.scale (game_completed_img,
                                                      (800, 600))
        game_completed_screen.blit (game_completed_scale, (0, 0))

        # Font created. Size 80
        font = pygame.font.SysFont ("FONT", 75, bold=False,
                                    italic=False)  #
        font.set_underline (True)

        # Big Text on Screen using the created font
        text_surface = font.render (" GAME COMPLETED! ", True, (255, 255,
                                                               255))

        # added image of player to the gameover screen to demonstrate
        # the ending of the storyline
        eg_player = pygame.image.load ("graphics/player-idle-1.png")
        eg_player_scaled = pygame.transform.scale (eg_player, (90, 90))

        # adding the text and image of the player to the display
        game_completed_screen.blit (text_surface, (45, 70))  # text
        game_completed_screen.blit (eg_player_scaled, (65, 375))  # player
        # image

        pygame.display.flip ()  # updates screen

        # If user exits program (using the x on the top right)
        for event in pygame.event.get ():
            if (event.type == pygame.QUIT):
                screen_loop = False


def menu_screen ():
    # creates the display for the menu
    menu_screen = pygame.display.set_mode ( (600, 600))

    # loop for the menu screen, to ensure it stays open until something
    # is done
    menu_screen_loop = True
    # the contents of the menu / start screen
    while menu_screen_loop:
        # Background size, image loading, and surface loading for the menu
        background_image = pygame.image.load ("graphics/start_menu.jpg")
        background_image = pygame.transform.scale (background_image,
                                                  (600, 600))
        menu_screen.blit (background_image, (0, 0))
        # button creation
        start_button_rect = pygame.Rect (225, 430, 150, 50)
        controls_button_rect = pygame.Rect (225, 500, 150, 50)

        # checks if the mouse is hovering over where the button is
        mouse_x, mouse_y = pygame.mouse.get_pos ()
        start_hovering = start_button_rect.collidepoint (mouse_x, mouse_y)
        controls_hovering = controls_button_rect.collidepoint (mouse_x,
                                                              mouse_y)

        # controls the colours for when the user is hovering and not
        # hovering over the button
        if (start_hovering):
            start_button_color = (0, 0, 255)
        else:
            start_button_color = (0, 0, 0)

        if (controls_hovering):
            controls_button_color = (0, 0, 255)
        else:
            controls_button_color = (0, 0, 0)

        # Font and Size used for the title of the game
        font = pygame.font.Font ('freesansbold.ttf', 65)  # font
        text_surface = font.render ("STRANDED", True, (255, 255,
                                                      255))  # text

        # New Font created for the authors/developers of the game
        font = pygame.font.SysFont ("creators", 20, bold=False,
                                   italic=True)

        # the drawing of the buttons
        pygame.draw.rect (menu_screen, start_button_color,
                         start_button_rect)
        pygame.draw.rect (menu_screen, controls_button_color,
                         controls_button_rect)

        # Font and size used for both buttons
        font = pygame.font.Font (None, 36)  # font and size

        # text of the Start Game Button
        start_text_surface = font.render ("Start Game", True,
                                         (255, 255, 255))

        # determines the positioning of Start Game text
        start_text_rect = start_text_surface.get_rect (
            center=start_button_rect.center)

        # Text of the How To Play Button.
        controls_text_surface = font.render ("How to Play", True,
                                            (255, 255, 255))

        # determines the positioning of the Controls text
        controls_text_rect = controls_text_surface.get_rect (
            center=controls_button_rect.center)

        # All text added to the menu screen display.
        menu_screen.blit (start_text_surface, start_text_rect)  # Start
        # Game
        menu_screen.blit (controls_text_surface,
                         controls_text_rect)  # ctrls
        menu_screen.blit (text_surface, (120, 80))  # title

        pygame.display.flip ()  # updates screen
        # tracks when the player presses the start or controls button, when
        # they do it will end the loop so the code can advance to the next
        # screen. The user is unable to close the game through the start
        # menu they gotta press play first then close if they want to
        # end early.
        for event in pygame.event.get (): # checks for user interactions
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==
                    1):
                if (start_hovering): # if start game button is pressed
                    menu_screen_loop = False
                    return "Start Game"
                elif (controls_hovering): # if controls button is pressed
                    menu_screen_loop = False
                    return "Controls"
            elif (event.type == pygame.QUIT): # if window is closed
                menu_screen_loop = False
                return "Quit"


def controls_screen_content (screen): # continuation of controls function
    controls_screen = screen  # Screen

    # font for the controls text
    font = pygame.font.SysFont ("text", 29, bold=True, italic=False)

    white = (255, 255, 255)  # colour code saved in variable

    controls = font.render ("Controls:", True, white)

    # Code for the text under the section of controls with font size
    font = pygame.font.Font (None, 27)  # font for objective / game explain

    objective_text = font.render ("The objective is for you, "
                                 "the player, to navigate past all "
                                 "obstacles", True,
                                 white)
    objective_text2 = font.render ("to reach a portal. You must go "
                                  "through 5 "
                                  "portals to end the game", True,
                                  white)

    font = pygame.font.Font (None, 26)  # font for controls
    c_jump = font.render ("W or Up Arrow Key -> Player Jumps", True,
                         white)
    c_left = font.render ("A or Left Arrow Key -> Player moves Left",
                         True, white)
    c_right = font.render ("D or Right Arrow Key -> Player moves "
                          "Right", True, white)

    # Font used for each text that is beside each image
    # Below, a legend is setup, where an image of each thing within the
    # game is loaded and scaled alongside a text that goes with it
    # explaining what it is.
    font = pygame.font.Font (None, 25)

    eg_spikes = pygame.image.load ("graphics/spikes.png")
    eg_spikes_scaled = pygame.transform.scale(eg_spikes, (30, 30))
    spikes_text1 = font.render (" --> These spikes are obstacles that "
                               "deal significant", True, white)
    spikes_text2 = font.render ("damager to the player", True, white)

    eg_enemy = pygame.image.load ("graphics/enemy-walk-1.png")
    eg_enemy_scaled = pygame.transform.scale(eg_enemy, (30, 30))
    enemy_text1 = font.render ("--> These are Enemies that act as "
                              "obstacles", True, white)
    enemy_text2 = font.render ("and deal damage when they collide "
                              "with the player", True, white)

    eg_player = pygame.image.load ("graphics/player-idle-1.png")
    eg_player_scaled = pygame.transform.scale (eg_player, (30, 30))
    player_text = font.render ("--> This is the player you will be "
                              "playing as", True, white)

    eg_portal = pygame.image.load ("graphics/portal.png")
    eg_portal_scaled = pygame.transform.scale (eg_portal, (30, 30))
    portal_text = font.render (" --> This is the end goal of every "
                              "level, it is the portal that ",
                              True, white)
    portal_text2 = font.render ("the player must reach in order to "
                               "advance levels  and end the game",
                               True, white)

    eg_turret = pygame.image.load ("graphics/turret.png")
    eg_turret_head = pygame.image.load ("graphics/turret-head.png")
    eg_turret_scaled = pygame.transform.scale (eg_turret, (30, 30))
    eg_head_scaled = pygame.transform.scale (eg_turret_head, (42, 42))
    turret_text = font.render ("--> Turret that shoots bullets towards "
                              "player", True, white)

    # Each image/text added to the screen and positioned correctly
    # Controls of the game, all keyboard/game input from the user
    controls_screen.blit (controls, (250, 120))  # controls text
    controls_screen.blit (c_jump, (130, 150))  # jump text
    controls_screen.blit (c_left, (130, 175))  # left text
    controls_screen.blit (c_right, (130, 200))  # right text

    controls_screen.blit (objective_text, (20, 60))  # objective
    # description
    controls_screen.blit (objective_text2, (20, 80))  # obective
    # description2

    controls_screen.blit (eg_portal_scaled, (40, 370))  # portal image
    controls_screen.blit (portal_text, (80, 372))  # portal text
    controls_screen.blit (portal_text2, (110, 392))  # portal text part 2

    controls_screen.blit (eg_turret_scaled, (40, 430))  # turret image
    controls_screen.blit (eg_head_scaled, (34, 422))  # turret head image
    controls_screen.blit (turret_text, (90, 437))  # turret text

    controls_screen.blit (eg_enemy_scaled, (40, 500))  # Enemy image
    controls_screen.blit (enemy_text1, (80, 502))  # enemy text
    controls_screen.blit (enemy_text2, (110, 522))  # enemy text part 2

    controls_screen.blit (eg_spikes_scaled, (40, 295))  # spikes image
    controls_screen.blit (spikes_text1, (80, 300))  # spikes text
    controls_screen.blit (spikes_text2, (110, 320))  # spikes text part 2

    controls_screen.blit (eg_player_scaled, (40, 240))  # player image
    controls_screen.blit (player_text, (80, 242))  # player text


def controls_screen ():
    # seperate screen created for controls
    controls_screen = pygame.display.set_mode ( (600, 600))
    # loop for the controls screen to stay open

    controls_screen_loop = True
    while controls_screen_loop:
        # Background loaded, scaled, and added to display
        ctrl_img = pygame.image.load ("graphics/controls_background.jpg")
        ctrl_scale = pygame.transform.scale (ctrl_img, (600, 600))
        controls_screen.blit (ctrl_scale, (0, 0))

        # Back button and Start Game button created in this menu
        back_button_rect = pygame.Rect (250, 560, 100, 40)  # back
        start_button_rect = pygame.Rect (225, 5, 150, 40)  # start

        # checks if the mouse is hovering over where the button is
        mouse_x, mouse_y = pygame.mouse.get_pos ()
        back_hovering = back_button_rect.collidepoint (mouse_x, mouse_y)
        start_hovering = start_button_rect.collidepoint (mouse_x, mouse_y)

        white = (255, 255, 255)

        # changes colours of buttons if user is hovering on either of them
        if (back_hovering):
            back_button_color = (0, 0, 255)
        else:
            back_button_color = (5, 5, 5)
        if (start_hovering):
            start_button_color = (0, 0, 255)
        else:
            start_button_color = (5, 5, 5)

        # Box for the back, and start buttons
        pygame.draw.rect (controls_screen, back_button_color,
                         back_button_rect)
        pygame.draw.rect (controls_screen, start_button_color,
                         start_button_rect)

        # Font and size used for both buttons
        font = pygame.font.Font(None, 32)
        # Start and Back text created and placed
        back_text_surface = font.render ("Back", True, white)
        back_text_rect = back_text_surface.get_rect (
            center=back_button_rect.center)
        start_text_surface = font.render ("Start Game", True, white)
        start_text_rect = start_text_surface.get_rect (
            center=start_button_rect.center)

        controls_screen.blit (back_text_surface,
                             back_text_rect)  # backbutton
        controls_screen.blit (start_text_surface, start_text_rect)  # start

        controls_screen_content (controls_screen)

        pygame.display.flip ()  # updates screen

        # tracks when the player presses the back or start button and when
        # they do it will end the loop so the code can return to the
        # main menu or start the game.
        for event in pygame.event.get ():
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==
                    1):
                if (back_hovering): # if back button is pressed
                    controls_screen_loop = False
                    return "Back"
                elif (start_hovering): # if start game button is pressed
                    controls_screen_loop = False
                    return "Start Game"
            elif (event.type == pygame.QUIT): # if window is closed
                controls_screen_loop = False
                return "Quit"


# Window to ask player to revive their character or not after they fail
# level
def revive_screen ():
    # Screen setup
    rev_screen = pygame.display.set_mode ( (600, 600))
    rev_screen_on = True
    star_bg = pygame.image.load ("graphics/star_bg.jpg")
    star_bg = pygame.transform.scale (star_bg, (600, 600))

    rev_screen.blit (star_bg, (0, 0))

    while (rev_screen_on):

        # MESSAGES
        font = pygame.font.Font ('freesansbold.ttf', 65)
        die_message = font.render ("YOU DIED", True,
                                  (255, 0, 0))
        font = pygame.font.Font (None, 55)
        rev_message = font.render ("Revive?", True, (255, 255, 255))

        rev_screen.blit (die_message, (140, 50))
        rev_screen.blit (rev_message, (230, 200))

        # BUTTONS
        yes_button_rect = pygame.Rect (85, 300, 150, 150)
        no_button_rect = pygame.Rect (375, 300, 150, 150)

        mouse_pos = pygame.mouse.get_pos ()
        hover_yes = yes_button_rect.collidepoint (mouse_pos[0],
                                                 mouse_pos[1])
        hover_no = no_button_rect.collidepoint (mouse_pos[0], mouse_pos[1])

        if (hover_yes):
            yes_button_col = (255, 0, 0)
        else:
            yes_button_col = (255, 255, 255)

        if (hover_no):
            no_button_col = (255, 0, 0)
        else:
            no_button_col = (255, 255, 255)

        pygame.draw.rect (rev_screen, yes_button_col, yes_button_rect)
        pygame.draw.rect (rev_screen, no_button_col, no_button_rect)

        yes_text_surface = font.render ("Yes", True, "black")
        no_text_surface = font.render ("No", True, "black")

        yes_rect = yes_text_surface.get_rect (
            center=yes_button_rect.center)
        no_rect = no_text_surface.get_rect (center=no_button_rect.center)

        rev_screen.blit (yes_text_surface, yes_rect)
        rev_screen.blit (no_text_surface, no_rect)

        pygame.display.update ()

        for event in pygame.event.get ():
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button ==
                    1):
                if (hover_yes):
                    return "Y"
                elif (hover_no):
                    return "N"
            elif (event.type == pygame.QUIT):
                return "Q"


def main():
    # all background images loaded and scaled, for each level there is a
    # different background image
    bg_1_img = pygame.image.load ("graphics/background_1.jpg")
    bg_1_scale = pygame.transform.scale (bg_1_img, (600, 600))

    bg_2_img = pygame.image.load ("graphics/background_2.jpg")
    bg_2_scale = pygame.transform.scale (bg_2_img, (600, 600))

    bg_3_img = pygame.image.load ("graphics/background_3.jpg")
    bg_3_scale = pygame.transform.scale (bg_3_img, (600, 600))

    bg_4_img = pygame.image.load ("graphics/background_4.jpg")
    bg_4_scale = pygame.transform.scale (bg_4_img, (600, 600))

    bg_5_img = pygame.image.load ("graphics/background_5.jpg")
    bg_5_scale = pygame.transform.scale (bg_5_img, (600, 600))

    # images
    img_block = pygame.image.load ('graphics/block.png')
    img_spikes = pygame.image.load ('graphics/spikes.png')
    img_portal = pygame.image.load ('graphics/portal.png')

    img_player_i_1 = pygame.image.load ("graphics/player-idle-1.png")
    img_player_i_2 = pygame.image.load ("graphics/player-idle-2.png")
    img_player_j = pygame.image.load ("graphics/player-jump.png")
    img_player_w = pygame.image.load ("graphics/player-walk.png")

    img_enemy_w_1 = pygame.image.load ("graphics/enemy-walk-1.png")
    img_enemy_w_2 = pygame.image.load ("graphics/enemy-walk-2.png")
    img_enemy_w_3 = pygame.image.load ("graphics/enemy-walk-3.png")

    img_health_o = pygame.image.load ("graphics/health-outline.png")
    img_health = pygame.image.load ("graphics/health.png")

    img_bullet = pygame.image.load ("graphics/bullet.png")
    img_turret = pygame.image.load ("graphics/turret.png")
    img_turret_head = pygame.image.load ("graphics/turret-head.png")

    img_store = [
        pygame.transform.scale (img_portal, (20, 20)),  # portal size
        pygame.transform.scale (img_block, (20, 20)),  # block size
        pygame.transform.scale (img_spikes, (20, 20)),  # spike size
        [
            pygame.transform.scale (img_player_i_1, (20, 20)),  # player
            pygame.transform.scale (img_player_i_2, (20, 20)),
            pygame.transform.scale (img_player_j, (20, 20)),
            pygame.transform.scale (img_player_w, (20, 20)),
        ],
        [
            pygame.transform.scale (img_enemy_w_1, (20, 20)),  # enemy
            pygame.transform.scale (img_enemy_w_2, (20, 20)),
            pygame.transform.scale (img_enemy_w_3, (20, 20)),
        ],
        [
            pygame.transform.scale (img_bullet, (8, 8)),
            pygame.transform.scale (img_turret, (20, 20)),
            pygame.transform.scale (img_turret_head, (28, 28)),
        ]
    ]

    lvl_track = 0  # this is the index of the lvl_grid array to determine
    # what lvl it is

    # The basic grid setup of the maps, the maps/levels will be created
    # the following template
    lvl_grid = [  # - block, ^ - player, x - enemy, = - lava
        [
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                     #        ",
            "   @                       #  ",
            "  ###    #     #              ",
            "                        #     ",
            "                              ",
            "      #              #        ",
            "           #            #     ",
            "                              ",
            "                            # ",
            "                              ",
            "                        =     ",
            "                      # ###   ",
            "          =   x    =          ",
            "  #  #    ##########          ",
            "                              ",
            "                          ^   ",
            " #       =                   ",
            "  ############  #   # #  ### #",
        ],
        [
            "1                             ",
            "#           #             @   ",
            "                         ###  ",
            "         #                    ",
            "               #             #",
            "           #            #     ",
            "       #                    # ",
            "            #                 ",
            "                        #     ",
            "          =   #     ##        ",
            "          #              #    ",
            "    #             =           ",
            "       #     #    #    #  x  #",
            "                        ##### ",
            "    #        #    ##      #   ",
            "          #                   ",
            "    #           #      #      ",
            "        #    #                ",
            "               #    #         ",
            "  #       #              =    ",
            "                #        #    ",
            "      #    #         #    #   ",
            "  #                           ",
            "  ^       #      #        #   ",
            "                             1",
            " ###  ##    #    #    #      #",
            "                              ",
        ],
        [
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "    @         #   #           ",
            "    #    #             #      ",
            "                              ",
            "                 #            ",
            "                =             ",
            "               ##             ",
            "    #                         ",
            "       #  #                 = ",
            "                            # ",
            "  #                    #      ",
            "           =      #           ",
            "    #     x   #             # ",
            "     #########                ",
            "                        #     ",
            " #  =                         ",
            "    ####                #     ",
            "                              ",
            " ^                            ",
            "  #               =      x### ",
            " ##  #   ##  #    ########    ",
        ],
        [
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "       #                      ",
            "             #                ",
            "     #                      @ ",
            "          #             ##### ",
            "        #                     ",
            "    #            #           #",
            "      #                       ",
            "                      =   ##   ",
            "   #     ##  #   =    #     #  ",
            "       =         # ==          ",
            "      ##     #     ##       #  ",
            "  #                      #  ##",
            "      =#     =      #         ",
            "      #     ###         #     ",
            "                  #  # #      ",
            "    ^   #     xx           ## ",
            " #         =######=    #      ",
            "  #########       #####       ",
        ],
        [
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "       =x    x    x    =      ",
            "      ###################     ",
            " #                            ",
            "  #                       #   ",
            "       =                   =  ",
            "      ##                      ",
            " =                            ",
            " ##                          #",
            "       =                      ",
            "      ##                  #   ",
            " =                         =  ",
            " ##                           ",
            "       =                      ",
            "      ##                     #",
            " =                            ",
            " ##                         # ",
            "      =                # =====",
            "     ##                       ",
            " ^                         @  ",
            "   =           1     ### # #  ",
            " ###           #              ",
        ],
        [
            "                              ",
            "                              ",
            "                              ",
            "                              ",
            "       =x    x    x    =      ",
            "      ###################     ",
            " #                            ",
            "  #                       #   ",
            "       =                   =  ",
            "      ##                      ",
            " =                            ",
            " ##                          #",
            "       =                      ",
            "      ##                  #   ",
            " =                         =  ",
            " ##                           ",
            "       =                      ",
            "      ##                     #",
            " =                            ",
            " ##                         # ",
            "     @ =                # =====",
            "     ##                       ",
            " ^                            ",
            "   =           1     ### # #  ",
            " ###           #              ",
        ],
    ]

    block_arr = []  # stores Block objects
    player_arr = []  # stores Player object
    enemy_arr = []  # stores Enemy object
    bullet_arr = []

    objects = [block_arr, player_arr,
               enemy_arr, bullet_arr]  # stores all object lists

    load_map (lvl_grid, lvl_track, objects, img_store)  # creates objects
    # based on
    # their position in grid and appends them to their respective lists

    running = True  # feeds a constant loop that can be updated in real time

    reset_lvl = False  # initialises boolean to reset the level
    next_lvl = lvl_track  # initialises the level number
    player_dead = False  # initialises whether player is dead
    health = 100  # initialises health

    clock = pygame.time.Clock ()

    clock.tick (605)

    # music for menus is loaded, adjusted volumne and looped
    pygame.mixer.music.load ('sound/loading_screen_music.mp3')
    pygame.mixer.music.set_volume (0.2)
    pygame.mixer.music.play (-1)

    in_menus = True # loop for menus
    while (in_menus): # while the user is in the menus
        menu_screens = menu_screen () # creates variable for checking
        # return of function

        if (menu_screens == "Controls"): # if "controls" is returned
            menu_screens = controls_screen () # go into control menu

        if (menu_screens == "Start Game"): # if "start game" is returned
            in_menus = False #menus false, proceed to game loop

        if (menu_screens == "Back"): # if "back" is returned
            back = 0 # no change in return values, placeholder variable
            # to continue the code

        if (menu_screens == "Quit"): # if quit is returned
            in_menus = False # menus loop ends
            running = False # game loop does not start
            # game does not run

    # sets up screen for game
    screen = pygame.display.set_mode ( [600, 600])

    # unloads menu music
    pygame.mixer.music.unload ()

    # loads game background music, adjust volumne and loops
    pygame.mixer.music.load ('sound/background_sound.mp3')
    pygame.mixer.music.set_volume (0.2)
    pygame.mixer.music.play (-1)

    deaths = 1

    while running:

        # Note can use if statements in conjunctions with
        # lvl_track to change the background/blocks based on level

        # Changes background image for each level
        if (lvl_track == 0):
            screen.blit (bg_1_scale, [0, 0])
        elif (lvl_track == 1):
            screen.blit (bg_2_scale, [0, 0])
        elif (lvl_track == 2):
            screen.blit (bg_3_scale, [0, 0])
        elif (lvl_track == 3):
            screen.blit (bg_4_scale, [0, 0])
        elif (lvl_track == 4):
            screen.blit (bg_5_scale, [0, 0])

        tick_rate = 0
        tick_rate -= 1

        if (player_dead is True):  # if player is dead,
            deaths += 1
            if (deaths > 1):
                deaths = 0

            revive = revive_screen ()

            if (revive == "Y"):
                resurr = resurrection (deaths)  # Resurrection result
                # stored

                if (resurr == 0):  # If player fails resurrection
                    game_over = game_over_screen ()

                    if (game_over == "Quit"):
                        running = False

                    if (game_over == "Replay"):
                        block_arr = []  # resets block objects
                        player_arr = []  # resets player object
                        enemy_arr = []  # resets enemy objects
                        objects = [block_arr, player_arr, enemy_arr,
                                   bullet_arr]

                        lvl_track = 0
                        health = 100  # resets health
                        load_map (lvl_grid, lvl_track, objects, img_store)
                        reset_lvl = False  # resets boolean

                else:  # Player passed resurrection
                    reset_lvl = True  # reset level
                    next_lvl = lvl_track  # level remains the same
                    health = 100  # resets health
                    player_dead = False  # resets boolean

            elif (revive == "N"):
                game_over = game_over_screen ()

                if (game_over == "Quit"):
                    running = False

                if (game_over == "Replay"):
                    block_arr = []  # resets block objects
                    player_arr = []  # resets player object
                    enemy_arr = []  # resets enemy objects
                    objects = [block_arr, player_arr, enemy_arr,
                               bullet_arr]
                    lvl_track = 0
                    health = 100  # resets health
                    load_map (lvl_grid, lvl_track, objects, img_store)
                    reset_lvl = False  # resets boolean

            elif (revive == "Q"):
                running = False

        if (reset_lvl is True):  # if reset level is true,

            if (lvl_track < len(lvl_grid)):  # if level number is
                # less than
                # max levels
                block_arr = []  # resets block objects
                player_arr = []  # resets player object
                enemy_arr = []  # resets enemy objects
                objects = [block_arr, player_arr, enemy_arr, bullet_arr]

                lvl_track = next_lvl  # level number changes,appends objects again
                load_map (lvl_grid, lvl_track, objects, img_store)
                reset_lvl = False  # resets boolean

        # If user exits program
        for event in pygame.event.get ():

            if (event.type == pygame.QUIT):
                running = False

        for p in player_arr:  # player objects

            p.display (screen)  # displays player
            p.key_inputs ()  # allows key inputs
            player_dead = p.physics ()  # returns if player is dead

        for b in bullet_arr:
            b.display (screen)
            health = b.physics (player_arr, health)

        for b in block_arr:  # block objects

            block_type = b.get_type ()  # gets block type
            b.display (block_type, screen)  # displays block
            b.collision (player_arr)  # gets player object for collisions
            b.collision (enemy_arr)  # gets enemy object for collisions

            if (block_type == "portal"):  # if block type is portal,
                # if player touches portal, sets next level number + resets level
                reset_lvl, next_lvl = b.portal_next_lvl (player_arr,
                                                        lvl_track)

            if (block_type == "spikes"):  # if block type is spikes,
                # if player touches spike, lower health
                health = b.p_coll (player_arr, health)
                b.p_coll (enemy_arr, 0)

        for e in enemy_arr:  # enemy objects

            enemy_type = e.get_type ()

            e.physics ()  # enemy physics

            if (enemy_type == "melee"):
                e.m_display (screen)  # displays enemy
                health = e.collision (player_arr, health)  # collision
                # with player
                e.movement ()  # enemy physics

            if (enemy_type == "turret"):
                e.t_display (screen)  # displays enemy
                e.shoot_gun (player_arr, bullet_arr, screen)

        # health

        rect = Rect(10, 565, 202, 22)  # black outline

        health_text = health * 2  # health text

        surf_hp_o = pygame.transform.scale (img_health_o, (204, 24))  #
        # outline

        if (health >= 0):
            surf_hp = pygame.transform.scale (img_health, (round (
                health_text), 20))

        screen.blit (surf_hp_o, (200, 547))
        screen.blit (surf_hp, (202, 549))

        if (health <= 0):
            player_dead = True  # if health drops to 0, respawn

        # if the userb eats the final level
        if (lvl_track == 5):
            running = False # game is over
            game_completed_screen( ) # proceeds to game completed screen

        # flip display
        pygame.display.flip ()

    # quit pygame
    pygame.quit ()


# main
main()