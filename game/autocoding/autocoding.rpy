init python:
    text_ended = False
    class AutoText(renpy.Displayable):
        def __init__(self, filename, speed, **kwargs):
            import os
            super(AutoText, self).__init__(**kwargs)

            self.speed = speed
            filepath = os.path.abspath(os.path.join(config.basedir, "game", "autocoding", filename))
            file = open(filepath, "r")
            self.code = file.read()
            self.code_pos = 0
            self.dcode = ""
            self.ended = False
            self.line_cnt = 0
            file.close()
    
        def render(self, width, height, st, at):
            dtext = Text(self.dcode, color="#1eff00", size=14)
            child_render = renpy.render(dtext, width, height, st, at)

            self.width, self.height = child_render.get_size()

            render = renpy.Render(self.width, self.height)
            render.blit(child_render, (0, 0))
            return render
        
        def event(self, ev, x, y, st):
            import pygame
            global text_ended

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return
                if self.ended:
                    text_ended = True
                    return True
                self.add_text()
                if self.height >= 575:
                    self.dcode = ""
                if not self.ended and not text_ended:
                    renpy.redraw(self, 0)   
                raise renpy.IgnoreEvent()

        def add_text(self):
            if self.code_pos + self.speed <= len(self.code):
                self.dcode += self.code[self.code_pos:self.code_pos + self.speed]
            else:
                self.dcode += self.code[self.code_pos:len(self.code)]
                self.ended = True
            self.code_pos += self.speed



screen autocoding_screen():
    modal True

    frame:
        background Image("images/autocoding/bg_autocoding.png")
        frame:
            background None
            xpadding 5
            area (497, 260, 927, 575)
            add AutoText("code.txt", 20)
        
    showif text_ended:
        text "success" color "#05c22b" size 100 at success_autocoding_transform
        imagebutton:
            idle "autocoding/remove.png"
            align 0.95, 0.05
            anchor .5, .5
            xsize 30
            ysize 30
            action Return()


label autocoding:
    "бла бла"

    window hide

    show screen autocoding_screen
    $ renpy.pause(modal=True)

    window show
    
    "{cps=10}Похоже, у меня получилось{/cps}{nw}"

    hide screen autocoding_screen

    return





                