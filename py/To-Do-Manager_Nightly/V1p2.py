import flet
import json
from flet import (Checkbox, Column, FloatingActionButton, IconButton, OutlinedButton, Page, Row, Tab, Tabs, Text, TextField, UserControl, icons)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Task(UserControl):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, task_name, task_status_change, task_delete, completed=False, deadline=None, duration=None): #newest additions: deadline, duration
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.deadline = deadline #Newest addition
        self.duration = duration #Newest addition
        self.task_status_change = task_status_change
        self.task_delete = task_delete
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def to_dict(self):
        return { #add to this section, when creating a new field
            "name": self.task_name,
            "completed": self.completed,
            "deadline": self.deadline,
            "duration": self.duration
        }
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def build(self):
        #this pretains to each task. we create a function that will make sure each task has its own things
        #creates checkboxes for each task, but is not called here
        self.display_task = Checkbox( value=self.completed, label=self.task_name, on_change=self.status_changed )
        #creates the tasks below the user input but is not called here
        self.edit_name = TextField(label="Task", multiline=True, expand=2)
        #cretes deadline field for each task but is not called here
        self.edit_deadline = TextField(label="Deadline",expand=1) #this was added for the new text line
        #creates duration field for each task but not called here
        self.edit_duration = TextField(label ="Duration", expand=1) #i added this
        #this will be returned by the end of this function to be called in the to-do app. Creates the field to EDIT task, and DELETE it
        self.display_view = Row( alignment="spaceBetween", vertical_alignment="center", 
                                controls=[
                                    #this task is now called from above
                                    self.display_task, 
                                    Row(
                                        spacing=0, 
                                        controls=[
                                            IconButton( icon=icons.CREATE_OUTLINED, tooltip="Edit To-Do", on_click=self.edit_clicked),
                                            IconButton( icon=icons.DELETE_OUTLINE, tooltip="Delete To-Do", on_click=self.delete_clicked),
                                            ],
                                        ),
                                    ],
                                )
        
        #this too will be returned by the end of this function to be called in the to-do app
        self.edit_view = Row( visible=False, alignment="spaceBetween", vertical_alignment="center",
                             controls=[
                                 self.edit_name, # this is now called from above
                                 self.edit_deadline, #newest addition
                                 self.edit_duration, #newest addition 
                                 IconButton( icon=icons.DONE, tooltip="Update To-Do", on_click=self.save_clicked),
                                ],
                             )
        return Column(controls=[self.display_view, self.edit_view]) #this is the return from def BUILD
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label 
        self.edit_deadline.value =self.deadline or "" #this was added
        self.edit_duration.value=self.duration or "" # I added this
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.deadline = self.edit_deadline.value or None #this was added
        self.duration = self.edit_duration.value or None #i added this 
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)
        self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def delete_clicked(self, e):
        self.task_delete(self)
        self.update()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TodoApp(UserControl):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #overall purpose of init: to populate the app with tasks
    def __init__(self): 
        super().__init__() 
        #create "tasks" dict to store tasks in program in a try - catch thing
        try:
            with open("..\\..\\json\\Tasks\\Tasks.json", "r") as f:
                tasks = json.load(f) #load the json file into a vairiable 
        except FileNotFoundError:
            tasks = [] #create an array, where we can store the data soon to go into a json file
            
        self.tasks = Column() #this makes a vairiable be considered a design column
        #retrieve task information from json and place it into the tasks dict
        for task_dict in tasks:
            #extract itteratively each task
            task = Task( #call the task class
                        task_dict["name"], 
                        self.task_status_change,
                        self.task_delete, 
                        task_dict["completed"], 
                        task_dict["deadline"], #New addition
                        task_dict["duration"] #new addition
                        )
            #append each block of task information into a column based list of tasks.
            self.tasks.controls.append(task)
        #This is where the task-bar is created, but not called
        self.new_task = TextField( hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True)
        #this is where the filter tabs are created!
        self.filter = Tabs( selected_index=0, on_change=self.tabs_changed, tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")])
        #this is where the counter is created! - it then changes when you use the app
        self.items_left = Text("0 items left")
        #this is where the add and save icons are craated, next to the task-bar, but not called
        self.save_button = FloatingActionButton(icon=icons.SAVE, on_click=self.save_tasks)
        self.add_button = FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def build(self):
        #here we build the complete app, we assemble all the pieces
        return Column( width=600, controls=[      #create a column where everything can go into, a "wrapper"          
                                             Row(   #creates rows to populate
                                                 controls=[
                                                     self.new_task, # add the new-task bar into row 1
                                                     self.add_button, #add the "add" button into row 2
                                                     self.save_button, #add the "save" button into row 3
                                                     ],
                                                 ),
                                             Column( spacing=25, #go to the next column below the 3 rows that were written, above
                                                    controls=[
                                                        self.filter, # add the filter bar created above
                                                        self.tasks, #call the column based list of tasks
                                                        Row( alignment="spaceBetween", vertical_alignment="center", # create a 2 rows below the tasks where..
                                                            controls=[ 
                                                                      self.items_left, #you display the incompleted tasks in row 1...
                                                                      OutlinedButton( text="Clear completed", on_click=self.clear_clicked ), #and provide a clear button in row 2
                                                                      ],
                                                            ),
                                                        ],
                                                    ),
                                             ],
                      )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def task_status_change(self, task):
        self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all" or (status == "active" and task.completed == False) or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        super().update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def clear_clicked(self, e):
        self.tasks.controls = [task for task in self.tasks.controls if not task.completed]
        self.update()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def save_tasks(self, e):
        tasks = []
        for task in self.tasks.controls:
            tasks.append(
                {
                    "name": task.display_task.label, 
                    "completed": task.completed,
                    "deadline": task.deadline, # this was added
                    "id": None,
                    "Subject": None,
                    "Description": None,
                    "duration": task.duration, #this was added
                    "Fudge factor": False
                }
            )
        with open("..\\..\\json\\Tasks\\Tasks.json", "w") as f:
            json.dump(tasks, f)
        self.update()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def main(page: Page):
    page.title = "To Do App"
    page.window_height = 600
    page.window_width = 500
    page.horizontal_alignment = "center"    
    page.scroll = "adaptive"
    page.update()

    # create application instance
    app = TodoApp()
        
    # add application's root control to the page
    page.add(app)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
flet.app(target=main)

