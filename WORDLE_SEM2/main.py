import pygame
import os
import moviepy.editor as mp
import random
import sys
from words import *

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 650, 750
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"
CORRECT_WORD = "ajaib"
ALPHABET = ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"]
GUESSED_LETTER_FONT_PATH = "/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-5/WORDLE_SEM2/assets/sfx/TypoSlab.otf"
AVAILABLE_LETTER_FONT_PATH = GUESSED_LETTER_FONT_PATH

# Setup display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NYASAR KATA GAME")

# Load assets
# jenni
video_path = "/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-5/WORDLE_SEM2/assets/bg_ingame.mp4"
video_path_2 = "/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-5/WORDLE_SEM2/assets/bg_vid.mp4"
video = mp.VideoFileClip(video_path)
video2 = mp.VideoFileClip(video_path_2)

#winScene
win_video = mp.VideoFileClip("/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-5/WORDLE_SEM2/assets/win_video.mp4")
lose_video = mp.VideoFileClip("/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-5/WORDLE_SEM2/assets/lose_video.mp4")

# angel
# video_path = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_cth.mp4"
# video_path_2 = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_vid.mp4"
# video = mp.VideoFileClip(video_path)
# video2 = mp.VideoFileClip(video_path_2)

# Extract audio from the main video
#audio_path = "/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-4/WORDLE_SEM2/assets/sfx/gamelan.mp3"
#audio = pygame.mixer.music.load(audio_path)
audio_sound = pygame.mixer.Sound("/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-5/WORDLE_SEM2/assets/sfx/gamelan.mp3")

# # Directly load the MP3 if available
# try:
#     if not os.path.exists(audio_path):
#         # Extract audio only if the mp3 doesn't exist
#         video.audio.write_audiofile(audio_path)
# except Exception as e:
#     print(f"Error extracting audio: {e}")


# Load other assets
ICON = pygame.image.load("/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2/WORDLE_SEM2/assets/tiles.png")

pygame.display.set_icon(ICON)

ENTER_SOUND = pygame.mixer.Sound("/Users/jennifernathaniahartono/Documents/GitHub/WORDLE_PROJ_SEM2/WORDLE_SEM2/assets/sfx/button_1.ogg")
TYPE_SOUND = pygame.mixer.Sound("/Users/jennifernathaniahartono/Documents/GitHub/WORDLE_PROJ_SEM2/WORDLE_SEM2/assets/sfx/type.ogg")

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
current_scene = "opening"  # New variable to track the current scene
video_start_time = pygame.time.get_ticks()  # Initialize video_start_time

class Button:
    def __init__(self, text, position, font):
        self.text = text
        self.position = position
        self.font = font
        self.text_surface = self.font.render(self.text, True, "#516061")
        self.rect = self.text_surface.get_rect(center=self.position)
        
    def draw(self):
        audio_sound.play()
        SCREEN.blit(self.text_surface, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class OpeningScene:
    def __init__(self):
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 30)
        self.start_button = Button(   "S T A R T   ", (335, 441), self.button_font)
        self.settings_button = Button("S E T T I N G S", (325, 551), self.button_font)
        self.video_start_time = pygame.time.get_ticks()  # Initialize local video_start_time
        
    def draw(self):
        current_time = (pygame.time.get_ticks() - self.video_start_time) / 1000.0
        if current_time < video2.duration:
            frame = video2.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            SCREEN.blit(frame_surface, (0, 0))
        else:
            self.video_start_time = pygame.time.get_ticks()
        #pygame.mixer.music.play(-1)
        self.start_button.draw()
        self.settings_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        #pygame.mixer.music.load(audio_path)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos):
                current_scene = "gameplay"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                audio_sound.stop()
            elif self.settings_button.is_clicked(event.pos):
                current_scene = "settings"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time

class SettingsScene:
    def __init__(self):
        self.title_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 75)
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 50)
        self.back_button = Button("Back", (225, 500), self.button_font)
        self.video_start_time = pygame.time.get_ticks()  # Initialize local video_start_time

    def draw(self):
        SCREEN.fill("black")
        title_surface = self.title_font.render("Settings", True, "white")
        title_rect = title_surface.get_rect(center=(WIDTH / 2, 150))
        SCREEN.blit(title_surface, title_rect)
        self.back_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event.pos):
                current_scene = "opening"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time

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
                    game_decided = True
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

# def play_again():
#     pygame.draw.rect(SCREEN, "grey", (10, 600, 1000, 600))
#     play_again_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 50)
#     play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
#     play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 700))
#     word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
#     word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 650))
#     SCREEN.blit(word_was_text, word_was_rect)
#     SCREEN.blit(play_again_text, play_again_rect)

class WinScene:
    def __init__(self):
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 30)
        self.play_again_button = Button(   " P L A Y  G A M E ", (335, 386), self.button_font)
        self.main_menu_button = Button("   M A I N  M E N U ", (325, 505), self.button_font)
        self.video_start_time = pygame.time.get_ticks()  # Initialize local video_start_time
        
    def draw(self):
        current_time = (pygame.time.get_ticks() - self.video_start_time) / 1000.0
        if current_time < win_video.duration:
            frame = win_video.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            SCREEN.blit(frame_surface, (0, 0))
        else:
            self.video_start_time = pygame.time.get_ticks()
        #pygame.mixer.music.play(-1)
        self.play_again_button.draw()
        self.main_menu_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        #pygame.mixer.music.load(audio_path)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_button.is_clicked(event.pos):
                current_scene = "gameplay"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                audio_sound.stop()
            elif self.main_menu_button.is_clicked(event.pos):
                current_scene = "opening"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                
class LoseScene:
    def __init__(self):
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 30)
        self.play_again_button = Button(   "P L A Y  G A M E ", (335, 425), self.button_font)
        self.main_menu_button = Button("M A I N  M E N U ", (325, 540), self.button_font)
        self.video_start_time = pygame.time.get_ticks()  # Initialize local video_start_time
        
    def draw(self):
        current_time = (pygame.time.get_ticks() - self.video_start_time) / 1000.0
        if current_time < lose_video.duration:
            frame = lose_video.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            SCREEN.blit(frame_surface, (0, 0))
        else:
            self.video_start_time = pygame.time.get_ticks()
        #pygame.mixer.music.play(-1)
        self.play_again_button.draw()
        self.main_menu_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        #pygame.mixer.music.load(audio_path)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_button.is_clicked(event.pos):
                current_scene = "gameplay"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                audio_sound.stop()
            elif self.main_menu_button.is_clicked(event.pos):
                current_scene = "opening"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time

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

opening_scene = OpeningScene()
settings_scene = SettingsScene()
win_scene = WinScene()
lose_scene = LoseScene()

while True:
    if current_scene == "gameplay":
        current_time = (pygame.time.get_ticks() - video_start_time) / 1000.0
        
        if current_time < video.duration:
            frame = video.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            SCREEN.blit(frame_surface, (0, 0))
        else:
            video_start_time = pygame.time.get_ticks()
    else:
        current_time = 0  # Reset current time for other scenes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_scene == "opening":
            opening_scene.handle_event(event)
        
        elif current_scene == "settings":
            settings_scene.handle_event(event)

        if current_scene == "gameplay":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_result != "":
                        reset()
                    else:
                        if len(current_guess_string) == 5 and current_guess_string.lower() in WORDS:
                            check_guess(current_guess)
                            ENTER_SOUND.play()
                            if game_result == "W":
                                current_scene = "win"
                            elif game_result == "L":
                                current_scene = "lose"
                elif event.key == pygame.K_BACKSPACE:
                    if len(current_guess_string) > 0 and game_result == "":
                        delete_letter()
                else:
                    key_pressed = event.unicode.upper()
                    if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and game_result == "":
                        if len(current_guess_string) < 5:
                            create_new_letter(key_pressed)
                            TYPE_SOUND.play()
                            
        if current_scene == "win":
            win_scene.handle_event(event)
            
        elif current_scene == "lose":
            lose_scene.handle_event(event)

    if current_scene == "gameplay":
        for guess in guesses:
            for letter in guess:
                letter.draw()

        for indicator in indicators:
            indicator.draw()

        # Start the video and audio when entering the gameplay scene
        if not pygame.mixer.music.get_busy():
            #pygame.mixer.music.play(-1)
            video_start_time = pygame.time.get_ticks()

    else:
        # Stop the video and audio when leaving the gameplay scene
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        if current_scene == "opening":
            opening_scene.draw()
        elif current_scene == "settings":
            settings_scene.draw()
        elif current_scene == "win":
            win_scene.draw()
        elif current_scene == "lose":
            lose_scene.draw()

    pygame.display.update()
    clock.tick(fps)

# Clean up temporary files if they were created
if not os.path.exists(audio_path):
    os.remove(audio_path)
