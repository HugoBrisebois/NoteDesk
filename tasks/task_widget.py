import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from .tasks import Task, TaskManager

class TaskWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_manager = TaskManager()
        self.setup_ui()

    def setup_ui(self):
        # Add Task Form
        form_frame = ttk.LabelFrame(self, text="Add New Task")
        form_frame.pack(fill="x", padx=5, pady=5)

        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        # Due Date
        ttk.Label(form_frame, text="Due Date:").grid(row=2, column=0, padx=5, pady=5)
        self.due_date = DateEntry(form_frame)
        self.due_date.grid(row=2, column=1, padx=5, pady=5)

        # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
        self.priority = ttk.Combobox(form_frame, values=["Low", "Medium", "High"])
        self.priority.set("Medium")
        self.priority.grid(row=3, column=1, padx=5, pady=5)

        # Create buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Add Task button
        ttk.Button(buttons_frame, text="Add Task", command=self.add_task).pack(side='left', padx=5)

        # Delete Task button
        ttk.Button(buttons_frame, text="Delete Task", command=self.delete_task).pack(side='left', padx=5)

        # Tasks List
        list_frame = ttk.LabelFrame(self, text="Tasks")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Create Treeview
        self.tree = ttk.Treeview(list_frame, columns=("Title", "Due Date", "Priority", "Status"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True)

        

        # Load existing tasks
        self.refresh_task_list()

    def add_task(self):
        task = Task(
            title=self.title_entry.get(),
            description=self.desc_entry.get(),
            due_date=self.due_date.get_date(),
            priority=self.priority.get()
        )
        self.task_manager.add_task(task)
        self.refresh_task_list()
        self.clear_form()

    def refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for task in self.task_manager.get_all_tasks():
            self.tree.insert("", "end", values=(
                task.title,
                task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
                task.priority,
                task.status
            ))

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority.set("Medium")

    def delete_task(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            return  # Nothing selected
        
        # Get the index of selected item
        index = self.tree.index(selected_item)
        
        # Delete from task manager
        self.task_manager.delete_task(index)
        
        # Refresh the display
        self.refresh_task_list()

