import pygame
import pygame.mixer
import pkg_resources
import os
import sys
import random
from words import *
#ini nat tes
pygame.init()
pygame.mixer.init()
# ASSET DISPLAY AND SFX SEMUA
WIDTH, HEIGHT = 900, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(200, 200))
ICON = pygame.image.load("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\Icon.png")
ENTER_SOUND = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\button_1.ogg")
TYPE_SOUND = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\type.ogg")
pygame.display.set_caption("projek apa ni")
pygame.display.set_icon(ICON)
BACKGROUND = pygame.image.load("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_test.jpeg")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
CORRECT_WORD = "bread"
ALPHABET = ["ABCDEFGH", "IJKLMNOP", "QRSTUVWXYZ"]
GUESSED_LETTER_FONT = pygame.font.Font("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\FreeSansBold.otf", 25)
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
pygame.display.update()
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75

# VARIABLE GLOBAL
guesses_count = 0
guesses = [[]] * 6
current_guess = []
current_guess_string = ""
current_letter_bg_x = 110
indicators = []
game_result = ""

class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (self.bg_x, self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x + 36, self.bg_y + 30)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect, border_radius=10)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3, border_radius=10)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        pygame.draw.rect(SCREEN, "white", self.bg_rect, border_radius=10)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3, border_radius=10)
        pygame.display.update()

class Indicator:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 55, 55)
        self.bg_color = OUTLINE

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, border_radius=10)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=(self.x + 27, self.y + 30))
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

indicator_x, indicator_y = 20, 600

for row in ALPHABET:
    total_row_width = len(row) * LETTER_X_SPACING  
    indicator_x = (WIDTH - total_row_width) // 2 
    for letter in row:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += LETTER_X_SPACING
    indicator_y += 100

def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].text.lower()
        if lowercase_letter in CORRECT_WORD:
            if lowercase_letter == CORRECT_WORD[i]:
                guess_to_check[i].bg_color = GREEN
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = GREEN
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    game_result = "W"
            else:
                guess_to_check[i].bg_color = YELLOW
                for indicator in indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = YELLOW
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                game_result = ""
                game_decided = True
        else:
            guess_to_check[i].bg_color = GREY
            for indicator in indicators:
                if indicator.text == lowercase_letter.upper():
                    indicator.bg_color = GREY
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            game_result = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()
    
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 110

    if guesses_count == 6 and game_result == "":
        game_result = "L"

def play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "grey", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\FreeSansBold.otf", 50)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 700))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill("grey")
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    guesses_count = 0
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[]] * 6
    current_guess = []
    current_guess_string = ""
    game_result = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()

def create_new_letter():
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*100+LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING

while True:
    if game_result != "":
        play_again()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
                        check_guess(current_guess)
                        ENTER_SOUND.play()
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < 5:
                        create_new_letter()
                        TYPE_SOUND.play()
