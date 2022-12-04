style submit_button_text:
    anchor (.5, .5)
    pos (.5, .5)
    color "#fdfdfd"
    font "fonts/JetBrainsMono-Light.ttf"
    size 26

style variants:
    color "#a7b8b8"
    font "fonts/JetBrainsMono-Light.ttf"
    size 26


init -1 python:
    from abc import ABC, abstractmethod
    class Task(ABC):
        def __init__(self, variants, answer):
            self.variants = variants
            self.answer = answer
            self.right = False
        
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
                RadioTask({"map": False, "split": False, "zip": False, "strip": False}, "split"),
                RadioTask({"map": False, "split": False, "zip": False, "strip": False}, "split"),
            ]

        def set_result(self, result):
            self.task_results[self.current_task] = result

        @property
        def task(self):
            return self.tasks[self.current_task]

        @property
        def current_task(self):
            return self.__current_task
        
        @current_task.setter
        def current_task(self, value):
            self.__current_task = value
            self.task_ended = False


screen python_tasks_screen(controller):
    modal True

    fixed:
        frame:
            background "python_tasks/pycharm_bg.png"

        viewport:
            pos 28, 106
            xysize 1870, 890
            mousewheel "vertical"        

            frame:
                background "python_tasks/pycharm_task[controller.current_task].png"

        showif controller.ans_panel:
            frame:
                pos 28, 650
                xysize 1870, 349
                background "python_tasks/variant_bg.png"
                use variants_screen(controller)

        imagebutton at shake:
            if controller.ans_panel:
                idle "python_tasks/arrow_down.png"
            else:
                idle "python_tasks/arrow_up.png"
            pos 28, 935
            action ToggleVariable("controller.ans_panel")
        
    showif controller.task_ended:
        on "show" action FileTakeScreenshot()
        use task_ended_screen(controller)


screen task_ended_screen(controller):
    modal True

    add FileCurrentScreenshot() at blur

    showif controller.task.right:
        add "python_tasks/success.png" at task_ended_transform
    else:
        add "python_tasks/failure.png" at task_ended_transform

    imagebutton at zooming:
        align .9, .5
        idle "python_tasks/next_task.png"
        action [SetVariable("controller.current_task", controller.current_task + 1)]


screen variants_screen(controller):
    fixed:
        vbox:
            ypos 30
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
                xpos 30
                idle "python_tasks/submit.png"
                insensitive "python_tasks/submit_inactive.png"
                sensitive controller.task.has_answer and not controller.task_ended
                action [ToggleVariable("controller.task_ended"), Function(controller.task.set_right)]
            
        textbutton "Подсказка":
            background "python_tasks/button_bg.png"
            xysize 180, 100
            pos 1680, 240
            text_style "submit_button_text"
            action SayOnScreen("task1_saying")
            


label task1_saying():
    "{cps=20}Похоже, здесь что-то инициализируется. Но код поврежден...{/cps}" 
    return

label task2_saying():
    "{cps=20}Хз че тут, еще не придумал{/cps}"
    $ saying_ended = True     
    return


label python_tasks():
    "start"
    $ controller = Controller()
    $ renpy.block_rollback()
    call screen python_tasks_screen(controller)
    "end"
    return