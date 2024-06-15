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
GUESSED_LETTER_FONT_PATH = "D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\TypoSlab.otf"
#GUESSED_LETTER_FONT_PATH = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\TypoSlab.otf"
AVAILABLE_LETTER_FONT_PATH = GUESSED_LETTER_FONT_PATH

# Setup display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NYASAR KATA GAME")

# Load assets
# jenni
#video_path = "D:\\Punyaku\\Python_FInal_Project_Wordle\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_ingame.mp4"
#video_path_2 = "D:\\Punyaku\\Python_FInal_Project_Wordle\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_vid.mp4"
#video = mp.VideoFileClip(video_path)
#video2 = mp.VideoFileClip(video_path_2)

#winScene
#win_video = mp.VideoFileClip("D:\\Punyaku\\Python_FInal_Project_Wordle\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\win_video.mp4")
#lose_video = mp.VideoFileClip("D:\\Punyaku\\Python_FInal_Project_Wordle\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\lose_video.mp4")

#jason
win_video = mp.VideoFileClip("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\win_video.mp4")
lose_video = mp.VideoFileClip("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\lose_video.mp4")
video_path = "D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\bg_ingame.mp4"
video_path_2 = "D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\bg_vid.mp4"
video = mp.VideoFileClip(video_path)
video2 = mp.VideoFileClip(video_path_2)

# angel
#win_video = mp.VideoFileClip("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\win_video.mp4")
#lose_video = mp.VideoFileClip("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\lose_video.mp4")
#video_path = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_ingame.mp4"
#video_path_2 = "C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\bg_vid.mp4"
#video = mp.VideoFileClip(video_path)
#video2 = mp.VideoFileClip(video_path_2)

# Extract audio from the main video
#audio_path = "/Users/jennifernathaniahartono/Documents/WORDLE_PROJ_SEM2-4/WORDLE_SEM2/assets/sfx/gamelan.mp3"
#audio = pygame.mixer.music.load(audio_path)
#audio_sound = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\gamelan.mp3")
audio_sound = pygame.mixer.Sound("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\sfx\\gamelan.mp3")

# # Directly load the MP3 if available
# try:
#     if not os.path.exists(audio_path):
#         # Extract audio only if the mp3 doesn't exist
#         video.audio.write_audiofile(audio_path)
# except Exception as e:
#     print(f"Error extracting audio: {e}")


# Load other assets
ICON = pygame.image.load("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\tiles.png")
#ICON = pygame.image.load("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\tiles.png")

pygame.display.set_icon(ICON)

ENTER_SOUND = pygame.mixer.Sound("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\sfx\\button_1.ogg")
TYPE_SOUND = pygame.mixer.Sound("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\sfx\\type.ogg")
#ENTER_SOUND = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\button_1.ogg")
#TYPE_SOUND = pygame.mixer.Sound("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\sfx\\type.ogg")
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
        SCREEN.blit(self.text_surface, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class WhiteButton:
    def __init__(self, text, position, font, text_color="white"):
        self.text = text
        self.position = position
        self.font = font
        self.text_color = text_color
        self.render()

    def render(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.text_surface.get_rect(center=self.position)

    def draw(self):
        SCREEN.blit(self.text_surface, self.rect)

    def is_clicked(self, mouse_position):
        return self.rect.collidepoint(mouse_position)

class ToggleButton:
    def __init__(self, x, y, width, height, text_on, text_off, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_on = text_on
        self.text_off = text_off
        self.font = font
        self.state = True
        self.update_text()

    def update_text(self):
        text = self.text_on if self.state else self.text_off
        self.text_surface = self.font.render(text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        SCREEN.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                self.update_text()
                pygame.mixer.Sound.set_volume(TYPE_SOUND, 1 if self.state else 0)
                pygame.mixer.Sound.set_volume(ENTER_SOUND, 1 if self.state else 0)

class VolumeButton:
    def __init__(self, x, y, width, height, text_on, text_off, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_on = text_on
        self.text_off = text_off
        self.font = font
        self.sound = audio_sound
        self.volume_levels = [0, 0.25, 0.5, 0.75, 1.00]
        self.current_level_index = 4  # Start at 0.5 volume
        self.state = True
        self.update_text()

    def update_text(self):
        current_volume = self.volume_levels[self.current_level_index]
        text = f"{self.text_on} {int(current_volume * 100)}%" if self.state else self.text_off
        self.text_surface = self.font.render(text, True, "white")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        SCREEN.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Cycle through the volume levels
                self.current_level_index = (self.current_level_index + 1) % len(self.volume_levels)
                new_volume = self.volume_levels[self.current_level_index]
                self.sound.set_volume(new_volume)
                self.state = new_volume > 0
                self.update_text()


class OpeningScene:
    def __init__(self):
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 30)
        self.start_button = Button("S T A R T   ", (335, 441), self.button_font)
        self.settings_button = Button("S E T T I N G S", (325, 551), self.button_font)
        self.credits_button = WhiteButton("C R E D I T S", (325, 661), self.button_font)
        self.exit_button = WhiteButton("EXIT", (600, 40), self.button_font)
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
        self.credits_button.draw()
        self.exit_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        #pygame.mixer.music.load(audio_path)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos):
                reset()
                current_scene = "gameplay"
                video_start_time = pygame.time.get_ticks()  #Update global video_start_time
                audio_sound.stop()
            elif self.settings_button.is_clicked(event.pos):
                current_scene = "settings"
                video_start_time = pygame.time.get_ticks()  #Update global video_start_time
            elif self.credits_button.is_clicked(event.pos):
                current_scene = "credits"
                video_start_time = pygame.time.get_ticks()
            elif self.exit_button.is_clicked(event.pos):
                pygame.quit()
                sys.exit()

class CreditScene:
    def __init__(self):
        self.title_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 75)
        self.text_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 30)
        self.back_button = WhiteButton("Back", (WIDTH / 2, HEIGHT - 100), self.text_font)
        
    def draw(self):
        frame = video.get_frame(current_time)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        SCREEN.blit(frame_surface, (0, 0))
        title_surface = self.title_font.render("Credits", True, "white")
        title_rect = title_surface.get_rect(center=(WIDTH / 2, 160))
        SCREEN.blit(title_surface, title_rect)
        
        credits_text = [
            "Game developed by:",
            "Angel 112006217",
            "Jeni 112006202",
            "Natalie 112000262",
            "There 112006221",
            "Jason 112006227"
        ]
        
        y_offset = 220
        for line in credits_text:
            text_surface = self.text_font.render(line, True, "white")
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y_offset))
            SCREEN.blit(text_surface, text_rect)
            y_offset += 50

        self.back_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_clicked(event.pos):
                current_scene = "opening"
                video_start_time = pygame.time.get_ticks()

class SettingsScene:
    def __init__(self):
        self.title_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 75)
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 50)
        self.back_button = WhiteButton("Back", (WIDTH // 2, 600), self.button_font)
        self.volume_button = VolumeButton(WIDTH//4, 275, 325, 50, "Volume", "Muted", self.button_font)
        self.sfx_button = ToggleButton(225, 400, 200, 50, "SFX: ON", "SFX: OFF", self.button_font)
        self.video_start_time = pygame.time.get_ticks()  # Initialize local video_start_time

    def draw(self):
        frame = video.get_frame(current_time)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        SCREEN.blit(frame_surface, (0, 0))
        title_surface = self.title_font.render("Settings", True, "white")
        title_rect = title_surface.get_rect(center=(WIDTH / 2, 175))
        SCREEN.blit(title_surface, title_rect)
        self.volume_button.draw()
        self.sfx_button.draw()
        self.back_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        self.volume_button.handle_event(event)
        self.sfx_button.handle_event(event)
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
                reset()
                current_scene = "gameplay"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                audio_sound.stop()
            elif self.main_menu_button.is_clicked(event.pos):
                current_scene = "opening"
                audio_sound.play()
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                
# def play_again():
#     pygame.draw.rect(SCREEN, "grey", (10, 600, 1000, 600))
#     play_again_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 50)
#     play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
#     play_again_rect = play_again_text.get_rect(center=(WIDTH / 2, 700))
#     word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
#     word_was_rect = word_was_text.get_rect(center=(WIDTH / 2, 650))
#     SCREEN.blit(word_was_text, word_was_rect)
#     SCREEN.blit(play_again_text, play_again_rect)
class LoseScene:
    def __init__(self):
        self.button_font = pygame.font.Font(GUESSED_LETTER_FONT_PATH, 30)
        self.play_again_button = Button("P L A Y  G A M E ", (335, 425), self.button_font)
        self.main_menu_button = Button("M A I N  M E N U ", (325, 540), self.button_font)
        self.video_start_time = pygame.time.get_ticks()  # Initialize local video_start_time
        self.answer_font = pygame.font.Font("D:\\Libraries\\Documents\\GitHub\\WORDLE_PROJ_SEM2\WORDLE_SEM2\\assets\\TypoSlab.otf", 50)
        #self.answer_font = pygame.font.Font("C:\\Users\\Angeline\\Documents\\GitHub\\WORDLE_PROJ_SEM2\\WORDLE_SEM2\\assets\\TypoSlab.otf", 50)
    def draw(self):
        current_time = (pygame.time.get_ticks() - self.video_start_time) / 1000.0
        if current_time < lose_video.duration:
            frame = lose_video.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            SCREEN.blit(frame_surface, (0, 0))
        else:
            self.video_start_time = pygame.time.get_ticks()
        #pygame.mixer.music.play(-1)
        static_text = "The word was"
        static_text_surface = self.button_font.render(static_text, True, "black")
        static_text_rect = static_text_surface.get_rect(center=(WIDTH / 2 - 70, 350))
        SCREEN.blit(static_text_surface, static_text_rect)

        correct_word_text_surface = self.answer_font.render(CORRECT_WORD.upper(), True, "red")
        correct_word_text_rect = correct_word_text_surface.get_rect(center=(WIDTH/2 + 120 , 350))
        SCREEN.blit(correct_word_text_surface, correct_word_text_rect)

        self.play_again_button.draw()
        self.main_menu_button.draw()

    def handle_event(self, event):
        global current_scene, video_start_time
        #pygame.mixer.music.load(audio_path)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_button.is_clicked(event.pos):
                reset()
                current_scene = "gameplay"
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time
                audio_sound.stop()
            elif self.main_menu_button.is_clicked(event.pos):
                current_scene = "opening"
                audio_sound.play()
                video_start_time = pygame.time.get_ticks()  # Update global video_start_time

first_round = True
def reset():
    global guesses_count, guesses, current_guess, current_guess_string, current_letter_bg_x, game_result, current_scene, video_start_time, CORRECT_WORD, first_round
    guesses_count = 0
    if first_round:
        CORRECT_WORD = "ajaib"  # First round word
        first_round = False
    else:
        CORRECT_WORD = random.choice(WORDS)  # Randomize the correct word for subsequent rounds
    guesses = [[] for _ in range(5)]
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 110
    game_result = ""
    current_scene = "opening"  # Reset to opening scene
    for indicator in indicators:
        indicator.bg_color = OUTLINE
    video_start_time = pygame.time.get_ticks()
    
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
credit_scene = CreditScene()
audio_sound.play()
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
        
        elif current_scene == "credits":
            credit_scene.handle_event(event)

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
        elif current_scene == "credits":
            credit_scene.draw()
        elif current_scene == "win":
            win_scene.draw()
        elif current_scene == "lose":
            lose_scene.draw()

    pygame.display.update()
    clock.tick(fps)

# Clean up temporary files if they were created
if not os.path.exists(audio_path):
    os.remove(audio_path)
