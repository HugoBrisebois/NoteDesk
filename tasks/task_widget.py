import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from .tasks import Task, TaskManager
from datetime import datetime

class TaskWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_manager = TaskManager()
        self.tasks = []
        
        # Control panel for filtering and sorting
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill='x', pady=(0, 10))
        
        # Filter controls
        self.filter_var = tk.StringVar(value="all")
        ttk.Label(self.control_frame, text="Filter:").pack(side='left', padx=5)
        self.filter_combo = ttk.Combobox(
            self.control_frame, 
            values=["all", "completed", "pending"],
            textvariable=self.filter_var,
            state="readonly",
            width=10
        )
        self.filter_combo.pack(side='left', padx=5)
        self.filter_combo.bind('<<ComboboxSelected>>', self.apply_filter)
        
        # Sort controls
        self.sort_var = tk.StringVar(value="priority")  # Changed from "date" to "priority"
        ttk.Label(self.control_frame, text="Sort by:").pack(side='left', padx=5)
        self.sort_combo = ttk.Combobox(
            self.control_frame,
            values=["date", "priority", "name"],
            textvariable=self.sort_var,
            state="readonly",
            width=10
        )
        self.sort_combo.pack(side='left', padx=5)
        self.sort_combo.bind('<<ComboboxSelected>>', self.apply_sort)
        
        # Task list
        self.task_frame = ttk.Frame(self)
        self.task_frame.pack(fill='both', expand=True)
        
        # Scrollable task list
        self.canvas = tk.Canvas(self.task_frame)
        self.scrollbar = ttk.Scrollbar(self.task_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind resize event
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

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

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

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
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all tasks and sort them
        tasks = self.task_manager.get_all_tasks()
        
        # Define priority order
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        
        # Sort tasks by priority and status
        sorted_tasks = sorted(tasks, 
            key=lambda x: (
                0 if x.status == "Pending" else 1,  # Pending tasks first
                priority_order.get(x.priority, 4),   # Then by priority
                x.due_date if x.due_date else datetime.max  # Then by due date
            )
        )
        
        # Insert sorted tasks into the tree
        for task in sorted_tasks:
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

    def apply_filter(self, event=None):
        filter_type = self.filter_var.get()
        for task in self.tasks:
            if filter_type == "all":
                task.frame.pack(fill='x', pady=2)
            elif filter_type == "completed" and task.completed:
                task.frame.pack(fill='x', pady=2)
            elif filter_type == "pending" and not task.completed:
                task.frame.pack(fill='x', pady=2)
            else:
                task.frame.pack_forget()

    def apply_sort(self, event=None):
        sort_by = self.sort_var.get()
        if sort_by == "date":
            self.tasks.sort(key=lambda x: x.creation_date)
        elif sort_by == "priority":
            self.tasks.sort(key=lambda x: x.priority, reverse=True)
        elif sort_by == "name":
            self.tasks.sort(key=lambda x: x.description.lower())
        
        # Repack all visible tasks in the new order
        for task in self.tasks:
            task.frame.pack_forget()
        self.apply_filter()

