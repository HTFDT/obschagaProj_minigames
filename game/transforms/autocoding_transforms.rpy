transform success_autocoding_transform:
    xalign 0.5 yalign 0.5 alpha 0.0

    on appear:
        alpha 1.0
    on show:
        zoom .75
        linear .25 zoom 1.0 alpha 1.0
    on hide:
        linear .25 zoom 1.25 alpha 0.0