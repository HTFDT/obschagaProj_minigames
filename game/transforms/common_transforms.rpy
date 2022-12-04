transform bg_blur:
    blur 5

transform zooming:
    anchor (.5, .5)
    on hover:
        linear .25 zoom 1.25
    on idle:
        linear .25 zoom 1.0

transform shake:
    on hover:
        linear .1 xoffset 3
        linear .1 xoffset -6
        linear .1 xoffset 3


transform blur(child):
        contains:
            child
            fit "contain"
            alpha 1.0
        contains:
            child
            fit "contain"
            alpha 0.2 xoffset -3
        contains:
            child
            fit "contain"
            alpha 0.2 xoffset 3
        contains:
            child
            fit "contain"
            alpha 0.2 yoffset -3
        contains:
            child
            fit "contain"
            alpha 0.2 yoffset 3