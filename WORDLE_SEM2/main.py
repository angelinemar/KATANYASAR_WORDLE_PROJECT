import pygame
import moviepy.editor as mp
import os
import sys
import random
from words import *

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 650, 750
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
CORRECT_WORD = "bread"
ALPHABET = ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"]
GUESSED_LETTER_FONT_PATH = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\FreeSansBold.otf"
AVAILABLE_LETTER_FONT_PATH = GUESSED_LETTER_FONT_PATH

# Setup display and video
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("projek apa ni")

video_path = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_cth.mp4"
video = mp.VideoFileClip(video_path)
audio_path = "temp_audio.mp3"
video.audio.write_audiofile(audio_path)
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play(-1)

ICON = pygame.image.load("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\Icon.png")
pygame.display.set_icon(ICON)

ENTER_SOUND = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\button_1.ogg")
TYPE_SOUND = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\type.ogg")

GUESSED_LETTER_FONT = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 50)
AVAILABLE_LETTER_FONT = pygame.font.Font(AVAILABLE_LETTER_FONT_PATH, 25)

# Global variables
guesses_count = 0
guesses = [[] for _ in range(5)]
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
        self.bg_rect = (self.bg_x, self.bg_y + 120, LETTER_SIZE, LETTER_SIZE - 10)
        self.text = text
        self.text_position = (self.bg_x + 37, self.bg_y + 150)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect, border_radius=10)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3, border_radius=10)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)

    def delete(self):
        pygame.draw.rect(SCREEN, "white", self.bg_rect, border_radius=10)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3, border_radius=10)

class Indicator:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 55, 55)
        self.bg_color = OUTLINE

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.rect, border_radius=0)
        self.text_surface = AVAILABLE_LETTER_FONT.render(self.text, True, "black")
        self.text_rect = self.text_surface.get_rect(center=(self.x + 25, self.y + 25))
        SCREEN.blit(self.text_surface, self.text_rect)

# Create indicators
indicator_x, indicator_y = 40, 0
for row in ALPHABET:
    total_row_width = len(row) * LETTER_X_SPACING
    indicator_x = -2
    for letter in row:
        new_indicator = Indicator(indicator_x, indicator_y, letter)
        indicators.append(new_indicator)
        indicator_x += 50
    indicator_y += 50

def check_guess(guess_to_check):
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
    
    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 110

    if guesses_count == 5 and game_result == "":
        game_result = "L"

def play_again():
    pygame.draw.rect(SCREEN, "grey", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 50)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 700))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)

def reset():
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result
    SCREEN.fill("grey")
    first_frame = video.get_frame(0)
    first_frame_surface = pygame.surfarray.make_surface(first_frame.swapaxes(0, 1))
    SCREEN.blit(first_frame_surface, (0, 0))
    guesses_count = 0
    CORRECT_WORD = random.choice(WORDS)
    guesses = [[] for _ in range(5)]
    current_guess = []
    current_guess_string = ""
    game_result = ""
    for indicator in indicators:
        indicator.bg_color = OUTLINE
        indicator.draw()
    pygame.mixer.music.play(-1) 
    
def create_new_letter(key_pressed):
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count * 75 + LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    global current_guess_string, current_letter_bg_x
    if len(guesses[guesses_count]) > 0:
        guesses[guesses_count][-1].delete()
        guesses[guesses_count].pop()
        current_guess_string = current_guess_string[:-1]
        current_guess.pop()
        current_letter_bg_x -= LETTER_X_SPACING

clock = pygame.time.Clock()
fps = video.fps
start_time = pygame.time.get_ticks()

while True:
    current_time = (pygame.time.get_ticks() - start_time) / 1000.0

    if current_time < video.duration:
        frame = video.get_frame(current_time)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        SCREEN.blit(frame_surface, (0, 0))
    else:
        start_time = pygame.time.get_ticks()
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
                        if game_result != "":
                            play_again()
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM":
                    if len(current_guess_string) < 5:
                        create_new_letter(key_pressed)
                        TYPE_SOUND.play()

    for guess in guesses:
        for letter in guess:
            letter.draw()

    for indicator in indicators:
        indicator.draw()

    pygame.display.update()
    clock.tick(fps)

os.remove(audio_path)
