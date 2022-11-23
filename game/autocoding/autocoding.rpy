init:
    image bg autocoding = "images/autocoding/bg_autocoding.png"

    python:
        res = None

        class Autocoding(renpy.Displayable):
            def __init__(self, filename, speed=1):
                import os
                renpy.Displayable.__init__(self, speed)

                self.speed = speed
                filepath = os.path.abspath(os.path.join(config.basedir, "game", "autocoding", filename))
                file = open(filepath, "r")
                self.code = file.read()
                self.code_pos = 0
                self.dcode = ""
                self.ended = False
                file.close()
            
            def render(self, width, height, st, at):
                code = Text(self.dcode, color="#28f903", size=14)
                # width: 927, heigth: 621
                render = renpy.render(code, 927, 621, st, at)
                r = renpy.Render(width, height)
                position = r.get_size()
                r.blit(render, (497, 260))
                return r
            
            def event(self, ev, x, y, st):
                import pygame
                # костыль ебаный
                global res

                if ev.type == pygame.KEYDOWN:
                    if self.ended:
                        res = "something"
                        renpy.end_interaction(True)

                    if self.code_pos + self.speed <= len(self.code):
                        self.dcode += self.code[self.code_pos:self.code_pos + self.speed]
                        self.code_pos += self.speed
                    else:
                        self.dcode += self.code[self.code_pos:]
                        self.ended = True 

                renpy.redraw(self, 0)
                raise renpy.IgnoreEvent()

# блять короче лучше все делать скринами, потому что дисплейебли сами по себе без скрина хуйня
screen autocoding_screen():
    add Autocoding("code.txt", 10)


label autocoding:
    window hide
    scene bg autocoding

    call screen autocoding_screen()

    scene black

    window show 

    "Текст кончился. Возвращенное значение: [res]"

    return





                