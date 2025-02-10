import logging
import threading
from queue import Queue

import pygame

from .config import (
    ICON_PATH,
    INITIAL_ANGLE,
    INITIAL_ROTATION_SPEED,
    MAX_ROTATION_SPEED,
    MIN_ROTATION_SPEED,
    PHI_SPACING,
    SCREEN_SIZE,
    THETA_SPACING,
    TITLE,
)
from .utils import draw_frame, get_microphones, process_voice_commands, render_frame


def select_microphone_index():
    microphones = get_microphones()
    for index, microphone in enumerate(microphones):
        logging.info("Microphone index: %s, name: %s", index, microphone)
    return int(input("Enter your microphone index:\n"))


def setup_screen():
    pygame.init()
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption(TITLE)
    logging.info("Screen initialized")
    return screen


def handle_voice_commands(voice_commands_queue: Queue, current_rotation_speed: int):
    while not voice_commands_queue.empty():
        command_type, value = voice_commands_queue.get()
        logging.info("Received voice command: %s, value: %s", command_type, value)

        if command_type == "add":
            current_rotation_speed = min(MAX_ROTATION_SPEED, current_rotation_speed + 1)
        elif command_type == "subtract":
            current_rotation_speed = max(MIN_ROTATION_SPEED, current_rotation_speed - 1)
        elif command_type == "set":
            current_rotation_speed = max(MIN_ROTATION_SPEED, min(value, MAX_ROTATION_SPEED))
        else:
            logging.error("Unknown command type: %s", command_type)

        logging.info("Current rotation speed: %s", current_rotation_speed)
    return current_rotation_speed


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    device_index = select_microphone_index()
    screen = setup_screen()

    voice_commands_queue = Queue()
    voice_thread = threading.Thread(
        target=lambda: process_voice_commands(voice_commands_queue, device_index=device_index), daemon=True
    )
    voice_thread.start()
    logging.info("Voice commands processing started")

    running = True
    current_rotation_speed = INITIAL_ROTATION_SPEED
    current_angle_a = INITIAL_ANGLE
    current_angle_b = INITIAL_ANGLE
    clock = pygame.time.Clock()

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_rotation_speed = handle_voice_commands(voice_commands_queue, current_rotation_speed)
            current_angle_a += THETA_SPACING * current_rotation_speed
            current_angle_b += PHI_SPACING * current_rotation_speed

            frame = render_frame(current_angle_a, current_angle_b)
            draw_frame(screen, frame)
            clock.tick(500)
    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        logging.info("Cleaning up")
        pygame.quit()


if __name__ == "__main__":
    main()
