style submit_button_text:
    yanchor .5
    ypos .5
    size 16 

    color "#7e9093"
    font "fonts/JetBrainsMono-Light.ttf"

style variants:
    color "#a7b8b8"
    font "fonts/JetBrainsMono-Light.ttf"
    size 26


init -1 python:
    from abc import ABC, abstractmethod
    class Task(ABC):
        def __init__(self, variants, answer, filename, question="", *hint):
            self.variants = variants
            self.answer = answer
            self.right = False
            self.hint = hint
            self.question = question
            self.filepic = filename
        
        @abstractmethod
        def set_right(self):
            pass

        @abstractmethod
        def __call__(self, variant):
            pass

    
    class RadioTask(Task):
        def set_right(self):
            for k, v in self.variants.items():
                if v:
                    ans = k
                    break
            self.right = ans == self.answer

        @property
        def has_answer(self):
            return any(self[i] for i in self)
        
        def __call__(self, variant):
            self.variants[variant] = not self.variants[variant]
            for k in self.variants:
                if k != variant:
                    self.variants[k] = False

        def __getitem__(self, item):
            return self.variants[item]

        def __iter__(self):
            return iter(self.variants.keys())


    class Controller:
        def __init__(self):
            self.task_ended = False
            self.ans_panel = True
            self.__current_task = 0
            self.tasks = [
                RadioTask({"os.getcwd()": False, "os.path.join()": False, "os.path.realpath()": False, "os.path.split()": False}, "os.path.join()", "python_tasks/task_0/filepic.png", "Какой метод следует применить, чтобы устанить ошибку?", "Похоже, система не может найти нужный файл. Проблема пожет быть в типе операционной системы. Стоит впомнить модуль os..."),
                RadioTask({"__add__": False, "__mul__": False, "__sub__": False, "__str__": False}, "__sub__", "python_tasks/task_1/filepic.png", "Какого специального метода не хватает?", "А тут какой-то класс, описывающий таймер. Ошибка точно в методе {i}run(){/i}, в классе не хватает какого-то специального метода..."),
                RadioTask({"list": False, "dict": False, "set": False, "frozenset": False}, "set", "python_tasks/task_2/filepic.png", "Какую коллекцию лучше всего использовать для переменной {i}visited{/i}?", "Похоже на рекурсивный алгоритм обхода графа, но отсутствует коллекция, в которую должны складываться уже посещенные узлы... Какую бы лучше использовать?", "Да еще и этот граф... Может быть, в нем содержится что-то важное?"),
                RadioTask({"wb": False, "w": False, "r": False, "a": False}, "a", "python_tasks/task_3/filepic.png", "Какой аргумент нужно передать функции {i}open{/i}, чтобы декоратор работал правильно?", "Скорее всего, это декоратор, предназначенный для логгирования вызовов функций. Но функции {i}open{/i} вообще не передано тегов, показывающих, как работать с файлом логов, скорее всего, проблема в этом."),
            ]
            self.panel_mode = "answer"

        @property
        def task(self):
            return self.tasks[self.__current_task]

        @property
        def current_task(self):
            return self.__current_task
        
        @current_task.setter
        def current_task(self, value):
            self.__current_task = value
            self.task_ended = False

        @property
        def last_task(self):
            return self.current_task + 1 == len(self.tasks)

        @property
        def right_tasks_rate(self):
            return sum(int(task.right) for task in self.tasks) / len(self.tasks)


screen python_tasks_screen(controller):
    modal True

    fixed:
        frame:
            background "python_tasks/pycharm_bg.png"
        fixed:
            pos 28, 106
            xysize 1870, 890
            viewport id "vp":
                mousewheel "vertical"   

                add "python_tasks/task_[controller.current_task]/bg.png"
            
            vbar value YScrollValue("vp"):
                xpos 1850
                base_bar None
                thumb "python_tasks/scrollbar.png"

            showif controller.ans_panel:
                use bottom_panel_screen(controller)

            imagebutton at shake:
                pos 1725, 820
                action ToggleVariable("controller.ans_panel")
                if controller.ans_panel:
                    idle "python_tasks/arrow_down.png"
                else:
                    idle "python_tasks/arrow_up.png"

            button at zooming:
                background "python_tasks/hint_btn.png"
                xysize 64, 64
                pos 1830, 850
                action SayOnScreen("task_hints", controller.task.hint)
            
        add controller.task.filepic at:
            pos (26, 72)
                

        hbox:
            pos 28, 1026    
            ysize 28
            spacing 10
            button:
                xsize 78
                action SetVariable("controller.panel_mode", "answer")
                selected controller.panel_mode == "answer"
                selected_background "python_tasks/answer_button_selected.png"
                background "python_tasks/answer_button_idle.png"
            
            button:
                xsize 87
                action SetVariable("controller.panel_mode", "error")
                selected controller.panel_mode == "error"
                selected_background "python_tasks/error_button_selected.png"
                background "python_tasks/error_button_idle.png"
            
        
    showif controller.task_ended:
        on "show" action [FileTakeScreenshot(), Show("task_ended_screen", None, controller)]

screen task_ended_screen(controller):
    modal True
    zorder 1

    add FileCurrentScreenshot() at blur

    imagebutton at zooming:
        pos .95, .5
        idle "python_tasks/next_task.png"
        action [If(controller.last_task, [Hide("python_tasks_screen", Fade(2.0, 0.0, 0.0, color="#fff")), Return(controller.right_tasks_rate)], SetVariable("controller.current_task", controller.current_task + 1)), Hide("task_ended_screen")]

screen bottom_panel_screen(controller):
    fixed:
        yanchor 1.0
        ypos 1.0
        xysize 1870, 349
        showif controller.panel_mode == "answer":
            use variants_screen(controller)
        elif controller.panel_mode == "error":
            use error_screen(controller)


screen variants_screen(controller):
    frame:
        background "python_tasks/variant_bg.png"
        viewport:
            mousewheel "vertical"
            ypos 30
            vbox:
                text controller.task.question style "variants"
                first_spacing 15
                spacing 50
                hbox:
                    box_wrap True
                    spacing 100
                    for key in controller.task:
                        vbox:
                            label key:
                                text_style "variants"
                            imagebutton:
                                if controller.task[key]:
                                    idle "python_tasks/radio_button_checked.png"
                                else:
                                    idle "python_tasks/radio_button_idle.png"
                                action Function(controller.task, key)

                imagebutton at zooming:
                    xpos 40
                    idle "python_tasks/submit.png"
                    insensitive "python_tasks/submit_inactive.png"
                    sensitive controller.task.has_answer
                    action [controller.task.set_right, ToggleVariable("controller.task_ended")]


screen error_screen(controller):
    frame:
        background "python_tasks/error_panel_bg.png"
        viewport:
            pos 66, 26
            xysize 1795, 318
            mousewheel "vertical"
            draggable True
            add "python_tasks/task_[controller.current_task]/error.png"

            

label task_hints(what):
    python:
        for phrase in what:
            renpy.say("", "{cps=40}[phrase]{/cps}")
    return


label python_tasks():
    "start"
    $ renpy.block_rollback()
    $ roll_forward = renpy.roll_forward_info()
    $ controller = Controller()

    window hide
    show screen python_tasks_screen(controller)

    $ rate = ui.interact(roll_forward=roll_forward)
    $ renpy.checkpoint(rate)

    "end"
    return