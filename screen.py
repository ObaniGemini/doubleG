class Screen:
    ratio = 8
    speed = 16
    decors = 4
    fullscreen = False


def float_val(value):
    return float(value*Screen.ratio)
    
def int_val(value):
    return int(value*Screen.ratio)


class Camera:
    def __init__(self):
        self.pos = (0, 0)

    def update_to(self, pos):
        self.pos = (-pos[0], -pos[1])