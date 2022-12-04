init:
    python:
        class SayOnScreen(Action):
            def __init__(self, label, *args, **kwargs):
                self.old_clear_layers = config.context_clear_layers
                self.label = label
                self.args = args
                self.kwargs = kwargs

            def __call__(self):
                renpy.config.context_clear_layers = [ ]
                renpy.call_in_new_context('intermediary_sayonscreen',
                    self.label, self.old_clear_layers,
                    *self.args, **self.kwargs)

        class Autocoding():
            def __init__(self, filename, speed):
                import string
                alph = "йцукенгшщзхъфывапролджэячсмитьбю"
                keymap = string.ascii_letters + string.digits + alph
                self.keymap = list(keymap) + ["K_SPACE"]
                filepath = os.path.abspath(os.path.join(config.basedir, "game", "autocoding", filename))
                with open(filepath) as file:
                    self.code = file.read()
                self.code_pos = 0
                self.dcode = ""
                self.code_ended = False
                self.speed = speed
                self.yadj = ui.adjustment(ranged=self.ranged)
            
            def add_text(self):
                if self.code_pos + self.speed <= len(self.code):
                    self.dcode += self.code[self.code_pos:self.code_pos + self.speed]
                else:
                    self.dcode += self.code[self.code_pos:len(self.code)]
                    self.code_ended = True
                self.code_pos += self.speed

            @staticmethod
            def ranged(yadj):
                yadj.value = yadj.range


label intermediary_sayonscreen(lbl, original_layers, *args, **kwargs):
    $ config.context_clear_layers = original_layers
    # $ renpy.show_layer_at(bg_blur, layer="screens")
    show screen absorb_input()
    $ renpy.call(lbl, *args, **kwargs)
    hide screen absorb_input
    return


screen absorb_input():
    zorder 1000
    key 'dismiss' action Function(renpy.ui.saybehavior, allow_dismiss=renpy.config.say_allow_dismiss)
    button:
        xysize (config.screen_width, config.screen_height)
        action Function(renpy.ui.saybehavior, allow_dismiss=renpy.config.say_allow_dismiss)


label autocoding_saying():
    "{cps=10}Похоже, у меня получилось{/cps}"
    return


screen autocoding_screen(autocoding):
    modal True
    zorder 1
    key autocoding.keymap action [autocoding.add_text, renpy.restart_interaction]

    frame:
        xysize 800, 600
        anchor .5, .5
        align .5, .5
        viewport:
            mousewheel "vertical"
            yadjustment autocoding.yadj
            text "[autocoding.dcode]" size 14 color "#0cc421"

        showif autocoding.code_ended:
            text "success" color "#05c22b" size 100 at success_autocoding_transform
            timer .001 action SayOnScreen("autocoding_saying")
            key 'dismiss' action [Return(), Hide("autocoding_screen")]
            button:
                xysize (config.screen_width, config.screen_height)
                action [Return(), Hide("autocoding_screen")]
    

label autocoding():
    "start"
    
    $ autocoding = Autocoding("code.txt", 50)
    
    call screen autocoding_screen(autocoding)

    "end"

    return


