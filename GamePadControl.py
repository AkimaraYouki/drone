

def joystick_stream():
    import pygame
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        raise RuntimeError("조이스틱이 연결되어 있지 않습니다.")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        pygame.event.pump()
        lx = joystick.get_axis(0)
        ly = joystick.get_axis(1)
        rx = joystick.get_axis(2)
        ry = joystick.get_axis(3)
        yield lx, ly, rx, ry


for lx, ly, rx, ry in joystick_stream():
    print(lx, ly, rx, ry)