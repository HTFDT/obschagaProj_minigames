init:
    python: #Borrowed code to show dialogue OVER other screens
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


label intermediary_sayonscreen(lbl, original_layers, *args, **kwargs): #Borrowed code to show dialogue OVER other screens
    $ config.context_clear_layers = original_layers
    $ renpy.call(lbl, *args, **kwargs)
    return


screen absorb_input(): #Borrowed code to block anything below while showing dialogue OVER other screens
    # layer "above_screens" #added to bump this to a higher layer so I can blur the background.
    zorder 1000
    key 'dismiss' action Function(renpy.ui.saybehavior, allow_dismiss=renpy.config.say_allow_dismiss)
    button:
        xysize (config.screen_width, config.screen_height)
        action Function(renpy.ui.saybehavior, allow_dismiss=renpy.config.say_allow_dismiss)


label test_say:
    e "бубубубуб"

screen inventory():
    modal True
    vbox:
        textbutton "say" action SayOnScreen("test_say")
        textbutton "item" action Return("item_1")
        textbutton "Return" action Return("exit")

label call_inventory():
    call screen inventory(_zorder=-1)  # show inventory again but below screen say


transform cd_transform:
    # This is run before appear, show, or hide.
    xalign 0.5 yalign 0.5 alpha 0.0

    on appear:
        alpha 1.0
    on show:
        zoom .75
        linear .25 zoom 1.0 alpha 1.0
    on hide:
        linear .25 zoom 1.25 alpha 0.0

screen countdown():
    default n = 3

    vbox:
        textbutton "3" action SetScreenVariable("n", 3)
        textbutton "2" action SetScreenVariable("n", 2)
        textbutton "1" action SetScreenVariable("n", 1)
        textbutton "0" action SetScreenVariable("n", 0)


    showif n == 2:
        text "Two" size 100 at cd_transform
