import flet
import json
from tkinter import *
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    icons,
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete, completed=False):
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=self.completed, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        #this will be returned by the end of this function to be called in the to-do app
        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        
        #this too will be returned by the end of this function to be called in the to-do app
        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)
        self.update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TodoApp(UserControl):
    
    def __init__(self):
        super().__init__() 
        ##try / catch statement to find or create a json file
        try:
            with open("..\\..\\json\\Tasks\\Tasks.json", "r") as f:
                tasks = json.load(f) #load the json file into a vairiable 
        except FileNotFoundError:
            tasks = [] #create an array, where we can store the data soon to go into a json file
        #after this try catch block, the array "tasks" now should contain json data or be empty json data
        
        self.tasks = Column() #this outputs "column{}"
    
        for task_dict in tasks:
            task = Task( #call the task class
                 
                task_dict["name"], #extracting the name from the json
                self.task_status_change,
                self.task_delete, #has to be in this order to establish the tasks first.
                task_dict["completed"] #extracting the completed state from the json
                #task_dict["deadline"], #extracting the deadline from the json                
            )
            self.tasks.controls.append(task) #append to controls, the parameters we just extracted
        
        self.new_task = TextField(
            hint_text="What needs to be done?",
            on_submit=self.add_clicked,
            expand=True)

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")])
        
        self.items_left = Text("0 items left")
        self.save_button = FloatingActionButton(icon=icons.SAVE, on_click=self.save_tasks)
        self.add_button = FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked)

    def build(self):
        return Column(
            width=600,
            controls=[                
                Row(
                    controls=[
                        self.new_task,
                        self.add_button,
                        self.save_button,
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="Clear completed", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        selected_tab = self.filter.selected_index
        for task in self.tasks.controls:
            if selected_tab == 0:
                task.visible = True
            elif selected_tab == 1:
                task.visible = not task.completed
            elif selected_tab == 2:
                task.visible = task.completed
        self.update()
    
    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        super().update()

    def clear_clicked(self, e):
        self.tasks.controls = [task for task in self.tasks.controls if not task.completed]
        self.update()

    def save_tasks(self, e):
        tasks = []
        
        for task in self.tasks.controls:
            tasks.append(
                {
                    "name": task.display_task.label, 
                    "completed": task.completed,
                   
                    "id": None,
                    "Subject": None,
                    "Description": None,
                    "duration": None,
                    "deadline": None,
                    "Fudge factor": False
                    }
                )
        with open("..\\..\\json\\Tasks\\Tasks.json", "w") as f:
            json.dump(tasks, f)
        self.update()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def main(page: Page):   
    #page.horizontal_alignment = "center" #old code, didnt work
    page.title = "To Do App"
    #grab screen dimentions
    root = Tk()
    screen_width = root.winfo_screenwidth()
   
    #app dimentions
    page.window_height = 300
    page.window_width = 1500
    center_of_app = page.window_width*0.5
    
    #app Positioning
    page.window_top = 0
    page.window_left = screen_width*0.5 - center_of_app
    
    page.window_always_on_top = True
    page.window_frameless = True
    page.scroll = "adaptive"
    page.update()
    
    # create application instance
    app = TodoApp()
        
    # add application's root control to the page
    page.add(app)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
flet.app(target=main)

