


class InteractionState:

    mouse_pos = None
    is_clicking = False
    released_click = False
    pressed_click = False

    nb_hovered = 0

    def reset_begin_frame():
        InteractionState.released_click = False
        InteractionState.pressed_click = False


        if InteractionState.nb_hovered < 0:
            InteractionState.nb_hovered = 0

    def update_is_clicking():

        if InteractionState.is_clicking and InteractionState.released_click:
            InteractionState.is_clicking = False
        
        elif not InteractionState.is_clicking and InteractionState.pressed_click:
            InteractionState.is_clicking = True

