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
    except ValueError:
        print("Invalid payload")
        return None

def handle_start_game(data: dict, network: NetworkManager, game: Game):
    response = { "id" : data["id"], "code": constants["GAME_CODES"]["CLIENT_ACKNOWLEDGE"], "data": "" }
    response_as_string = json.dumps(response)
    network.send_message(response_as_string.encode())
    game.place_soldiers_to_initial_pos()

def restart():
    import sys
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)


def main():
    #network = NetworkManager()
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
    is_game_started = False

    while running:

        payload = network.fetch_message()
        if payload is not None:
            data = convert_payload_to_dict(payload)
            if data is not None:
                if data["code"] == constants["GAME_CODES"]["GAME_START"]:
                    handle_start_game(data, network, game)
                    is_game_started = True

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
        
        mapUI.display()
        InteractionState.update_cursor()

        if InteractionState.want_restart:
            restart()


if __name__ == "__main__":
    main()