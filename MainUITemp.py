import pygame
from MapUI import MapUI
from InteractionState import InteractionState


def main():
    
    mapUI = MapUI()

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

    while running:

        InteractionState.reset_begin_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                InteractionState.released_click = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                InteractionState.pressed_click = True

        
        InteractionState.update_is_clicking()
        InteractionState.mouse_pos = pygame.mouse.get_pos()
        
        mapUI.check_interaction()
        mapUI.display()

        InteractionState.update_cursor()


if __name__ == "__main__":
    main()