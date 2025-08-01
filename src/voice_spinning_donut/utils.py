import logging
import re
from queue import Queue

import numpy as np
import pygame
import speech_recognition as sr
from word2number import w2n

from .config import BLACK, CIRCLE_POINTS, ILLUMINATION, K1, K2, PHI_SPACING, R1, R2, SCREEN_SIZE, THETA_SPACING, COLOR_THEMES


def render_frame(angle_a: float, angle_b: float) -> np.ndarray:
    cos_a = np.cos(angle_a)
    sin_a = np.sin(angle_a)
    cos_b = np.cos(angle_b)
    sin_b = np.sin(angle_b)

    output = np.full((SCREEN_SIZE, SCREEN_SIZE), " ")
    zbuffer = np.zeros((SCREEN_SIZE, SCREEN_SIZE))

    cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, PHI_SPACING))
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, THETA_SPACING))
    sin_theta = np.sin(theta)
    circle_x = R2 + R1 * cos_theta
    circle_y = R1 * sin_theta

    x = (np.outer(cos_b * cos_phi + sin_a * sin_b * sin_phi, circle_x) - circle_y * cos_a * sin_b).T
    y = (np.outer(sin_b * cos_phi - sin_a * cos_b * sin_phi, circle_x) + circle_y * cos_a * cos_b).T
    z = ((K2 + cos_a * np.outer(sin_phi, circle_x)) + circle_y * sin_a).T
    ooz = np.reciprocal(z)
    xp = (SCREEN_SIZE / 2 + K1 * ooz * x).astype(int)
    yp = (SCREEN_SIZE / 2 - K1 * ooz * y).astype(int)
    l1 = (np.outer(cos_phi, cos_theta) * sin_b) - cos_a * np.outer(sin_phi, cos_theta) - sin_a * sin_theta
    l2 = cos_b * (cos_a * sin_theta - np.outer(sin_phi, cos_theta * sin_a))
    l = np.around(((l1 + l2) * 8)).astype(int).T
    mask_l = l >= 0
    chars = ILLUMINATION[l]

    for i in range(CIRCLE_POINTS):
        mask = mask_l[i] & (ooz[i] > zbuffer[xp[i], yp[i]])
        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output


def draw_frame(screen: pygame.Surface, frame: np.ndarray, theme_colors: list[tuple[int, int, int]]) -> None:
    screen.fill(BLACK)
    font = pygame.font.Font(None, 18)

    for y in range(SCREEN_SIZE):
        for x in range(SCREEN_SIZE):
            char = frame[y, x]
            if char != " ":
                try:
                    color_index = ILLUMINATION.tolist().index(char)
                except ValueError:
                    color_index = 0
                color = tuple(map(int, theme_colors[color_index]))
                text = font.render(char, True, color)
                screen.blit(text, (x, y))

    pygame.display.flip()


def handle_voice_command(queue: Queue, command: str) -> None:
    if "faster" in command:
        queue.put(("add", 1))
    elif "slower" in command:
        queue.put(("subtract", 1))
    elif "stop" in command:
        queue.put(("set", 0))
    elif "set" in command:
        match = re.search(r"set (.+)", command, re.IGNORECASE)
        if match:
            number_input = match.group(1).strip()
            if number_input.isdigit():
                queue.put(("set", int(number_input)))
            else:
                try:
                    new_speed = w2n.word_to_num(number_input)
                    queue.put(("set", new_speed))
                except ValueError:
                    logging.error("Invalid number input: %s", number_input)
    else:
        for theme in COLOR_THEMES:
            if theme in command:
                queue.put(("theme", theme))


def process_audio(recognizer: sr.Recognizer, source: sr.Microphone, queue: Queue) -> None:
    recognizer.adjust_for_ambient_noise(source)
    logging.debug("Listening for voice commands")
    audio = recognizer.listen(source)
    logging.debug("Audio recorded")
    logging.debug("Recognizing voice command")
    command = recognizer.recognize_google(audio).lower()
    logging.debug("Received voice command: %s", command)
    handle_voice_command(queue, command)


def process_voice_commands(queue: Queue, device_index: int) -> None:
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone(device_index) as source:
                process_audio(recognizer, source, queue)
        except sr.UnknownValueError:
            logging.debug("Could not understand audio")
        except sr.RequestError:
            logging.debug("Could not request results")
        except Exception as e:
            logging.debug("An error occurred: %s", e)


def get_microphones() -> list[str]:
    return sr.Microphone.list_microphone_names()
