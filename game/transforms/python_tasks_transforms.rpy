transform task_ended_transform:
    xalign 0.5 yalign 0.5 zoom 0.0
    on appear:
        ease 1.0 zoom 1.0
    on show:
        block:
            ease 1.0 zoom 1.25
            ease 1.0 zoom 1.0
            repeat
        