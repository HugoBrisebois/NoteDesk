import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Task:
    def __init__(self, parent, description, priority=1):
        self.frame = ttk.Frame(parent)
        self.completed = False
        self.description = description
        self.priority = priority
        self.creation_date = datetime.now()
        
        # Checkbox for completion status
        self.complete_var = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(
            self.frame,
            variable=self.complete_var,
            command=self.toggle_complete
        )
        self.checkbox.pack(side='left')
        
        # Task description
        self.label = ttk.Label(self.frame, text=description)
        self.label.pack(side='left', padx=5)
        
        # Priority label
        self.priority_label = ttk.Label(self.frame, text=f"Priority: {priority}")
        self.priority_label.pack(side='right', padx=5)
        
        self.frame.pack(fill='x', pady=2)

    def toggle_complete(self):
        self.completed = self.complete_var.get()
        if self.completed:
            self.label.configure(overstrike=True)
        else:
            self.label.configure(overstrike=False)

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def update_task_status(self, index, status):
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = status

    def update_task(self, index, **kwargs):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            for key, value in kwargs.items():
                setattr(task, key, value)

    def get_all_tasks(self):
        return self.tasks.copy()
