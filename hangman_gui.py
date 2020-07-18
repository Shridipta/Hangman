import random
import pygame
from pygame import time
import time
from words import words_list

global hint_count

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Hangman")
icon = pygame.image.load("hangmanIco.png")
pygame.display.set_icon(icon)

pygame.mixer.music.set_volume(0.45)  # initializing the music system
pygame.mixer.music.load("videoplayback.wav")
pygame.mixer.music.play(-1)
click_sound = pygame.mixer.Sound("CLICKS.wav")
slide_down_sound = pygame.mixer.Sound("SLIDE_DOWN.wav")
correct_sound = pygame.mixer.Sound("CORRECT.wav")
worng_sound = pygame.mixer.Sound("INCORRECT.wav")
time_up_sound = pygame.mixer.Sound("TIME-UP.wav")

random_word = random.choice(words_list)  # initializing the game values

c = 0
showing_already = False
showing_worng = False
showing_correct = False
die = False
time_up = False
g = True
running = True

correct_guess = ["_" for item in random_word]
wrong_guess = []
already_guessed = []
r = [char.upper() for char in random_word]  # list of letters in the random word
start_ticks = pygame.time.get_ticks()
selection_dict = {}
clock = pygame.time.Clock()


def non_duplicater(string):
    non_duplicate_list = []
    new_string = ""
    for element in string:
        if element not in non_duplicate_list:
            non_duplicate_list.append(element)
    return new_string.join(non_duplicate_list)


def show_text(text, font_size, x, y):
    font = pygame.font.Font("freesansbold.ttf", int(font_size))
    font_render_text = font.render(str(text), True, (255, 255, 255))
    font_display_screen = screen.blit(font_render_text, (int(x), int(y)))


def join(iterable):  # with space
    join_str = ""
    for elements in iterable:
        join_str += " " + elements
    return join_str


def button_screen_2(mouse_pos, x_1, x_2, y_1, y_2, width, height):  # replay, surrender, hint
    if x_1 <= mouse_pos[0] <= x_2:
        if y_1 <= mouse_pos[1] <= y_2:
            pygame.draw.rect(screen, (225, 0, 0), (x_1, y_1, width, height), 0)  # button_replay


def stopwatch(secs_limit, sec_gap):  # for timed ones
    global time_up
    second = (secs_limit - (int(time.perf_counter()))) + sec_gap
    if second >= 0:
        minu = second // 60
        second = second % 60
        return f"{minu} mins, {second} secs"
    elif second <= 0:
        time_up = True
        return f"0 mins, 0 secs"


def screen_2(timer_seconds):
    global event_chr, already_guessed, running, die, backgroundImg, start_ticks, level_comp
    global clock, die_count
    global y, c, r, i, g, t
    global showing_worng, showing_already, showing_correct, correct_guess, hint, wrong_guess
    global random_word, level, no_game
    global sec_gap

    if die_count >= 9:
        die_count = 9
        die = True

    backgroundImg = pygame.image.load(f"hangmanImg{die_count}.png")

    if y != 0:
        y += 10

    screen.blit(backgroundImg, (0, y))

    show_text("MODE~ " + str(selection_dict["MODE"]), 19, 10, 15)

    if selection_dict["TIMED"] == "UNTIMED":
        show_text(selection_dict["TIMED"], 15, 45, 40)
        show_text(selection_dict["DIFFICULTY"], 15, 130, 40)
    else:
        if selection_dict["DIFFICULTY"] == "MODERATE":
            show_text(selection_dict["TIMED"], 15, 60, 40)
            show_text(selection_dict["DIFFICULTY"], 15, 100, 40)
        else:
            show_text(selection_dict["TIMED"], 15, 85, 40)
            show_text(selection_dict["DIFFICULTY"], 15, 125, 40)

    if level <= no_game:
        show_text(f"LEVEL {level}/{no_game}", 25, 270, 10)
    else:
        show_text(f"LEVEL {no_game}/{no_game}", 25, 270, 10)

    pygame.draw.rect(screen, (225, 0, 0), (100, 330, 100, 50), 3)  # button 1
    show_text("REPLAY", 21, 107, 346)

    pygame.draw.rect(screen, (225, 0, 0), (224, 330, 150, 50), 3)  # button 2
    show_text("SURRENDER", 21, 232, 346)

    pygame.draw.rect(screen, (225, 0, 0), (400, 330, 100, 50), 3)  # button 3
    show_text("HINT", 21, 425, 346)

    if hint > 0:
        show_text(f"HINT {str(hint)}", 25, 490, 10)  # hint counter
    elif hint <= 0:
        show_text(f"HINT 0", 25, 490, 10)  # hint counter

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            event_ord = event.key  # getting A, B, C...
            if 97 <= event_ord <= 122:
                event_chr = chr(event_ord - 32)
            else:
                event_chr = chr(event_ord)

            if event_chr in random_word.upper() and event_chr not in already_guessed:
                showing_correct = True
                correct_sound.play()
                for i in random_word.upper():  # changing the underscores with letters
                    if i == event_chr:
                        correct_guess[c] = event_chr
                    c += 1
                c = 0

            if event_chr not in random_word.upper() and event_chr not in already_guessed:
                wrong_guess.append(event_chr)
                showing_worng = True  # you guessed the worng letter
                worng_sound.play()
                die_count += 1

            if event_chr not in already_guessed:  # all the guessed letters
                already_guessed.append(event_chr)
                showing_already = False
            else:
                showing_already = True  # you have already guessed that letter

        if event.type == pygame.KEYUP:
            showing_worng = False
            showing_already = False
            showing_correct = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            pygame.display.update()
            mouse_pos = pygame.mouse.get_pos()

            button_screen_2(mouse_pos, 100, 200, 330, 380, 100, 50)  # replay
            button_screen_2(mouse_pos, 224, 374, 332, 382, 150, 50)  # surrender
            button_screen_2(mouse_pos, 400, 500, 332, 382, 100, 50)  # hint

            if 100 <= mouse_pos[0] <= 200:
                if 330 <= mouse_pos[1] <= 380:
                    random_word = random.choice(words_list)
                    correct_guess = ["_" for item in random_word]
                    r = [char.upper() for char in random_word]
                    already_guessed = []
                    die = False
                    sec_gap = int(time.perf_counter())
                    level = 1

            if 224 <= mouse_pos[0] <= 374:
                if 332 <= mouse_pos[1] <= 382:
                    die_count = 0
                    random_word = random.choice(words_list)
                    correct_guess = ["_" for item in random_word]
                    r = [char.upper() for char in random_word]
                    already_guessed = []
                    die = False
                    g = True
                    level = 1

            if 400 <= mouse_pos[0] <= 500 and 332 <= mouse_pos[1] <= 382:
                rand_choice_hint = random.choice(random_word.upper())
                if hint > 0:
                    while True:  # hint != 0 and not die and not time_up and correct_guess != r:
                        if hint != 0 and rand_choice_hint not in correct_guess and rand_choice_hint not in already_guessed:
                            for i in random_word.upper():
                                if i == rand_choice_hint:
                                    correct_guess[c] = i
                                c += 1
                            hint -= 1
                            c = 0
                            break
                        else:
                            rand_choice_hint = random.choice(random_word.upper())

    second = (pygame.time.get_ticks() - start_ticks) // 1000

    if not time_up and not die and correct_guess != r and level <= no_game:
        if selection_dict["TIMED"] != "UNTIMED":
            show_text(f"TIME: {stopwatch(timer_seconds, sec_gap)}", 23, 215, 35)
        else:
            show_text(f"TIME: 00", 23, 280, 35)

        show_text(join(correct_guess), 32, 265, 100)
        show_text("WRONG GUESSES: ", 15, 270, 220)
        show_text(join(wrong_guess), 32, 265, 250)

    elif die:
        show_text("OH NO! YOU DIED", 32, 260, 120)
        show_text("THE WORD WAS:", 20, 290, 195)
        show_text(random_word.upper(), 30, 290, 235)
        pygame.display.update()
        time.sleep(2)
        g = True

    elif correct_guess == r:
        show_text("LEVEL COMPLETED", 32, 250, 120)
        show_text("CORRECT THE WORD IS:", 20, 250, 210)
        show_text(random_word.upper(), 28, 300, 250)
        pygame.display.update()
        time.sleep(2)
        random_word = random.choice(words_list)
        level += 1
        correct_guess = ["_" for item in random_word]
        r = [char.upper() for char in random_word]
        already_guessed = []
        wrong_guess = []

        if selection_dict["MODE"] == "NORMAL":
            hint = len(non_duplicater(random_word)) - hint_count
            sec_gap = int(time.perf_counter())
            die_count = 2

    elif level > no_game:
        show_text("BRAVO!", 28, 345, 100)
        show_text("YOU ESCAPED", 28, 295, 140)
        show_text("ALL LEVELS COMPLETE", 24, 253, 230)
        pygame.display.update()
        time.sleep(3)
        hint = 0
        g = True
        level = 1

    elif time_up:
        if second < timer_seconds + 5:
            backgroundImg9 = pygame.image.load(f"hangmanImg9.png")
            screen.blit(backgroundImg9, (0, 0))
            show_text("TIME UP! YOU DIED", 32, 260, 120)
            show_text("THE WORD WAS:", 20, 290, 195)
            show_text(random_word.upper(), 30, 290, 235)
        else:
            g = True

    if showing_already:
        show_text("ALREADY GUESSED THAT LETTER", 18, 270, 160)
    if showing_worng:
        show_text("WORNG LETTER", 20, 330, 155)
    if showing_correct:
        if correct_guess != r:
            show_text("CORRECT!", 20, 330, 155)

    pygame.display.update()


timer = 0  # untimed
selection_dict["MODE"] = "NORMAL"
selection_dict["TIMED"] = "UNTIMED"
selection_dict["DIFFICULTY"] = "EASY"
hint = len(random_word.upper()) - 3
level = 1

if selection_dict["MODE"] == "NORMAL":
    die_count = 2
else:
    die_count = 0
no_game = 9

while running:
    if not g:
        if -240 > y > -260:
            slide_down_sound.play()
        screen_2(timer)

    if g:
        if selection_dict["MODE"] == "NORMAL":
            die_count = 2
        else:
            die_count = 0

        c = 0
        die = False
        showing_worng = False
        showing_correct = False
        showing_already = False
        time_up = False
        correct_guess = ["_" for item in random_word]
        already_guessed = []
        wrong_guess = []
        r = [char.upper() for char in random_word]  # list of letters in the random word
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()

        y = -300
        screen.fill((0, 0, 0))
        backgroundImg1 = pygame.image.load(f"hangmanImg9.png")
        screen.blit(backgroundImg1, (0, 0))

        show_text("HANGMAN", 30, 220, 20)
        show_text("WELCOME BACK!", 18, 273, 82)

        if selection_dict["MODE"] == "NORMAL":
            pygame.draw.rect(screen, (225, 0, 0), (275, 112, 100, 30), 0)  # button 1 outline
            show_text("NORMAL", 20, 280, 118)
            pygame.draw.rect(screen, (225, 0, 0), (390, 112, 110, 30), 3)  # button 1 outline
            show_text("SURVIVAL", 20, 395, 118)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (275, 112, 100, 30), 3)  # button 1 outline
            show_text("NORMAL", 20, 280, 118)
            pygame.draw.rect(screen, (225, 0, 0), (390, 112, 110, 30), 0)  # button 1 outline
            show_text("SURVIVAL", 20, 395, 118)

        show_text("TIMED?", 21, 278, 155)

        if selection_dict["TIMED"] != "30 S":
            pygame.draw.rect(screen, (225, 0, 0), (275, 184, 40, 20), 3)  # button 3 outline
            show_text("30 S", 15, 280, 188)

        else:
            pygame.draw.rect(screen, (225, 0, 0), (275, 184, 40, 20), 0)  # button 3 outline
            show_text("30 S", 15, 280, 188)
            timer = 30

        if selection_dict["TIMED"] != "1 M":
            pygame.draw.rect(screen, (225, 0, 0), (325, 184, 40, 20), 3)  # button 3 outline
            show_text("1 M", 15, 332, 188)

        else:
            pygame.draw.rect(screen, (225, 0, 0), (325, 184, 40, 20), 0)  # button 3 outline
            show_text("1 M", 15, 332, 188)
            timer = 60

        if selection_dict["TIMED"] != "2 M":
            pygame.draw.rect(screen, (225, 0, 0), (275, 212, 40, 20), 3)  # button 3 outline
            show_text("2 M", 15, 282, 216)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (275, 212, 40, 20), 0)  # button 3 outline
            show_text("2 M", 15, 282, 216)
            timer = 120

        if selection_dict["TIMED"] != "4 M":
            pygame.draw.rect(screen, (225, 0, 0), (325, 212, 40, 20), 3)  # button 3 outline
            show_text("4 M", 15, 332, 216)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (325, 212, 40, 20), 0)  # button 3 outline
            show_text("4 M", 15, 332, 216)
            timer = 240

        if selection_dict["TIMED"] != "UNTIMED":
            pygame.draw.rect(screen, (225, 0, 0), (390, 198, 111, 30), 3)  # button 3 outline
            show_text("UNTIMED", 20, 398, 205)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (390, 198, 111, 30), 0)  # button 3 outline
            show_text("UNTIMED", 20, 398, 205)

        show_text("DIFFICULTY?", 21, 278, 243)

        if selection_dict["DIFFICULTY"] != "EASY":
            pygame.draw.rect(screen, (225, 0, 0), (272, 268, 68, 28), 3)  # button 3 outline
            show_text("EASY", 18, 280, 274)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (272, 268, 68, 28), 0)  # button 3 outline
            show_text("EASY", 18, 280, 274)

        if selection_dict["DIFFICULTY"] != "MODERATE":
            pygame.draw.rect(screen, (225, 0, 0), (353, 268, 118, 28), 3)  # button 3 outline
            show_text("MODERATE", 18, 360, 274)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (353, 268, 118, 28), 0)  # button 3 outline
            show_text("MODERATE", 18, 360, 274)

        if selection_dict["DIFFICULTY"] != "HARD":
            pygame.draw.rect(screen, (225, 0, 0), (486, 268, 68, 28), 3)  # button 3 outline
            show_text("HARD", 18, 493, 274)
        else:
            pygame.draw.rect(screen, (225, 0, 0), (486, 268, 68, 28), 0)  # button 3 outline
            show_text("HARD", 18, 493, 274)

        pygame.draw.rect(screen, (225, 0, 0), (248, 330, 120, 50), 3)  # button 3 outline
        show_text("START", 21, 272, 345)

        sec_gap = int(time.perf_counter())

        for event_s1 in pygame.event.get():
            if event_s1.type == pygame.QUIT:
                running = False
            if event_s1.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos_s1 = pygame.mouse.get_pos()

                if 275 <= mouse_pos_s1[0] <= 375 and 112 <= mouse_pos_s1[1] <= 142:
                    pygame.draw.rect(screen, (225, 0, 0), (275, 112, 100, 30), 0)  # button 1 outline
                    selection_dict["MODE"] = "NORMAL"
                    die_count = 3

                if 390 <= mouse_pos_s1[0] <= 500 and 112 <= mouse_pos_s1[1] <= 142:
                    pygame.draw.rect(screen, (225, 0, 0), (390, 112, 110, 30), 0)  # button 1 outline
                    selection_dict["MODE"] = "SURVIVAL"
                    die_count = 0

                if 390 <= mouse_pos_s1[0] <= 501 and 198 <= mouse_pos_s1[1] <= 220:
                    pygame.draw.rect(screen, (225, 0, 0), (390, 198, 111, 30), 0)  # button 3 outline
                    selection_dict["TIMED"] = "UNTIMED"
                    no_game = 9

                if 275 <= mouse_pos_s1[0] <= 310 and 184 <= mouse_pos_s1[1] <= 204:
                    selection_dict["TIMED"] = "30 S"
                    timer = 30
                    no_game = 1

                if 325 <= mouse_pos_s1[0] <= 360 and 184 <= mouse_pos_s1[1] <= 204:
                    selection_dict["TIMED"] = "1 M"
                    timer = 60
                    no_game = 2

                if 275 <= mouse_pos_s1[0] <= 315 and 212 <= mouse_pos_s1[1] <= 232:
                    selection_dict["TIMED"] = "2 M"
                    timer = 120
                    no_game = 4

                if 325 <= mouse_pos_s1[0] <= 365 and 212 <= mouse_pos_s1[1] <= 232:
                    selection_dict["TIMED"] = "4 M"
                    timer = 240
                    no_game = 6

                if 272 <= mouse_pos_s1[0] <= 272 + 68 and 268 <= mouse_pos_s1[1] <= 268 + 28:
                    selection_dict["DIFFICULTY"] = "EASY"
                    hint_count = 3
                    hint = len(non_duplicater(random_word)) - hint_count

                if 353 <= mouse_pos_s1[0] <= 353 + 118 and 268 <= mouse_pos_s1[1] <= 268 + 28:
                    selection_dict["DIFFICULTY"] = "MODERATE"
                    hint_count = 4
                    hint = len(non_duplicater(random_word)) - hint_count

                if 486 <= mouse_pos_s1[0] <= 486 + 68 and 268 <= mouse_pos_s1[1] <= 268 + 28:
                    selection_dict["DIFFICULTY"] = "HARD"
                    hint_count = 5
                    hint = len(non_duplicater(random_word)) - hint_count

                if 248 <= mouse_pos_s1[0] <= 368 and 330 <= mouse_pos_s1[1] <= 380:  # screen_1 start button
                    screen.fill((0, 0, 0))
                    g = False

                if g:
                    click_sound.play()

        pygame.display.flip()
        if selection_dict["MODE"] == "SURVIVAL":
            if selection_dict["DIFFICULTY"] == "EASY":
                hint = 14
            if selection_dict["DIFFICULTY"] == "MODERATE":
                hint = 8
            if selection_dict["DIFFICULTY"] == "HARD":
                hint = 4

    pygame.display.update()
