import pygame
import json
from MapUI import MapUI
from InteractionState import InteractionState
from Network import NetworkManager
from Game import Game

constants = {
    "GAME_CODES": {
        "GAME_START": 201,
        "GAME_UPDATE": 202,
        "GAME_END": 203,
        "CLIENT_ACKNOWLEDGE": 204,
        "ERROR": 500
    }
}

def convert_payload_to_dict(payload: bytes):
    try:
        return json.loads(payload.decode("utf-8"))
    except ValueError as e:
        print("Invalid payload", e)
        return None

def handle_start_game(data: dict, network: NetworkManager, game: Game) -> int:
    response = { "id" : data["id"], "code": constants["GAME_CODES"]["CLIENT_ACKNOWLEDGE"], "data": "" }
    response_as_string = json.dumps(response)
    network.send_message(response_as_string.encode())
    return data["data"]

def restart():
    import sys
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)

def main():
    network = NetworkManager()
    mapUI = MapUI()
    game = Game()

    mapUI.add_soldier_stats(0, None)
    mapUI.add_soldier_stats(0, None)
    mapUI.add_soldier_stats(0, None)
    mapUI.add_soldier_stats(0, None)
    mapUI.add_soldier_stats(0, None)
    mapUI.add_soldier_stats(0, None)
    mapUI.add_soldier_stats(1, None)
    mapUI.add_soldier_stats(1, None)
    mapUI.add_soldier_stats(1, None)
    mapUI.add_soldier_stats(1, None)
    mapUI.add_soldier_stats(1, None)
    mapUI.add_soldier_stats(1, None)

    running = True
    is_game_started = True

    soldiers_to_display = [[], []]
    selected_soldier = None

    while running:

        payload = network.fetch_message()
        if payload is not None:
            print("Received", payload)
            data = convert_payload_to_dict(payload)
            if data is not None:
                if data["code"] == constants["GAME_CODES"]["GAME_START"]:
                    seed = handle_start_game(data, network, game)
                    is_game_started = True
                    mapUI.generate_map(seed)

                if data["code"] == constants["GAME_CODES"]["GAME_UPDATE"]:
                    soldiers_to_display = data["data"]


        InteractionState.reset_begin_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                InteractionState.released_click = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                InteractionState.pressed_click = True
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    InteractionState.is_ended = True

        if is_game_started:
            InteractionState.update_is_clicking()
            InteractionState.mouse_pos = pygame.mouse.get_pos()
            mapUI.check_interaction()

            if InteractionState.released_click == True:
                x_mouse, y_mouse = InteractionState.mouse_pos
                x_cell = round((x_mouse / 29) - 0.5) # 29px is cell width/height
                y_cell = round((y_mouse / 29) - 0.5)
                selected_soldier = (x_cell, y_cell)

        mapUI.display(soldiers_to_display)
        InteractionState.update_cursor()

        if InteractionState.want_restart:
            restart()


if __name__ == "__main__":
    main()
