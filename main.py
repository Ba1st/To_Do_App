from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.lang import Builder
import datetime
from datetime import date
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.snackbar import Snackbar
from plyer import filechooser

Window.size = (350, 600)


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()


class TodoApp(MDApp):

    def build(self):

        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("AddTodo.kv"))
        return screen_manager

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        screen_manager.get_screen("main").date.text = f"{days[wd]}, {day} {month} {year}"

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):

        Snackbar(text="All tasks will be saved automatically!", snackbar_x=10, snackbar_y=10,
                 size_hint_y=.08, size_hint_x=(Window.width - (10 * 2)) / Window.width,
                 bg_color=(0, 153 / 250, 1, 255 / 250)).open()

        f = open(selection[0], "r")
        fs = open("C:\\To_do_list_saved.txt", "w")
        for x in f:
            if x != "":
                screen_manager.get_screen("main").todo_list.add_widget(TodoCard(description=x))
                screen_manager.get_screen("add_todo").description.text = ""
                fs.write(x)

        fs.close()
        f.close()

    def on_complete(self, checkbox, value, description, bar):

        if value:

            with open("C:\\To_do_list_saved.txt", "r+") as f:
                new_f = f.readlines()
                f.seek(0)
                for line in new_f:
                    if f"{description.text}" not in line:
                        f.write(line)
                f.truncate()

            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179/255, 0, 1

        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 0, 153/250, 1, 255/250



    def add_todo(self, title, description):

        Snackbar(text="All tasks will be saved automatically!", snackbar_x=10, snackbar_y=10,
                 size_hint_y=.08, size_hint_x=(Window.width - (10 * 2)) / Window.width,
                 bg_color=(0, 153 / 250, 1, 255 / 250)).open()

        fa = open("C:\\To_do_list_saved.txt", "a")

        if title != "" and description != "" and len(title) < 21 and len(description) < 61:
            screen_manager.current = "main"
            screen_manager.transition.direction = "right"
            screen_manager.get_screen("main").todo_list.add_widget(TodoCard(title=title, description=description))
            screen_manager.get_screen("add_todo").description.text = ""
            fa.write("\n")
            fa.write(f"Title: {title}   Description: {description}")

        elif title == "":
            Snackbar(text="Title is missing!", snackbar_x=10, snackbar_y=10,size_hint_y=.08,
                     size_hint_x=(Window.width - (10*2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif description == "":
            Snackbar(text="Description is missing!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif len(title) > 21:
            Snackbar(text="Title should be lower than 20 characters!", snackbar_x=10, snackbar_y=10,
                     size_hint_y=.08, size_hint_x=(Window.width - (10 * 2)) / Window.width,
                     bg_color=(0, 153/250, 1, 255/250)).open()
        elif len(description) > 61:
            Snackbar(text="Description should be lower than 60 characters!", snackbar_x=10, snackbar_y=10,
                     size_hint_y=.08, size_hint_x=(Window.width - (10 * 2)) / Window.width,
                     bg_color=( 0, 153/250, 1, 255/250)).open()

        fa.close()


if __name__ == "__main__":
    TodoApp().run()
