import flet as ft
import json

class Task(ft.UserControl):
    def __init__(self, input_text, remove_task):
        super().__init__()
        self.input = input_text
        self.remove_task = remove_task

    def build(self):
        #these get called in edit_view and task_view but they are only made here.
        self.task_cb = ft.Checkbox(label=self.input, expand=True)
        self.edit_tf = ft.TextField(value=self.input,expand=True)
        
        
        self.task_view = ft.Row(
            visible=True, 
            controls=[
                self.task_cb,
                ft.IconButton(icon=ft.icons.CREATE_OUTLINED,on_click=self.edit_clicked),
                ft.IconButton(icon=ft.icons.DELETE_OUTLINE,on_click=self.remove_clicked)
            ]
        )
        self.edit_view = ft.Row(
            visible=False,
            controls=[
               self.edit_tf,
               ft.IconButton(icon=ft.icons.CHECK,on_click=self.save_clicked)
            ]
        )
        return ft.Column(controls=[self.task_view, self.edit_view]) #return the task and edit views 

    def edit_clicked(self, e):
        self.task_view.visible=False
        self.edit_view.visible=True
        self.update()

    def remove_clicked(self, e):
        self.remove_task(self)
        
    def save_clicked(self, e):
        self.task_cb.label = self.edit_tf.value
        self.task_view.visible=True
        self.edit_view.visible=False
        self.update()

class ToDo(ft.UserControl):
    def build(self):
        #these will be referenced in view, this is for the text field
        self.input = ft.TextField(hint_text='What should be done?', expand=True)
        #this self.tasks contains //bill
        self.tasks = ft.Column() #calls the column from the class --> TASK, and going in further from the function ---> build, which returned column()
    
        #these are for the icons, but are not called until self.buttons_row
        #iconButton and FloatingActionButton are cosmetically different
        #visit https://flet.dev/docs/controls/floatingactionbutton for more information
        self.save_button = ft.FloatingActionButton(icon=ft.icons.SAVE, on_click=self.save_tasks) #bgcolor=ft.colors.DEEP_PURPLE_100  example of changing its colour
        self.add_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked)

        #here the buttons are called. I have broken it down like this to be more readable, and also so that you can change each button separately
        self.buttons_row = ft.Row(
            controls=[
                self.add_button, 
                self.save_button
            ]
        )

        view = ft.Column( 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, #alignment of the column
            controls=[
                ft.Text(value='Tasks To Complete', style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Text(value="The AI Decides your fate now", style=ft.TextThemeStyle.LABEL_MEDIUM),
                ft.Row(controls=[ self.input, self.buttons_row ]), # Replaced the FloatingActionButton with the new Row control
                self.tasks
            ]
        )
        return view

    def add_clicked(self, e):
        if self.input.value !='':
            task = Task(self.input.value, self.remove_task)
            self.tasks.controls.append(task)
            self.input.value = ''
            self.update()

    def remove_task(self, task):
        self.tasks.controls.remove(task)
        self.update()

#this needs to be updated to suit the new json file
    def save_tasks(self, e):
        #create a dict
        tasks = {}
        
        #for each item in 
        for i, task in enumerate(self.tasks.controls):
            tasks[i] = task.task_cb.label

        with open('New_tasks.json', 'w') as f:
            json.dump(tasks, f)
        self.update()


def main(page: ft.Page):
    page.window_height = 600
    page.window_width = 400
    page.title = 'ToDo'
    todo = ToDo() #here is where we grab the ToDo class
    page.add(todo)


ft.app(target=main)